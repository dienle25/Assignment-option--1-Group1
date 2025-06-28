# event_manager.py

# Import các module cần thiết
import file_handler
from models import Event

def create_event(name: str, date: str, capacity: int) -> Event:
    """
    Tạo một sự kiện mới và lưu vào file.
    Trả về đối tượng Event vừa được tạo.
    """
    # 1. Tải danh sách các sự kiện hiện có
    events_data = file_handler.load_data(file_handler.EVENTS_FILE)
    
    # 2. Tạo một đối tượng Event mới
    # ID sẽ được tự động tạo trong lớp Event
    new_event = Event(name=name, date=date, capacity=capacity)
    
    # 3. Thêm sự kiện mới (dưới dạng dictionary) vào danh sách
    events_data.append(new_event.to_dict())
    
    # 4. Lưu lại toàn bộ danh sách sự kiện
    file_handler.save_data(file_handler.EVENTS_FILE, events_data)
    
    print(f"Sự kiện '{name}' đã được tạo thành công với ID: {new_event.event_id}")
    return new_event

def view_all_events() -> list[Event]:
    """
    Tải và trả về một danh sách tất cả các đối tượng Event.
    """
    # 1. Tải dữ liệu thô (danh sách các dictionary) từ file JSON
    events_data = file_handler.load_data(file_handler.EVENTS_FILE)
    
    # 2. Chuyển đổi mỗi dictionary thành một đối tượng Event
    all_events = []
    for event_dict in events_data:
        event = Event(
            event_id=event_dict['event_id'],
            name=event_dict['name'],
            date=event_dict['date'],
            capacity=event_dict['capacity'],
            attendees=event_dict['attendees']
        )
        all_events.append(event)
        
    return all_events

# --- Ví dụ cách sử dụng (để kiểm tra) ---
if __name__ == '__main__':
    print("--- Tạo sự kiện mới ---")
    create_event("Hội thảo AI", "2025-07-15", 100)
    create_event("Cuộc thi Hackathon", "2025-08-01", 50)
    
    print("\n--- Xem tất cả sự kiện ---")
    events = view_all_events()
    if not events:
        print("Chưa có sự kiện nào.")
    else:
        for ev in events:
            print(f"ID: {ev.event_id}, Tên: {ev.name}, Ngày: {ev.date}, Sức chứa: {len(ev.attendees)}/{ev.capacity}")