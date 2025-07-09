import uuid


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    def to_dict(self):
        return {"username": self.username, "password": self.password, "role": self.role}

class Event:
    def __init__(self, name, date, capacity, event_id=None, attendees=None, created_by=None):
        self.name = name
        self.date = date
        self.capacity = capacity
        self.event_id = event_id or str(uuid.uuid4())  # Tạo ID ngẫu nhiên nếu không có
        self.attendees = attendees or []
        self.created_by = created_by  # Thêm dòng này

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "date": self.date,
            "capacity": self.capacity,
            "event_id": self.event_id,
            "attendees": self.attendees,
            "created_by": self.created_by  # Thêm dòng này
        }