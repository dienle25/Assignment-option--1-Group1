def main():
    while True:
        print("=== MENU ===")
        print("1. Đăng nhập")
        print("2. Đăng ký")
        print("0. Thoát")
        
        choice = input("Chọn chức năng (0-2): ")

        if choice == "1":
            result = login()
            if result:
                print("Đăng nhập thành công!")
            else:
                print("Đăng nhập thất bại. Vui lòng thử lại.")
        elif choice == "2":
            register()
            print("Đăng ký thành công.")
        elif choice == "0":
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
def login():
    username = input("Tên đăng nhập: ")
    password = input("Mật khẩu: ")
    return username == "admin" and password == "123"
def register():
    username = input("Chọn tên đăng nhập: ")
    password = input("Chọn mật khẩu: ")
    print(f"Tài khoản {username} đã được tạo.")
if __name__ == "__main__":
    main()
