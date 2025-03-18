# README  

## Mô tả  

Đây là một đoạn mã Python dùng để xử lý dữ liệu từ file Excel. Chương trình thực hiện các bước sau:  

1. Trích xuất thông tin từ file Excel.  
2. Tạo mapping dựa trên thông tin đã trích xuất.  
3. Phân loại dữ liệu từ file Excel bằng mapping vừa tạo thành loại NON_SENSE và MAKE_SENSE
4. Dựa trên rull được phát triển, xóa các tin nhắn rác trong loại NON_SENSE

## Cách hoạt động  

### Các bước xử lý  

1. **Trích xuất thông tin từ file Excel**  
    - Chương trình đọc dữ liệu từ file Excel đầu vào.  
    - Lấy thông tin từ sheet đầu tiên (giả sử sheet này chứa các cột `object`, `field`, `definition`, `keyword`).  

2. **Tạo mapping**  
    - Sử dụng thông tin từ sheet đầu tiên để tạo mapping thông qua hàm `gen_mapping`.  

3. **Phân loại dữ liệu**  
    - Dữ liệu từ sheet `raw_data` được lưu ra file Excel tạm thời (`processed_data.xlsx`).  
    - File này được phân loại bằng hàm `classification`, sử dụng API key và các tham số khác.  

4. **Xóa tin nhắn rác**  
    - Các tin nhắn được xác định là rác sẽ bị xóa thông qua hàm `delete_spam_message`.  

### Các hàm chính  

- `get_info(input_file)`: Trích xuất thông tin từ file Excel.  
- `main(input_excel)`: Hàm chính để xử lý dữ liệu từ file Excel đầu vào.  

## Yêu cầu  

- Python 3.x  
- Các thư viện:  
  - `pandas`  
  - `openpyxl` (để xử lý file Excel)  
- File Excel đầu vào (`input_data.xlsx`) phải có ít nhất 2 sheet:  
  - Sheet đầu tiên chứa thông tin mapping.  
  - Sheet thứ hai chứa dữ liệu thô (`raw_data`).  

## Cách sử dụng  

1. Đảm bảo đã cài đặt các thư viện cần thiết:  
    ```bash  
    pip install pandas openpyxl  
    ```  

2. Đặt file Excel đầu vào trong cùng thư mục với mã nguồn và đặt tên là `input_data.xlsx`.  

3. Chạy chương trình:  
    ```bash  
    python script.py  
    ```  

4. Kết quả:  
    - File `classified_data.xlsx` chứa dữ liệu đã được phân loại.  
    - Các tin nhắn rác sẽ bị xóa.  

## Ghi chú  

- Cập nhật API key trong biến `api_key` trước khi chạy chương trình.  
- Đảm bảo file Excel đầu vào có cấu trúc đúng như yêu cầu.  
