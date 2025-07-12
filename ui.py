# ui.py

# Import các module cần thiết
import services
from models import User
from file_handler import load_data, save_data, USERS_FILE
from services import create_event, update_event, view_all_events, search_events, register_for_event, view_registered_events, calculate_total_attendees,find_events_by_attendance,export_to_csv, get_events_by_organizer
# --- Nhóm hàm xử lý giao diện ---

from datetime import datetime

def handle_create_event(current_user):
    """Xử lý luồng tạo sự kiện mới, có ghi nhận người tạo."""
    print("\n--- Tạo sự kiện mới ---")
    name = input("Nhập tên sự kiện: ")

    # ✅ Kiểm tra định dạng ngày
    while True:
        date = input("Nhập ngày tổ chức (NĂM-THÁNG-NGÀY): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ Nhập không đúng định dạng. Vui lòng nhập theo dạng NĂM-THÁNG-NGÀY (VD: 2025-07-10).")

    try:
        capacity = int(input("Nhập sức chứa tối đa: "))
        if capacity <= 0:
            print("⚠️ Sức chứa phải lớn hơn 0.")
            return
    except ValueError:
        print("⚠️ Sức chứa phải là số nguyên.")
        return

    while True:
        use_custom_id = input("Bạn có muốn tự nhập ID sự kiện? (y/n): ").strip().lower()
        if use_custom_id in ['y', 'n']:
            break
        print("⚠️ Vui lòng chỉ nhập 'y' (đồng ý) hoặc 'n' (không).")

    if use_custom_id == 'y':
        event_id = input("Nhập ID sự kiện (phải là duy nhất): ").strip()
    else:
        event_id = None

    new_event = create_event(name, date, capacity, event_id, created_by=current_user.username)

    organizer_username = ""

    if current_user.role == 'admin' and new_event:
        organizer_username = input("Bạn có muốn gán sự kiện này cho organizer nào không? (nhập username hoặc Enter để bỏ qua): ").strip()
    if organizer_username:
        services.assign_event_to_organizer(organizer_username, new_event.event_id)
    if new_event:
        print(f"🎉 Sự kiện '{new_event.name}' đã được tạo thành công!")
        print(f"📅 Ngày: {new_event.date}")
        print(f"🆔 ID: {new_event.event_id}")
        print(f"👥 Sức chứa: {new_event.capacity}")
        print(f"👤 Tạo bởi: {new_event.created_by}")
        print(f"👨‍👩‍👧‍👦 Số người đã đăng ký: {len(new_event.attendees)}")
    else:
        print("❌ Không thể tạo sự kiện. Vui lòng kiểm tra lại thông tin đã nhập.")

def handle_search_event():
    """(UI/UX - TV6) Xử lý luồng tìm kiếm sự kiện theo ID."""
    print("\n--- Tìm kiếm sự kiện theo ID ---")
    event_id = input("Nhập ID sự kiện cần tìm: ")
    for event in view_all_events():
        if event.event_id == event_id:
            so_nguoi_tham_gia = len(event.attendees) if event.attendees else 0
            print(f"\n🔍 Thông tin sự kiện tìm thấy:")
            print(f"ID: {event.event_id}")
            print(f"Tên: {event.name}")
            print(f"Ngày: {event.date}")
            print(f"Sức chứa: {event.capacity}")
            print(f"Số người tham gia: {so_nguoi_tham_gia}")
            print(f"Tạo bởi: {getattr(event, 'created_by', 'Không rõ')}")
            print("-" * 40)
            return
    print("❌ Không tìm thấy sự kiện với ID này.")

def print_registered_events(username: str):
    print("\n📋 Danh sách sự kiện bạn đã đăng ký:\n")
    events = view_registered_events(username)

    if not events:
        print("❗ Bạn chưa đăng ký sự kiện nào.")
        return

    print(f"{'ID':<15} {'Tiêu đề':<30} {'Ngày':<12} {'Sức chứa':<10} {'Đã ĐK':<6} {'Tạo bởi':<10}")
    print("-" * 95)

    for event in events:
        registered = len(event.attendees) if event.attendees else 0
        created_by = getattr(event, 'created_by', 'N/A') or 'N/A'
        print(f"{event.event_id:<15} {event.name:<30} {event.date:<12} {event.capacity:<10} {registered:<6} {created_by:<10}")

