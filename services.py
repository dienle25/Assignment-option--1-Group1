# services.py
from models import User, Event
from file_handler import load_data, save_data, USERS_FILE, EVENTS_FILE
import csv 
import uuid
# ... (code các hàm logic của bạn)
def register(username: str, password: str, role: str) -> bool:
    users = load_data(USERS_FILE)
    
    if username.strip() =='':
        return False
    
    for user in users:
        if user['username'] == username:
            return False
        
    if len(password) < 6:
        return False
    
    role = role.strip().lower()
    if role not in ['admin', 'organizer', 'student']:
        return False
    
    new_user = {'username': username, 'password':password, 'role': role.lower()}
    save_data(USERS_FILE, users)
    return True

def login(username: str, password: str) -> User | None:
    users = load_data(USERS_FILE)

    for user  in users:
        if user['username'] == username and user['password'] == password:
            return User(user['username'], user['password'], user['role'])
    return None

# --- Nhóm chức năng: Quản lý Sự kiện của ADMIN (Dành cho TV4) ---

def create_event(name: str, date: str, capacity: int) -> Event | None:
    events = load_data(EVENTS_FILE)
    new_event = Event(name=name, date=date, capacity=capacity)
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