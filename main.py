# main.py - PHIÊN BẢN TẤT CẢ TRONG MỘT
import json
import os
import uuid
# ==============================================================================
# PHẦN 1 & 2: NỀN TẢNG (ĐÃ HOÀN CHỈNH)
# ==============================================================================
# --- Các hàm xử lý file ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def load_data(file_path):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Các lớp dữ liệu ---
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    def to_dict(self):
        return {"username": self.username, "password": self.password, "role": self.role}

class Event:
    def __init__(self, name: str, date: str, capacity: int, event_id: str = None, attendees: list = None):
        self.event_id = event_id if event_id else str(uuid.uuid4())
        self.name = name
        self.date = date
        self.capacity = capacity
        self.attendees = attendees if attendees is not None else []
    def to_dict(self):
        return {"event_id": self.event_id, "name": self.name, "date": self.date, "capacity": self.capacity, "attendees": self.attendees}

# ==============================================================================
# PHẦN 3: CÁC HÀM QUẢN LÝ LOGIC (BẢN THIẾT KẾ ĐẦY ĐỦ CHO SPRINT 1)
# ==============================================================================

# --- Nhóm chức năng: Quản lý Người dùng (Dành cho TV3) ---


def register(username: str, password: str, role: str) -> bool:
    users = load_data(USERS_FILE)

    if username.strip() =='':
        print('Tên đăng nhập không được để trống.')
        return False
    
    for user in users:
        if user['username'] == username:
            print('Tên đăng nhập đã được đăng kí từ trước.')
            return False
        
    if len(password) < 6:
        print('Mật khẩu không được ít hơn 6 kí tự.')
        return False
    
    role = role.strip().lower()
    if role not in ['admin', 'organizer', 'student']:
        print('Chọn sai vai trò.')
        return False
    
    new_user = {'username': username, 'password':password, 'role': role.lower()}
    users.append(new_user)
    save_data(USERS_FILE, users)
    return True

def login(username: str, password: str) -> User | None:
    users = load_data(USERS_FILE)

    for user  in users:
        if user['username'] == username and user['password'] == password:
            return User(user['username'], user['password'], user['role'])
    return None

# --- Nhóm chức năng: Quản lý Sự kiện của ADMIN (Dành cho TV4) ---

def create_event(name: str, date: str, capacity: int, event_id: str = None) -> Event | None:
    events = load_data(EVENTS_FILE)
    if event_id:
        for e in events:
            if e['event_id'] == event_id:
                print("⚠️ ID sự kiện đã tồn tại. Vui lòng dùng ID khác.")
                return None

    new_event = Event(name=name, date=date, capacity=capacity, event_id=event_id)
    events.append(new_event.to_dict())
    save_data(EVENTS_FILE, events)
    return new_event

def update_event(event_id: str, new_data: dict) -> bool:
    """
    (Backend - TV4) Cập nhật thông tin sự kiện.
    - Logic: Tìm sự kiện theo ID, cập nhật các trường trong new_data, lưu lại.
    - Trả về: True nếu cập nhật thành công, False nếu không tìm thấy ID.
    """
    events = load_data(EVENTS_FILE)
    updated = False
    for event in events:
        if event['event_id'] == event_id:
            for key, value in new_data.items():
                if key in event:
                    event[key] = value
            updated = True
            break

    save_data(EVENTS_FILE, events)
    return updated

def delete_event(event_id: str) -> bool:
    """
    (Backend - TV4) Xóa một sự kiện.
    - Logic: Tìm và xóa sự kiện khỏi danh sách trong events.json.
    - Trả về: True nếu xóa thành công, False nếu không tìm thấy ID.
    """
    deleted = False
    events = load_data(EVENTS_FILE)  # Tải dữ liệu từ file JSON
    for i, event in enumerate(events):
        if event.get('event_id') == event_id:
            del events[i]  # Xóa sự kiện tại vị trí i
            deleted = True
            break
    save_data(EVENTS_FILE, events)  # Ghi lại dữ liệu mới vào file
    return deleted

def view_all_events() -> list[Event]:
    events_data = load_data(EVENTS_FILE)
    return [Event(**event_dict) for event_dict in events_data]

# --- Nhóm chức năng: Chức năng của STUDENT (Dành cho TV3) ---
print("Chức năng của STUDENT (Dành cho TV3)")
def search_events(keyword: str) -> list[Event]:
    keyword = keyword.lower()
    events_data = load_data(EVENTS_FILE)
    matching_events = list()

    for item in events_data: 
        if (keyword in item['name'].lower()   
            or keyword in item['date']
            or keyword in item['capacity']
            or keyword in item['event_id'].lower()
            or keyword in str(item['attendees'].lower())):
            #tạo đối tượng Event (trong class Event) và gán vào biến e
            e = Event(name = item['name'], date = item['date'], capacity = item['capacity'], event_id = item['event_id'], attendees = item['attendees'])
            matching_events.append(e)
    return matching_events