def handle_update_event():
    print("\n--- Cập nhật sự kiện ---")
    event_id = input("Nhập ID sự kiện cần cập nhật: ") 
    new_name = input("Nhập tên mới (để trống nếu không thay đổi): ")
    new_date = input("Nhập ngày mới (NĂM-THÁNG-NGÀY, để trống nếu không thay đổi): ")

    new_data = {}
    if new_name.strip() != "":
        new_data["name"] = new_name
    if new_date.strip() != "":
        try:
            datetime.strptime(new_date.strip(), "%Y-%m-%d")  # kiểm tra hợp lệ
            new_data["date"] = new_date.strip()
        except ValueError:
            print("⚠️ Ngày không hợp lệ. Vui lòng nhập đúng định dạng YYYY-MM-DD.")
            return

    try:
        new_capacity = input("Nhập sức chứa mới (để trống nếu không thay đổi): ")
        if new_capacity.strip() != "":
            new_capacity = int(new_capacity)
            if new_capacity <= 0:
                print("⚠️ Sức chứa phải lớn hơn 0.")
                return
            new_data["capacity"] = new_capacity
    except ValueError:
        print("⚠️ Sức chứa phải là số nguyên.")
        return

    # ✅ Hỏi phân quyền ngay sau phần sức chứa
    while True:
        assign_organizer = input("Bạn có muốn gán organizer cho sự kiện này? (y/n): ").strip().lower()
        if assign_organizer in ['y', 'n']:
            break
        print("⚠️ Vui lòng chỉ nhập 'y' (đồng ý) hoặc 'n' (không).")

    organizer_username = ""
    if assign_organizer == 'y':
        organizer_username = input("Nhập username của organizer: ").strip()

    # ✅ Nếu không có gì để cập nhật thì dừng
    if not new_data and not organizer_username:
        print("⚠️ Bạn chưa nhập gì để cập nhật.")
        return

    # ✅ Tiến hành cập nhật sự kiện
    success = update_event(event_id, new_data)
    if success:
        print("✅ Đã cập nhật thông tin sự kiện.")
        
        if organizer_username:
            assigned = services.assign_event_to_organizer(organizer_username, event_id)
            if assigned:
                print(f"✅ Đã gán sự kiện cho organizer '{organizer_username}'.")
            else:
                print("⚠️ Không thể gán organizer. Kiểm tra lại tên người dùng và vai trò.")
    else:
        print("❌ Cập nhật thất bại. Kiểm tra lại thông tin sự kiện.")


def handle_view_all_events():
    events = services.view_all_events()
    if not events:
        print("Hiện tại không có sự kiện nào.")
        return

    print("\n📋 Danh sách tất cả sự kiện:\n")
    for event in events:
        so_nguoi_tham_du = len(event.attendees) if event.attendees else 0
        print(f"--- Sự kiện {event.event_id} ---")
        print(f"ID: {event.event_id}")
        print(f"Tên: {event.name}")
        print(f"Ngày: {event.date}")
        print(f"Sức chứa: {event.capacity}")
        print(f"Số người tham gia: {so_nguoi_tham_du}")
        print(f"Được tạo bởi: {getattr(event, 'created_by', 'Không rõ')}")
        print("-" * 40)


