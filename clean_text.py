import pandas as pd
import re

# Hàm xử lý văn bản: loại bỏ HTML tags, ký tự đặc biệt, chuyển về chữ thường,.
def clean_text(text):
    if pd.isnull(text):
        return ""
    # Loại bỏ HTML tags (nếu có))))
    text = re.sub(r'<[^>]+>', '', text)
    # Loại bỏ ký tự đặc biệt, chỉ giữ lại chữ và số và khoảng trắngg
    text = re.sub(r'[^\w\s]', '', text)
    # Chuyển sang chữ thường và loại bỏ khoảng trắng dư thừaa
    text = text.lower().strip()
    return text

# Đường dẫn file và tên sheet cần đọcc
input_file = "C:/Users/admin/Downloads/test_work.xlsx"
sheet_test = "test"

# Đọc dữ liệu từ sheet "test"
df_test = pd.read_excel(input_file, sheet_name=sheet_test)

# Áp dụng hàm clean_text cho cột "message"
df_test['clean_message'] = df_test['MESSAGE'].apply(clean_text)

# Ghi kết quả vào một sheet mới có tên "result" trong cùng file Excelel
# Lưu ý: Chế độ "a" là append, if_sheet_exists="replace" giúp ghi đè nếu sheet "result" đã tồn tạii nh
with pd.ExcelWriter(input_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    # Ở đây lưu toàn bộ cột clean_message, bạn có thể thay đổi nếu muốn lưu thêm dữ liệu khác ccc
    df_test[['clean_message']].to_excel(writer, sheet_name="result", index=False)

print("Hoàn thành xử lý và lưu dữ liệu sang sheet 'result'.")