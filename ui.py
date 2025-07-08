# ui.py

# Import các module cần thiết
import services
from models import User
from file_handler import load_data, save_data, USERS_FILE

# --- Nhóm hàm xử lý giao diện ---

def handle_create_event():
    """Xử lý luồng tạo sự kiện mới."""
    print("\n--- Tạo sự kiện mới ---")
    name = input("Nhập tên sự kiện: ")
    date = input("Nhập ngày diễn ra (YYYY-MM-DD): ")
    try:
        capacity = int(input("Nhập sức chứa: "))
        # Gọi hàm backend từ module services
        new_event = services.create_event(name, date, capacity)
        if new_event:
            print(f"Tạo sự kiện '{new_event.name}' thành công!")
        else:
            print("Tạo sự kiện thất bại.")
    except ValueError:
        print("Lỗi: Sức chứa phải là một số nguyên.")

# ... Các hàm handle_... khác sẽ được thêm vào đây ...


# --- Các hàm menu chính ---

def show_admin_menu(current_user):
    """Hiển thị và điều hướng menu cho Admin."""
    while True:
        print(f"\n--- Menu Admin (Đăng nhập với tài khoản: {current_user.username}) ---")
        print("1. Tạo sự kiện mới")
        print("2. Xem tất cả sự kiện")
        # ... thêm các lựa chọn khác
        print("0. Đăng xuất")
        
        choice = input("Vui lòng nhập lựa chọn của bạn: ")
        
        if choice == '1':
            handle_create_event()
        # ... elif cho các lựa chọn khác ...
        elif choice == '0':
            print("Đang đăng xuất...")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.")

# ... Các hàm show_student_menu, show_organizer_menu ...


# --- Hàm chạy chính của chương trình ---

def main():
    """Hàm chính để điều khiển toàn bộ luồng của ứng dụng."""
    current_user = None
    
    # Tạo sẵn tài khoản admin nếu chưa có
    users = load_data(USERS_FILE)
    if not any(user['username'] == 'admin' for user in users):
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
                current_user = services.login(username, password)
                if not current_user:
                    print("Tên đăng nhập hoặc mật khẩu không đúng.")
            
            elif choice == '2':
                username = input("Nhập tên đăng nhập muốn đăng ký: ")
                password = input("Nhập mật khẩu: ")
                # Mặc định vai trò là Student
                success = services.register(username, password, "Student")
                if success:
                    print("Đăng ký thành công! Vui lòng đăng nhập.")
                else:
                    print("Lỗi: Tên người dùng có thể đã tồn tại.")

            elif choice == '0':
                print("Cảm ơn đã sử dụng chương trình!")
                break
        
        else:
            # Phân luồng dựa trên vai trò của người dùng
            if current_user.role.lower() == "admin":
                show_admin_menu(current_user)
            # ... elif cho các vai trò khác ...
            
            current_user = None # Quay lại menu chính sau khi đăng xuất