def handle_delete_event(current_user):
    print("\n--- Xóa sự kiện ---")
    event_id = input("Nhập ID sự kiện cần xóa: ").strip()

    # ✅ Kiểm tra chặt chẽ y/n
    while True:
        confirm = input("Bạn có chắc chắn muốn xóa sự kiện này không? (y/n): ").strip().lower()
        if confirm in ['y', 'n']:
            break
        print("⚠️ Vui lòng chỉ nhập 'y' (đồng ý) hoặc 'n' (không).")

    if confirm == 'y' or confirm == 'yes':
        success = services.delete_event(event_id, current_user)
        if success:
            print("✅ Sự kiện đã được xóa và dữ liệu đã được cập nhật.")
        else:
            print("❌ Xóa sự kiện thất bại.")
    else:
        print("❌ Hủy bỏ xóa sự kiện.")


def handle_view_attendees_for_organizer(current_user):
    users = load_data(USERS_FILE)
    user_data = next((u for u in users if u['username'] == current_user.username), None)

    if not user_data or 'assigned_events' not in user_data:
        print("❗ Bạn chưa được gán sự kiện nào.")
        return

    assigned_ids = user_data['assigned_events']
    all_events = services.view_all_events()
    organizer_events = [event for event in all_events if event.event_id in assigned_ids]

    if not organizer_events:
        print("❗ Không có sự kiện nào được gán cho bạn.")
        return

    for event in organizer_events:
        print(f"\n📌 Sự kiện: {event.name}")
        print(f"🆔 ID: {event.event_id}")
        print(f"📅 Ngày: {event.date}")
        print(f"👥 Sức chứa: {event.capacity}")
        print(f"✅ Số người đã tham gia: {len(event.attendees)}")
        print(f"👤 Người tạo: {getattr(event, 'created_by', 'Không rõ')}")
        print(f"📋 Danh sách người tham dự: {', '.join(event.attendees) if event.attendees else 'Không có'}")
        print("-" * 50)
# --- Các hàm menu chính ---



def show_admin_menu(current_user):
    """(UI/UX - TV5) Hiển thị và điều hướng menu cho Admin."""
    while True:
        print(f"\n--- Menu Admin (Đăng nhập với tài khoản: {current_user.username}) ---")
        print("1. Tạo sự kiện mới")
        print("2. Xem tất cả sự kiện")
        print("3. Cập nhật sự kiện")
        print("4. Xóa sự kiện")
        print("5. Tìm sự kiện theo ID")
        print("6. Tính tổng số người tham dự")
        print("7. Tìm sự kiện theo số lượng người tham dự")
        print("8. Xuất danh sách sự kiện ra file CSV")
        print("0. Đăng xuất")

        choice = input("Vui lòng nhập lựa chọn của bạn: ")

        if choice == '1':
            handle_create_event(current_user)
        elif choice == '2':
            handle_view_all_events()
        elif choice == '3':
            handle_update_event()
        elif choice == '4':
            handle_delete_event(current_user)
        elif choice == '5':
            handle_search_event()
        elif choice == '6':
            total = calculate_total_attendees()
            print(f"📊 Tổng số lượt đăng ký trên tất cả các sự kiện: {total}")
        elif choice == '7':
            result = find_events_by_attendance()
            highest = result['highest']
            lowest = result['lowest']

            if highest and lowest:
                print(f"📈 Sự kiện có nhiều người nhất: {highest['name']} ({highest['count']} người)")
                print(f"📉 Sự kiện có ít người nhất: {lowest['name']} ({lowest['count']} người)")
            else:
                print("❗ Không có dữ liệu sự kiện.")
        elif choice == '8':
            export_to_csv()
        elif choice == '0':
            print("Đang đăng xuất...")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")


# ... Các hàm show_student_menu, show_organizer_menu ...
def show_organizer_menu(current_user):
    """(UI/UX - TV6) Hiển thị menu cho Event Organizer."""
    while True:
        print("\n===== EVENT ORGANIZER MENU =====")
        print("1. Xem danh sách người tham dự cho sự kiện")
        print("2. Đăng xuất")
        choice = input("Chọn một tùy chọn: ")

        if choice == '1':
            handle_view_attendees_for_organizer(current_user)
        
        elif choice == '2':
            print("Đăng xuất...\n")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

