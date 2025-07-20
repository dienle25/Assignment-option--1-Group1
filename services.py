# services.py
import uuid
import csv
import os
from datetime import datetime  # để xử lý ngày giờ


from models import User, Event
from file_handler import load_data, save_data, USERS_FILE, EVENTS_FILE
# ... (code các hàm logic của bạn)
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

    for user in users:
        user['role'] = user['role'].strip().lower()

    for user  in users:
        if user['username'] == username and user['password'] == password:
            return User(user['username'], user['password'], user['role'])
    return None

# --- Nhóm chức năng: Quản lý Sự kiện của ADMIN (Dành cho TV4) ---

def create_event(name: str, date: str, capacity: int, event_id: str = None, created_by: str = "") -> Event | None:
    events = load_data(EVENTS_FILE)

    # ✅ CHẶN sự kiện trong quá khứ
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d").date()
        if event_date < datetime.now().date():
            print("❌ Không thể tạo sự kiện trong quá khứ.")
            return None
    except ValueError:
        print("❌ Ngày không hợp lệ. Vui lòng nhập đúng định dạng YYYY-MM-DD.")
        return None

    # ✅ CHẶN trùng tên và ngày
    for event in events:
        if event['name'].strip().lower() == name.strip().lower() and event['date'] == date:
            print("⚠️ Đã tồn tại một sự kiện có cùng tên và ngày. Không thể tạo trùng.")
            return None

    # ✅ Nếu không nhập ID → tự động tạo ID kiểu ev0001
    if not event_id:
        existing_ids = [e.get("event_id", "") for e in events if e.get("event_id", "").startswith("ev")]
        next_num = 1
        while True:
            new_id = f"ev{next_num:04d}"
            if new_id not in existing_ids:
                event_id = new_id
                break
            next_num += 1
    else:
        for e in events:
            if e['event_id'] == event_id:
                print("⚠️ ID sự kiện đã tồn tại.")
                return None

    new_event = Event(name=name, date=date, capacity=capacity, event_id=event_id, created_by=created_by)
    event_dict = new_event.to_dict()
    event_dict['created_by'] = created_by  # Thêm người tạo
    event_dict['attendees'] = []

    events.append(event_dict)
    save_data(EVENTS_FILE, events)
    return new_event

def update_event(event_id: str, new_data: dict) -> bool:
    events = load_data(EVENTS_FILE)
    updated = False
    for event in events:
        if event['event_id'] == event_id:

            # ✅ Kiểm tra ngày không nằm trong quá khứ
            if 'date' in new_data:
                try:
                    new_date = datetime.strptime(new_data['date'], "%Y-%m-%d").date()
                    if new_date < datetime.now().date():
                        print("❌ Không thể cập nhật ngày trong quá khứ.")
                        return False
                except ValueError:
                    print("❌ Ngày không hợp lệ.")
                    return False

            # ✅ Kiểm tra sức chứa
            if 'capacity' in new_data:
                new_capacity = new_data['capacity']
                current_attendee_count = len(event.get('attendees', []))
                if new_capacity < current_attendee_count:
                    print(f"❌ Không thể giảm sức chứa xuống {new_capacity} vì đã có {current_attendee_count} người tham gia.")
                    return False

            for key, value in new_data.items():
                if key in event:
                    event[key] = value
            updated = True
            break

    save_data(EVENTS_FILE, events)
    return updated

def delete_event(event_id: str, current_user: User) -> bool:
    """
    (Backend - TV4) Xóa một sự kiện.
    - Logic: Tìm và xóa sự kiện khỏi danh sách trong events.json.
    - Trả về: True nếu xóa thành công, False nếu không tìm thấy ID.
    """
    events = load_data(EVENTS_FILE)
    users = load_data(USERS_FILE)
    deleted = False

    for i, event in enumerate(events):
        if event.get('event_id') == event_id:
            if current_user.role != "admin" and event.get("created_by") != current_user.username:
                print("❌ Bạn không có quyền xóa sự kiện này.")
                return False
            del events[i]
            deleted = True
            break

    if not deleted:
        print("❌ Không tìm thấy sự kiện để xóa.")
        return False

    # ✅ Loại bỏ khỏi assigned_events nếu có
    for user in users:
        if user.get('role', '').strip().lower() == 'organizer':
            if 'assigned_events' in user and event_id in user['assigned_events']:
                user['assigned_events'].remove(event_id)

    save_data(EVENTS_FILE, events)
    save_data(USERS_FILE, users)

    print(f"✅ Đã xóa sự kiện '{event_id}' và cập nhật lại danh sách organizer.")
    return True

def view_attendees_for_event(event_id: str) -> list[str] | None:
    events = load_data(EVENTS_FILE)
    for event in events:
        if event['event_id'] == event_id:
            return event.get('attendees', [])
    return None

def view_all_events() -> list[Event]:
    events_data = load_data(EVENTS_FILE)
    return [Event(**event_dict) for event_dict in events_data]

