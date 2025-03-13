import json
import pandas as pd
import time
import google.generativeai as genai

# Hàm đọc danh sách các MESSAGE bị phân loại sai từ file result_classified.xlsx
def get_misclassified_messages(file_path, sheet_name="Misclassified"):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        if 'MESSAGE' not in df.columns:
            print("Không tìm thấy cột MESSAGE trong sheet", sheet_name)
            return None
        # Lấy danh sách message, nối thành một chuỗi với dấu xuống dòng
        messages = df['MESSAGE'].dropna().tolist()
        return "\n".join(messages)
    except Exception as e:
        print(f"Có lỗi khi đọc file Excel: {e}")
        return None

# Hàm gọi Gemini API để cập nhật mapping
def update_mapping_via_api(api_key, current_mapping, misclassified_text):
    # Cấu hình API key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Xây dựng prompt với dữ liệu mapping hiện tại và các message bị phân loại sai
    prompt = f"""
Đây là những nội dung thông tin bị phân loại sai:
{misclassified_text}

Hãy phân tích mapping sau và thay đổi bằng cách thêm hoặc xóa chủ đề mapping:
{json.dumps(current_mapping, ensure_ascii=False, indent=2)}

Chỉ trả về dữ liệu mapping mới dưới dạng JSON.
"""
    wait_time = 1
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_message = str(e)
            if "429" in error_message:
                print(f"Lỗi quota, thử lại sau {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                print(f"Lỗi API: {error_message}")
                return None

def main():
    # Đường dẫn tới file mapping và file chứa kết quả phân loại
    mapping_path = 'D:/GIT_files/8-3_weekend_work/MB_BANK/mapping.json'
    result_file = r'C:/Users/admin/Downloads/result_classified.xlsx'
    api_key = 'AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk'
    
    # Đọc file mapping hiện tại
    try:
        with open(mapping_path, 'r', encoding='utf-8') as file:
            current_mapping = json.load(file)
    except Exception as e:
        print(f"Không đọc được file mapping: {e}")
        return
    
    # Lấy nội dung message bị phân loại sai
    misclassified_text = get_misclassified_messages(result_file, sheet_name="Misclassified")
    if misclassified_text is None:
        return
    
    # Gọi API để cập nhật mapping
    new_mapping_text = update_mapping_via_api(api_key, current_mapping, misclassified_text)
    if new_mapping_text is None:
        print("Không nhận được dữ liệu mới từ API.")
        return
    
    # Thử parse kết quả trả về dưới dạng JSON
    try:
        new_mapping = json.loads(new_mapping_text)
    except Exception as e:
        print(f"Lỗi khi parse kết quả trả về: {e}")
        print("Nội dung trả về từ API:\n", new_mapping_text)
        return
    
    # Ghi đè file mapping.json với mapping mới
    try:
        with open(mapping_path, 'w', encoding='utf-8') as file:
            json.dump(new_mapping, file, ensure_ascii=False, indent=2)
        print("Cập nhật mapping thành công. Mapping mới:")
        print(json.dumps(new_mapping, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Lỗi khi ghi file mapping: {e}")

if __name__ == "__main__":
    main()
