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