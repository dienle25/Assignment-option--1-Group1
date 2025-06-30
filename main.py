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

#viêt hàm tính tổng:
def tinh_tong_bang_de(a,b):
    a = 0
    b = 0
    r = 0
    return a + b + r

def register(username: str, password: str, role: str) -> bool:
    """
    (Backend - TV3) Đăng ký một người dùng mới.
    - Logic: Kiểm tra xem username đã tồn tại chưa. Nếu chưa, thêm user mới vào users.json.
    - Trả về: True nếu thành công, False nếu tên người dùng đã tồn tại.
    """
    # TODO: TV3 sẽ viết code logic vào đây.
    pass

def login(username: str, password: str) -> User | None:
    """
    (Backend - TV3) Xác thực đăng nhập.
    - Logic: Tìm người dùng có username và password khớp.
    - Trả về: Đối tượng User nếu tìm thấy, ngược lại trả về None.
    """
    # TODO: TV3 sẽ viết code logic vào đây.
    pass

# --- Nhóm chức năng: Quản lý Sự kiện của ADMIN (Dành cho TV4) ---

def create_event(name: str, date: str, capacity: int) -> Event | None:
    """
    (Backend - TV4) Tạo một sự kiện mới.
    - Logic: Tạo đối tượng Event mới, thêm vào events.json.
    - Trả về: Đối tượng Event vừa tạo.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    pass

def update_event(event_id: str, new_data: dict) -> bool:
    """
    (Backend - TV4) Cập nhật thông tin sự kiện.
    - Logic: Tìm sự kiện theo ID, cập nhật các trường trong new_data, lưu lại.
    - Trả về: True nếu cập nhật thành công, False nếu không tìm thấy ID.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    pass

def delete_event(event_id: str) -> bool:
    """
    (Backend - TV4) Xóa một sự kiện.
    - Logic: Tìm và xóa sự kiện khỏi danh sách trong events.json.
    - Trả về: True nếu xóa thành công, False nếu không tìm thấy ID.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    pass

def view_all_events() -> list[Event]:
    """
    (Backend - TV4) Lấy danh sách tất cả sự kiện.
    - Logic: Đọc toàn bộ file events.json và chuyển đổi thành danh sách các đối tượng Event.
    - Trả về: Một danh sách các đối tượng Event.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    return []

# --- Nhóm chức năng: Chức năng của STUDENT (Dành cho TV3) ---

def search_events(keyword: str) -> list[Event]:
    """
    (Backend - TV3) Tìm kiếm sự kiện theo tên.
    - Logic: Duyệt qua tất cả sự kiện, trả về danh sách các sự kiện có tên chứa keyword (không phân biệt hoa thường).
    - Trả về: Một danh sách các đối tượng Event tìm thấy.
    """
    # TODO: TV3 sẽ viết code logic vào đây.
    return []

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
    pass

def view_registered_events(username: str) -> list[Event]:
    """

    (Backend - TV3) Xem các sự kiện mà một người dùng đã đăng ký.
    - Logic: Duyệt qua tất cả sự kiện, trả về danh sách các sự kiện mà trong danh sách 'attendees' có chứa username.
    - Trả về: Một danh sách các đối tượng Event.
    """
    # TODO: TV3 sẽ viết code logic vào đây.
    return []

# --- Nhóm chức năng: Chức năng của EVENT ORGANIZER (Dành cho TV4) ---

def view_attendees_for_event(event_id: str) -> list[str] | None:
    """
    (Backend - TV4) Xem danh sách người tham dự của một sự kiện cụ thể.
    - Logic: Tìm sự kiện theo ID và trả về danh sách 'attendees' của nó.
    - Trả về: Một danh sách các username, hoặc None nếu không tìm thấy sự kiện.
    """
    # TODO: TV4 sẽ viết code logic vào đây.
    pass

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
def tinh_tong(a,b):
    return a + b

def handle_create_event():
    """(UI/UX - TV5) Xử lý luồng tạo sự kiện mới."""
    print("\n--- Tạo sự kiện mới ---")
    # TODO: TV5 viết code để:
    # 1. Lấy input: Tên, Ngày, Sức chứa từ người dùng.
    # 2. Xác thực đầu vào (ví dụ: sức chứa phải là số).
    # 3. Gọi hàm backend: create_event(name, date, capacity)
    # 4. In ra thông báo thành công hoặc thất bại.
    pass

def handle_update_event():
    """(UI/UX - TV5) Xử lý luồng cập nhật sự kiện."""
    # TODO: TV5 viết code để:
    # 1. Lấy input: event_id cần cập nhật.
    # 2. Lấy input: các thông tin mới (tên mới, sức chứa mới...).
    # 3. Gọi hàm backend: update_event(event_id, new_data)
    # 4. In ra thông báo.
    pass

# --- Nhóm hàm xử lý giao diện cho Admin & các vai trò khác (Dành cho TV6) ---

def handle_view_all_events():
    """(UI/UX - TV6) Xử lý luồng xem tất cả sự kiện."""
    print("\n--- Danh sách tất cả sự kiện ---")
    # TODO: TV6 viết code để:
    # 1. Gọi hàm backend: all_events = view_all_events()
    # 2. Dùng vòng lặp for để duyệt qua danh sách all_events.
    # 3. In thông tin mỗi sự kiện ra màn hình theo một định dạng đẹp mắt.
    pass

def handle_delete_event():
    """(UI/UX - TV6) Xử lý luồng xóa sự kiện."""
    # TODO: TV6 viết code để:
    # 1. Lấy input: event_id cần xóa.
    # 2. In ra một câu hỏi xác nhận (Bạn có chắc không?).
    # 3. Nếu người dùng xác nhận, gọi hàm backend: delete_event(event_id)
    # 4. In ra thông báo.
    pass

# --- Các hàm menu chính ---

def show_admin_menu(current_user):
    """(UI/UX - TV5) Hiển thị và điều hướng menu cho Admin."""
    while True:
        print(f"\n--- Menu Admin (Đăng nhập với tài khoản: {current_user.username}) ---")
        print("1. Tạo sự kiện mới")
        print("2. Xem tất cả sự kiện")
        print("3. Cập nhật sự kiện")
        print("4. Xóa sự kiện")
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
                print("Chức năng đang được xây dựng.")
                pass

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