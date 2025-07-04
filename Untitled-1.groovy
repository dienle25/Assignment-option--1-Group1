def handle_update_event():
    """(UI/UX - TV5) Xử lý luồng cập nhật sự kiện."""
    print("\n--- CẬP NHẬT SỰ KIỆN ---")
    event_id = input("Nhập ID sự kiện cần cập nhật: ").strip()
    
    # Nhập thông tin mới
    new_name = input("Tên mới (để trống nếu không đổi): ").strip()
    new_date = input("Ngày mới (YYYY-MM-DD) (để trống nếu không đổi): ").strip()
    new_capacity = input("Sức chứa mới (để trống nếu không đổi): ").strip()

    # Chuyển đổi sức chứa nếu có nhập
    capacity = int(new_capacity) if new_capacity else None

    # Gọi hàm backend update_event
    success = update_event(event_id, name=new_name or None, date=new_date or None, capacity=capacity)

    if success:
        print("✅ Cập nhật sự kiện thành công.")
    else:
        print("❌ Không tìm thấy sự kiện hoặc cập nhật thất bại.")


def handle_delete_event():
    """(UI/UX - TV5) Xử lý luồng xóa sự kiện."""
    print("\n--- XOÁ SỰ KIỆN ---")
    event_id = input("Nhập ID sự kiện cần xóa: ").strip()

    confirm = input("⚠️ Bạn có chắc chắn muốn xóa sự kiện này? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Đã hủy thao tác xóa.")
        return

    # Gọi hàm backend delete_event
    success = delete_event(event_id)

    if success:
        print("✅ Đã xóa sự kiện thành công.")
    else:
        print("❌ Không tìm thấy sự kiện hoặc xóa thất bại.")