def show_student_menu(current_user):
    while True:
        print(f"\n🎓 MENU HỌC SINH (Xin chào, {current_user.username})")
        print("1.  Tìm kiếm sự kiện")
        print("2.  Đăng ký tham gia sự kiện")
        print("3.  Xem các sự kiện đã đăng ký")
        print("0.  Đăng xuất")

        choice = input("Chọn chức năng (0-3): ")

        if choice == "1":
            keyword = input("Nhập từ khóa tìm kiếm: ")
            events = search_events(keyword)
            if events:
                print("\n📋 Kết quả tìm kiếm:")
                print(f"{'ID':<15} {'Tiêu đề':<30} {'Ngày':<12} {'Sức chứa':<10} {'Đã ĐK':<6} {'Tạo bởi':<10}")
                print("-" * 95)
                for event in events:
                    registered = len(event.attendees) if event.attendees else 0
                    created_by = getattr(event, 'created_by', 'N/A') or 'N/A'
                    print(f"{event.event_id:<15} {event.name:<30} {event.date:<12} {event.capacity:<10} {registered:<6} {created_by:<10}")
            else:
                print("❌ Không tìm thấy sự kiện nào phù hợp với từ khóa.")
        elif choice == "2":
            event_id = input("Nhập mã sự kiện muốn đăng ký: ")
            success, status = register_for_event(current_user.username, event_id)

            if success and status == "success":
                print("✅ Bạn đã đăng ký thành công sự kiện!")
            elif status == "duplicated":
                print("⚠️ Bạn đã đăng ký sự kiện này rồi.")
            elif status == "full":
                print("❌ Sự kiện đã đầy. Không thể đăng ký thêm.")
            elif status == "not_found":
                print("❌ Không tìm thấy sự kiện với ID bạn đã nhập.")
            else:
                print("❌ Vui lòng thử lại.")
        elif choice == "3":
            print_registered_events(current_user.username)
        elif choice == "0":
            print("Đăng xuất khỏi tài khoản học sinh.")
            break
        else:
            print("Vui lòng chọn đúng chức năng.")

# --- Hàm chạy chính của chương trình ---

def main():
    """Hàm chính để điều khiển toàn bộ luồng của ứng dụng."""
    current_user = None
    
    # Tạo sẵn tài khoản admin nếu chưa có
    users = load_data(USERS_FILE)
    if not any(user['username'] == 'admin' for user in users):
        save_data(USERS_FILE, [{"username": "admin", "password": "123", "role": "Admin"}])

    while True:
        if not current_user:
            print("\n--- HỆ THỐNG QUẢN LÝ SỰ KIỆN ---")
            print("1. Đăng nhập")
            print("2. Đăng ký")
            print("0. Thoát chương trình")
            
            choice = input("Vui lòng nhập lựa chọn của bạn: ")
            
            if choice == '1':
                username = input("Tên đăng nhập: ")
                password = input("Mật khẩu: ")
                current_user = services.login(username, password)
                if not current_user:
                    print("Tên đăng nhập hoặc mật khẩu không đúng.")
            
            elif choice == '2':
                print('----- Đăng kí tài khoản mới -----')
                username = input('Tên đăng nhập: ')
                password = input('Mật khẩu: ')
                role = input('Nhập vai trò (Admin / Organizer /  Student): ')
                if services.register(username, password, role):
                    print('Tạo tài khoản thành công!')
                else:
                    print('Tạo tài khoản thất bại. Kiểm tra lại thông tin.')

            elif choice == '0':
                print("Cảm ơn đã sử dụng chương trình!")
                break
        
        else:
            if current_user.role == 'admin':
                show_admin_menu(current_user)
            elif current_user.role == 'organizer':
                show_organizer_menu(current_user)  # Chức năng dành cho Organizer
            elif current_user.role == 'student':
                show_student_menu(current_user)  # Chức năng dành cho Student
            else:
                print("Vai trò không hợp lệ, vui lòng đăng nhập lại.")
            current_user = None