def register_for_event(username: str, event_id: str) -> tuple[bool, str]:
    """
    (Backend - TV3 & TV2) Đăng ký một người dùng cho một sự kiện.
    - Logic (Phức tạp):
        1. Kiểm tra sự kiện có tồn tại không.
        2. Kiểm tra sự kiện còn chỗ không (dựa vào capacity).
        3. Kiểm tra người dùng này đã đăng ký sự kiện này trước đó chưa (ngăn chặn trùng lặp).
        4. Nếu ổn, thêm username vào danh sách 'attendees' của sự kiện và lưu lại.
    - Trả về: Một tuple (bool, str) chứa trạng thái và tin nhắn. Ví dụ: (True, "Đăng ký thành công!"), (False, "Sự kiện đã đầy.").
    """
    # TODO: TV3 sẽ viết code logic vào đây, có thể cần sự hỗ trợ của TV2.
    events  = load_data(EVENTS_FILE)

    #Kiểm tra sự kiện có tồn tại không
    for event in events:
        if event['event_id'] == event_id:
            #kiểm tra sự kiện còn chỗ không: so sánh số lượng ng đki và sức chứa tối đa
            if len(event['attendees']) == event['capacity']:
                return False, 'Sự kiện đã đầy.'
            #ktra ng dùng đã đki sự kiện này trước đó chưa:
            if username in event['attendees']:
                return False, 'Bạn đã đăng kí sự kiện này rồi.'
            #nếu chưa có thì thêm nào ds attendees và lưu lại
            event['attendees'].append(username)
            save_data(EVENTS_FILE, events)
            return True, "Đăng kí thành công!"
    return False, 'Không tìm thấy sự kiện.'

def view_registered_events(username: str) -> list[Event]:
    """

    (Backend - TV3) Xem các sự kiện mà một người dùng đã đăng ký.
    - Logic: Duyệt qua tất cả sự kiện, trả về danh sách các sự kiện mà trong danh sách 'attendees' có chứa username.
    - Trả về: Một danh sách các đối tượng Event.
    """
    # TODO: TV3 sẽ viết code logic vào đây.
    events_data = load_data(EVENTS_FILE)
    user_events = list()

    for item in events_data:
        if username in item['attendees']: #kiểm tra username có trong attendees hay không
            #nếu có, tạo đối tượng Event (trong class Event) và gán vào biến e
            e = Event(name=item['name'], date=item['date'], capacity=item['capacity'], event_id=item['event_id'], attendees=item['attendees'])
            user_events.append(e)
    return user_events

# --- Nhóm chức năng: Chức năng của EVENT ORGANIZER (Dành cho TV4) ---

