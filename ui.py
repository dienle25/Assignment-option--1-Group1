# ui.py

# Import các module cần thiết
import services
from models import User
from file_handler import load_data, save_data, USERS_FILE
from services import create_event, update_event, view_all_events
# --- Nhóm hàm xử lý giao diện ---

def handle_create_event():
    """Xử lý luồng tạo sự kiện mới."""
    print("\n--- Tạo sự kiện mới ---")
    name = input("Nhập tên sự kiện: ")
    date = input("Nhập ngày tổ chức (NĂM-THÁNG-NGÀY): ")

    try:
        capacity = int(input("Nhập sức chứa tối đa: "))
        if capacity <= 0:
            print("⚠️ Sức chứa phải lớn hơn 0.")
            return
    except ValueError:
        print(" Sức chứa phải là số nguyên.")
        return
    use_custom_id = input("Bạn có muốn tự nhập ID sự kiện? (y/n): ").strip().lower()
    if use_custom_id == 'y':
        event_id = input("Nhập ID sự kiện (phải là duy nhất): ").strip()
    else:
        event_id = None

    new_event = create_event(name, date, capacity, event_id)
    print(f"🎉 Sự kiện '{new_event.name}' đã được tạo thành công!")
    print(f"📅 Ngày: {new_event.date}")
    print(f"🆔 ID: {new_event.event_id}")
    print(f"👥 Sức chứa: {new_event.capacity}")

def handle_search_event():
    """(UI/UX - TV6) Xử lý luồng tìm kiếm sự kiện theo ID."""
    print("\n--- Tìm kiếm sự kiện theo ID ---")
    event_id = input("Nhập ID sự kiện cần tìm: ")
    for event in view_all_events():
        if event.event_id == event_id:
            print(f"ID: {event.event_id}, Tên: {event.name}, Ngày: {event.date}, Sức chứa: {event.capacity}, Người tham dự: {', '.join(event.attendees)}")
            return
    print("Không tìm thấy sự kiện với ID này.")

def handle_update_event():
    print("\n--- Cập nhật sự kiện ---")
    event_id = input("Nhập ID sự kiện cần cập nhật: ") 
    new_name = input("Nhập tên mới (để trống nếu không thay đổi): ")
    new_date = input("Nhập ngày mới (NĂM-THÁNG-NGÀY, để trống nếu không thay đổi): ")

    new_data = {}
    if new_name.strip() != "":
        new_data["name"] = new_name
    if new_date.strip() != "":
        new_data["date"] = new_date
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

    if not new_data:
        print("⚠️ Bạn chưa nhập gì để cập nhật.")
        return

    if update_event(event_id, new_data):
        print("✅ Đã cập nhật sự kiện.")
    else:
        print("❌ Không tìm thấy sự kiện để cập nhật.")

def handle_view_all_events():
    events = services.view_all_events()
    if not events:
        print("Hiện tại không có sự kiện nào.")
        return
    for event in events:
        print(f"ID: {event.event_id}, Tên: {event.name}, Ngày: {event.date}, Sức chứa: {event.capacity}, Người tham dự: {', '.join(event.attendees)}")


def handle_delete_event():
    print("\n--- Xóa sự kiện ---")
    event_id = input("Nhập ID sự kiện cần xóa: ")
    confirm = input("Bạn có chắc chắn muốn xóa sự kiện này không? (y/n): ")
    if confirm.lower() == 'y':
        services.delete_event(event_id)
        print("✅ Đã xóa sự kiện.")
    else:
        print("❌ Hủy bỏ xóa sự kiện.")

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
        print("0. Đăng xuất")

        choice = input("Vui lòng nhập lựa chọn của bạn: ")

        if choice == '1':
            handle_create_event()
        elif choice == '2':
            handle_view_all_events()
        elif choice == '3':
            handle_update_event()
        elif choice == '4':
            handle_delete_event()
        elif choice == '5':
            handle_search_event()
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
        print("2. Tạo sự kiện mới")
        print("3. Đăng xuất")
        choice = input("Chọn một tùy chọn: ")

        if choice == '1':
            handle_view_attendees_for_organizer(current_user)
        elif choice == '2':
            handle_create_event(current_user)  # Đã có sẵn trong project
        elif choice == '3':
            print("Đăng xuất...\n")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

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