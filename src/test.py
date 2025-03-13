import json
import pandas as pd
import random
import pathlib
import requests
import textwrap
import time
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor

prompt = 'D:/GIT_files/8-3_weekend_work/MB_BANK/mapping.json'
with open(prompt, 'r', encoding='utf-8') as file:
    data = json.load(file)

def get_messages_from_excel(file_path, num_messages=202):
    try:
        df = pd.read_excel(file_path, sheet_name='test')
        if 'MESSAGE' not in df.columns:
            return "Không tìm thấy cột MESSAGE trong file Excel"
        return df['MESSAGE'].head(num_messages).tolist()
    except FileNotFoundError:
        return "Không tìm thấy file Excel"
    except Exception as e:
        return f"Có lỗi xảy ra: {str(e)}"

def classify_message_with_gemini(message, api_key, data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""Trả về 1 hoặc 0 theo quy tắc:
- Nếu tin nhắn thuộc chủ đề từ 1 đến 19, trả về 1.
- Nếu tin nhắn thuộc chủ đề từ 20 đến 36, trả về 0.
- Nếu tin nhắn không khớp với bất kỳ chủ đề nào, trả về null
    
    Tin nhắn: "{message}"
    
    {data}
    Chỉ trả về một số duy nhất là 1 hoặc 0 hoặc null, không được trả về một giá trị nào khác.

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
                return f"Có lỗi xảy ra khi gọi Gemini API: {error_message}"

def analyze_messages(excel_path, output_path, api_key, num_messages, max_workers):
    messages = get_messages_from_excel(excel_path, num_messages)
    if isinstance(messages, str):
        print(messages)
        return
    
    print("\nKết quả phân loại:")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda msg: classify_message_with_gemini(msg, api_key, data), messages))
    
    for i, result in enumerate(results, 1):
        print(f"Tin {i}: {result}")
    
    df_result = pd.DataFrame({'MESSAGE': messages, 'CLASSIFICATION': results})
    df_result.to_excel(output_path, index=False)
    print(f"Kết quả đã được lưu vào: {output_path}")

# Thay đổi đường dẫn và API key theo nhu cầu
excel_path = r'C:/Users/admin/Downloads/test_work.xlsx'
output_path = r'C:/Users/admin/Downloads/result_classified.xlsx'
api_key = 'AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk'
analyze_messages(excel_path, output_path, api_key, num_messages=10, max_workers=5)
