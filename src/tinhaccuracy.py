import json
import pandas as pd
import time
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor

# Load mapping
mapping_path = 'D:/GIT_files/8-3_weekend_work/src/mbbank.json'
with open(mapping_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

def get_messages_from_excel(file_path, num_messages=200):
    try:
        df = pd.read_excel(file_path, sheet_name='test')
        if 'MESSAGE' not in df.columns or 'Ground_truth' not in df.columns:
            return "Không tìm thấy cột MESSAGE hoặc Ground_truth trong file Excel"
        return df[['MESSAGE', 'Ground_truth']].head(num_messages)
    except FileNotFoundError:
        return "Không tìm thấy file Excel"
    except Exception as e:
        return f"Có lỗi xảy ra: {str(e)}"

def classify_message_with_gemini(message, api_key, data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f""" Trả về duy nhất một số: 1 hoặc 0.

        Quy tắc:
        - Nếu tin nhắn thuộc chủ đề SPAM trên key "###", trả về 1.
        - Nếu tin nhắn thuộc chủ đề NONSPAM dưới key "###", trả về 0.
        Chỉ in ra số 1 hoặc 0, không được ghi thêm bất kỳ nội dung nào khác.

    Tin nhắn: "{message}"
    {data}
   
   
    LƯU Ý: Không giải thích, không viết thêm chữ, chỉ trả về một số duy nhất là 1 hoặc 0. 
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
                return f"Lỗi API: {error_message}"

def calculateaccu(excel_path, output_path, api_key, num_messages, max_workers):
    df = get_messages_from_excel(excel_path, num_messages)
    if isinstance(df, str):
        print(df)
        return
    
    print("\nBắt đầu phân loại...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        df['CLASSIFICATION'] = list(executor.map(lambda msg: classify_message_with_gemini(msg, api_key, data), df['MESSAGE']))
    
    # Chuyển đổi kiểu dữ liệu để so sánh
    df['CLASSIFICATION'] = df['CLASSIFICATION'].astype(int)
    df['Ground_truth'] = df['Ground_truth'].astype(int)
    
    # Tính độ chính xác
    df['CORRECT'] = df['CLASSIFICATION'] == df['Ground_truth']
    accuracy = df['CORRECT'].mean() * 100
    print(f"Độ chính xác: {accuracy:.2f}%")
    
    # Lọc ra tin nhắn bị phân loại sai
    df_errors = df[df['CORRECT'] == False][['MESSAGE', 'Ground_truth', 'CLASSIFICATION']]
    
    # Ghi kết quả ra file Excel
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='Results', index=False)
        df_errors.to_excel(writer, sheet_name='Misclassified', index=False)
    
    print(f"Kết quả đã được lưu vào: {output_path}")

# Thay đổi đường dẫn và API key theo nhu cầu
excel_path = r'C:/Users/admin/Downloads/test_work.xlsx'
output_path = r'C:/Users/admin/Downloads/result_classified.xlsx'
api_key = ''
calculateaccu(excel_path, output_path, api_key, num_messages=20, max_workers=10)
