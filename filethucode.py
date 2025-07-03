def show_admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Tạo tại khoảng")
        print("2. Xem nội dung ")
        print("3.Sửa đổi tài khoảng")
        print("4. Quay lại menu chính ")
        print("5. Thoát")
        choice = input (" nhập lựa chọn của bạn:")
        if choice == '1':
            print("Tạo tài khoảng ")
        elif choice =='2':
            print("xem nội dung")
        elif choice =='3':
            print("Sửa đổi tài khoảng")
        elif choice =='4':
            print("Quay lại menu chính")
        elif choice =='5':
            print("Thoát")
