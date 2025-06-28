

import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def load_data(file_path):
    """
    Tải dữ liệu từ một file JSON.
    Nếu file không tồn tại hoặc rỗng, trả về một danh sách rỗng.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file_path, data):
    """
    Lưu dữ liệu vào một file JSON.
    Ghi đè toàn bộ nội dung file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Ví dụ cách sử dụng ---
if __name__ == '__main__':
    # Tải danh sách người dùng
    users = load_data(USERS_FILE)
    print("Users:", users)

    # Tải danh sách sự kiện
    events = load_data(EVENTS_FILE)
    print("Events:", events)

    # Thêm một user mới (ví dụ)
    # users.append({"username": "new_user", "password": "123", "role": "Student"})
    # save_data(USERS_FILE, users)