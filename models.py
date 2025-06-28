# models.py

import uuid # Thư viện để tạo ID duy nhất cho mỗi sự kiện

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Trong thực tế cần mã hóa, nhưng bài tập này có thể để đơn giản
        self.role = role          # Ví dụ: "Admin", "Event Organizer", "Student"

    def to_dict(self):
        """Chuyển đổi đối tượng User thành dictionary."""
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

class Event:
    def __init__(self, name: str, date: str, capacity: int, event_id: str = None, attendees: list = None):
        # Nếu không cung cấp event_id, tạo một ID mới và duy nhất
        self.event_id = event_id if event_id else str(uuid.uuid4())
        self.name = name
        self.date = date
        self.capacity = capacity
        # Nếu không có danh sách người tham dự, khởi tạo một danh sách rỗng
        self.attendees = attendees if attendees is not None else []

    def to_dict(self):
        """Chuyển đổi đối tượng Event thành dictionary."""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "date": self.date,
            "capacity": self.capacity,
            "attendees": self.attendees
        }

    def is_full(self):
        """Kiểm tra xem sự kiện đã đầy chỗ chưa."""
        return len(self.attendees) >= self.capacity

    def add_attendee(self, username):
        """Thêm một người tham dự vào sự kiện."""
        if not self.is_full() and username not in self.attendees:
            self.attendees.append(username)
            return True
        return False