def assign_event_to_organizer(username: str, event_id: str) -> bool:
    users = load_data(USERS_FILE)
    for user in users:
        user['role'] = user['role'].strip().lower()

    for user in users:
        if user['username'] == username and user['role'] == 'organizer':
            if 'assigned_events' not in user:
                user['assigned_events'] = []
            if event_id not in user['assigned_events']:
                user['assigned_events'].append(event_id)
                save_data(USERS_FILE, users)
                return True
            else:
                print("⚠️ Organizer đã được gán sự kiện này rồi.")
                return False
    print("❌ Không tìm thấy organizer.")
    return False

# --- Nhóm chức năng: Chức năng của STUDENT (Dành cho TV3) ---
def search_events(keyword: str) -> list[Event]:
    keyword = keyword.lower()
    events_data = load_data(EVENTS_FILE)
    matching_events = []

    for item in events_data:
        name = item.get('name', '').lower()
        if keyword in name:  # 🔍 So khớp theo tên
            e = Event(
                name=item['name'],
                date=item['date'],
                capacity=item['capacity'],
                event_id=item['event_id'],
                attendees=item.get('attendees', []),
                created_by=item.get('created_by', 'N/A')
            )
            matching_events.append(e)
    return matching_events

def register_for_event(username: str, event_id: str) -> tuple[bool, str]:
    events = load_data(EVENTS_FILE)

    for event in events:
        if event['event_id'] == event_id:
            if 'attendees' not in event:
                event['attendees'] = []

            if username in event['attendees']:
                return False, "duplicated"  # đã đăng ký rồi

            if len(event['attendees']) >= event['capacity']:
                return False, "full"  # sự kiện đã đầy

            event['attendees'].append(username)
            save_data(EVENTS_FILE, events)
            return True, "success"  # đăng ký thành công

    return False, "not_found"

def view_registered_events(username: str) -> list[Event]:
    events_data = load_data(EVENTS_FILE)
    user_events = []
    for item in events_data:
        if username in item.get('attendees', []):
            e = Event(
                name=item['name'],
                date=item['date'],
                capacity=item['capacity'],
                event_id=item['event_id'],
                attendees=item['attendees'],
                created_by=item.get('created_by', 'N/A')
            )
            user_events.append(e)
    return user_events

# --- Nhóm chức năng: Chức năng của EVENT ORGANIZER (Dành cho TV4) ---
def get_events_by_organizer(organizer_username):
    events = load_data(EVENTS_FILE)
    return [Event(**e) for e in events if e.get('created_by') == organizer_username]

def view_attendees_for_event(event_id: str) -> list[str] | None:
    """
    (Backend - TV4) Xem danh sách người tham dự của một sự kiện cụ thể.
    - Logic: Tìm sự kiện theo ID và trả về danh sách 'attendees' của nó.
    - Trả về: Một danh sách các username, hoặc None nếu không tìm thấy sự kiện.
    """

    events = load_data(EVENTS_FILE)
    for event in events:
        if event['event_id'] == event_id:
            return event.get('attendees', [])
    return None



# --- Nhóm chức năng: Báo cáo & Thống kê (Dành cho TV2) ---

def calculate_total_attendees() -> int:
    """(Backend - TV2) Tính tổng số lượt đăng ký trên tất cả các sự kiện."""
    events = load_data(EVENTS_FILE)
    total = 0
    for event in events:
        attendees = event.get("attendees", [])
        total += len(attendees)
    return total

def find_events_by_attendance() -> dict:
    """
    (Backend - TV2) Tìm sự kiện có số người tham dự cao nhất và thấp nhất.
    - Trả về: Một dictionary, ví dụ: 
    {"highest": {"name": ..., "count": ...}, "lowest": {"name": ..., "count": ...}}
    """
    events = load_data(EVENTS_FILE)
    if not events:
        return {"highest": None, "lowest": None}
    
    highest = {"name": None, "count": -1}
    lowest = {"name": None, "count": float('inf')}

    for event in events:
        name = event.get("name", "Unknown")
        count = len(event.get("attendees", []))

        if count > highest["count"]:
            highest = {"name": name, "count": count}
        if count < lowest["count"]:
            lowest = {"name": name, "count": count}

    return {"highest": highest, "lowest": lowest}

def export_to_csv():
    """(Backend - TV2) Xuất báo cáo ra file CSV."""
    events = load_data(EVENTS_FILE)
    filename = "events_report.csv"

    
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Event ID", "Tên sự kiện", "Ngày", "Sức chứa", "Người tạo", "Số người tham dự"])

        for event in events:
            writer.writerow([
                event.get("event_id", ""),
                event.get("name", ""),
                event.get("date", ""),
                event.get("capacity", ""),
                event.get("created_by", ""),
                len(event.get("attendees", []))
            ])

    print(f"✅ Đã xuất dữ liệu ra file: {filename}")
