def handle_create_event():
    """(UI/UX - TV5) Xử lý luồng tạo sự kiện mới."""
    print("\n--- Tạo sự kiện mới ---")

    # 1. Lấy input từ người dùng
    name = input("Nhập tên sự kiện: ").strip()
    date = input("Nhập ngày tổ chức (YYYY-MM-DD): ").strip()
    capacity_str = input("Nhập sức chứa: ").strip()

    # 2. Xác thực đầu vào
    try:
        capacity = int(capacity_str)
    except ValueError:
        print("Lỗi: Sức chứa phải là một số nguyên.")
        return

    # 3. Gọi hàm backend
    try:
        event_id = create_event(name, date, capacity)  # Hàm này bạn đã định nghĩa ở phần backend
    except Exception as e:
        print(f"Tạo sự kiện thất bại: {e}")
        return

    # 4. In ra thông báo thành công
    print(f"Tạo sự kiện thành công! (ID: {event_id})")

