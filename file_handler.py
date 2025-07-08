import os
import json
# --- Các hàm xử lý file ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ... code còn lại giữ nguyên
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