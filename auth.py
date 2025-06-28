# auth.py

# Import các hàm và lớp cần thiết từ các file khác
from file_handler import load_data, save_data, USERS_FILE
from models import User

def register(username: str, password: str, role: str) -> bool:
    """
    Đăng ký một người dùng mới.
    - Trả về True nếu đăng ký thành công.
    - Trả về False nếu tên người dùng đã tồn tại.
    """
    # 1. Tải danh sách người dùng hiện có
    users_data = load_data(USERS_FILE)
    
    # 2. Kiểm tra xem username đã tồn tại chưa
    for user_dict in users_data:
        if user_dict['username'] == username:
            print(f"Lỗi: Tên người dùng '{username}' đã tồn tại.")
            return False
            
    # 3. Nếu chưa tồn tại, tạo đối tượng User mới
    new_user = User(username=username, password=password, role=role)
    
    # 4. Thêm người dùng mới (dưới dạng dictionary) vào danh sách
    users_data.append(new_user.to_dict())
    
    # 5. Lưu danh sách người dùng đã cập nhật trở lại file JSON
    save_data(USERS_FILE, users_data)
    
    print(f"Đăng ký thành công tài khoản '{username}'.")
    return True

def login(username: str, password: str) -> User | None:
    """
    Xác thực thông tin đăng nhập của người dùng.
    - Trả về đối tượng User nếu đăng nhập thành công.
    - Trả về None nếu thông tin sai.
    """
    # 1. Tải danh sách người dùng
    users_data = load_data(USERS_FILE)
    
    # 2. Tìm người dùng với username và password tương ứng
    for user_dict in users_data:
        if user_dict['username'] == username and user_dict['password'] == password:
            print(f"Chào mừng {username}!")
            # Tạo một đối tượng User từ dữ liệu đã tìm thấy và trả về
            return User(
                username=user_dict['username'], 
                password=user_dict['password'], 
                role=user_dict['role']
            )
            
    # 3. Nếu không tìm thấy, thông báo lỗi và trả về None
    print("Lỗi: Sai tên đăng nhập hoặc mật khẩu.")
    return None

# --- Ví dụ cách sử dụng (để kiểm tra) ---
if __name__ == '__main__':
    # Thử đăng ký một admin
    register("admin", "admin123", "Admin")
    
    # Thử đăng ký một sinh viên
    register("student1", "pass123", "Student")

    # Thử đăng nhập
    print("\n--- Thử đăng nhập ---")
    logged_in_user = login("admin", "admin123")
    if logged_in_user:
        print(f"Vai trò của người dùng đang đăng nhập là: {logged_in_user.role}")

    print("\n--- Thử đăng nhập sai ---")
    login("admin", "saimatkhau")