def view_attendees_for_event(event_id: str) -> list[str] | None:
    """
    (Backend - TV4) Xem danh sách người tham dự của một sự kiện cụ thể.
    - Logic: Tìm sự kiện theo ID và trả về danh sách 'attendees' của nó.
    - Trả về: Một danh sách các username, hoặc None nếu không tìm thấy sự kiện.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    events = load_data(EVENTS_FILE)
    for event in events:
        if event.event_id == event_id:
            return event.attendees
# --- Nhóm chức năng: Báo cáo & Thống kê (Dành cho TV2) ---

def calculate_total_attendees() -> int:
    """(Backend - TV2) Tính tổng số lượt đăng ký trên tất cả các sự kiện."""
    # TODO: TV2 sẽ viết code logic vào đây.
    pass

def find_events_by_attendance() -> dict:
    """
    (Backend - TV2) Tìm sự kiện có số người tham dự cao nhất và thấp nhất.
    - Trả về: Một dictionary, ví dụ: {"highest": {"name": "Tên event", "count": 100}, "lowest": ...}
    """
    # TODO: TV2 sẽ viết code logic vào đây.
    pass

def export_to_csv():
    """(Backend - TV2) Xuất báo cáo ra file CSV."""
    # TODO: TV2 sẽ viết code logic vào đây.
    pass


# ==============================================================================
# # ==============================================================================
# PHẦN 4: CÁC HÀM GIAO DIỆN & HÀM CHÍNH (Nhóm UI/UX lấp đầy)
# ==============================================================================

# --- Nhóm hàm xử lý giao diện cho Admin (Dành cho TV5) ---
def handle_create_event():
    """(UI/UX - TV5) Xử lý luồng tạo sự kiện mới."""
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

# --- Nhóm hàm xử lý giao diện cho Admin & các vai trò khác (Dành cho TV6) ---

def handle_view_all_events():
    """(UI/UX - TV6) Xử lý luồng xem tất cả sự kiện."""
    print("\n--- Danh sách tất cả sự kiện ---")
    # TODO: TV6 viết code để:
    # 1. Gọi hàm backend: all_events = view_all_events()
    # 2. Dùng vòng lặp for để duyệt qua danh sách all_events.
    # 3. In thông tin mỗi sự kiện ra màn hình theo một định dạng đẹp mắt.
    events = view_all_events()
    if not events:
        print("Hiện tại không có sự kiện nào.")
        return
    for event in events:
        print(f"ID: {event.event_id}, Tên: {event.name}, Ngày: {event.date}, Sức chứa: {event.capacity}, Người tham dự: {', '.join(event.attendees)}")

def handle_search_event():
    """(UI/UX - TV6) Xử lý luồng tìm kiếm sự kiện theo ID."""
    print("\n--- Tìm kiếm sự kiện theo ID ---")
    event_id = input("Nhập ID sự kiện cần tìm: ")
    for event in view_all_events():
        if event.event_id == event_id:
            print(f"ID: {event.event_id}, Tên: {event.name}, Ngày: {event.date}, Sức chứa: {event.capacity}, Người tham dự: {', '.join(event.attendees)}")
            return
    print("Không tìm thấy sự kiện với ID này.")
def handle_delete_event():
    """(UI/UX - TV6) Xử lý luồng xóa sự kiện."""
    # TODO: TV6 viết code để:
    # 1. Lấy input: event_id cần xóa.
    # 2. In ra một câu hỏi xác nhận (Bạn có chắc không?).
    # 3. Nếu người dùng xác nhận, gọi hàm backend: delete_event(event_id)
    # 4. In ra thông báo.
    print("\n--- Xóa sự kiện ---")
    event_id = input("Nhập ID sự kiện cần xóa: ")
    confirm = input("Bạn có chắc chắn muốn xóa sự kiện này không? (y/n): ")
    if confirm.lower() == 'y':
        delete_event(event_id)
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

def show_student_menu(current_user):
    """(UI/UX - TV6) Hiển thị và điều hướng menu cho Student."""
    # TODO: TV6 sẽ xây dựng menu tương tự như menu Admin cho các chức năng của Student
    # (Tìm kiếm, Đăng ký, Xem sự kiện đã đăng ký)
    print(f"\n--- Menu Sinh viên (Chào mừng, {current_user.username}) ---")
    print("Chức năng đang được xây dựng.")
    pass

def show_organizer_menu(current_user):
    """(UI/UX - TV5) Hiển thị và điều hướng menu cho Event Organizer."""
    # TODO: TV5 sẽ xây dựng menu cho các chức năng của Event Organizer
    print(f"\n--- Menu Nhà tổ chức (Chào mừng, {current_user.username}) ---")
    print("Chức năng đang được xây dựng.")
    pass

# --- Hàm chạy chính của chương trình ---

def main():
    """Hàm chính để điều khiển toàn bộ luồng của ứng dụng."""
    current_user = None
    
    # Tạo sẵn tài khoản admin để dễ dàng kiểm tra
    users = load_data(USERS_FILE)
    if not any(user['username'] == 'admin' for user in users):
        # Giả sử hàm register đã được TV3 hoàn thành
        # register("admin", "123", "Admin")
        # Do hàm register đang rỗng, ta tạo thủ công để test
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
                current_user = login(username, password) # Gọi hàm login của Backend
                if not current_user:
                    print("Tên đăng nhập hoặc mật khẩu không đúng.")
            
            elif choice == '2':
                # TODO: TV5 hoặc TV6 sẽ xây dựng luồng đăng ký chi tiết ở đây
                print('----- Đăng kí tài khoản mới -----')
                username = input('Tên đăng nhập: ')
                password = input('Mật khẩu: ')
                role = input('Nhập vai trò (Admin / Organizer /  Student): ')
                if register(username, password, role):
                    print('Tạo tài khoản thành công!')
                else:
                    print('tạo tài khoản thất bại. Kiểm tra lại thông tin.')

            elif choice == '0':
                print("Cảm ơn đã sử dụng chương trình!")
                break
            else:
                print("Lựa chọn không hợp lệ.")
        
        else:
            # Phân luồng dựa trên vai trò của người dùng
            if current_user.role == "Admin":
                show_admin_menu(current_user)
            elif current_user.role == "Student":
                show_student_menu(current_user)
            elif current_user.role == "Event Organizer":
                show_organizer_menu(current_user)
            
            # Sau khi người dùng đăng xuất từ menu con, đặt lại current_user để quay về menu chính
            current_user = None 

if __name__ == "__main__":
    main()