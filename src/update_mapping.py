import os
import json
import time
import pandas as pd
import google.generativeai as genai
import re

def get_mapping(object_name, mapping_path='D:/GIT_files/8-3_weekend_work/src/object_mapping.json'):
    """Truy cập file object_mapping.json, tìm object và trả về dữ liệu nếu có."""
    if not os.path.exists(mapping_path):
        print("File mapping không tồn tại.")
        return None
    
    try:
        with open(mapping_path, 'r', encoding='utf-8') as file:
            object_mapping = json.load(file)
    except Exception as e:
        print(f"Lỗi đọc file mapping: {e}")
        return None
    
    return object_mapping.get(object_name, "Chưa có dữ liệu")

def get_EXPLANATION(file_path, sheet_name="Misclassified"):
    """Đọc và lấy nội dung giải thích từ file Excel."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return "\n".join(df['EXPLANATION'].dropna().tolist()) if 'EXPLANATION' in df.columns else None
    except Exception as e:
        print(f"Lỗi đọc file Excel: {e}")
        return None

def update_mapping_via_api(api_key, object_mapping, explanation):
    """Gọi API Gemini để cập nhật object_mapping."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Tạo file JSON bằng cách phân tích giải thích sau đây và cập nhật object_mapping:
    {explanation}
    
    Mapping hiện tại:
    Chủ đề thuộc loại SPAM nằm bên trên key "###"
    Chủ đề thuộc loại NONSPAM nằm bên dưới key "###"
    {json.dumps(object_mapping, ensure_ascii=False, indent=2)}
    
    Đầu ra cần ở định dạng JSON, ngăn cách hai loại bằng key "###", không thêm bất kỳ giải thích nào.
    """
    
    wait_time = 1
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):
                print(f"Lỗi quota, thử lại sau {wait_time}s...")
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, 60)
            else:
                print(f"Lỗi API: {e}")
                return None

def update_object_mapping(json_file, object_name, new_data):
    """Cập nhật object_mapping.json với dữ liệu mới."""
    if not os.path.exists(json_file):
        print(f"File {json_file} không tồn tại.")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        data[object_name] = new_data
        
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(data)
        print(f"✅ Đã cập nhật mapping cho {object_name}.")
        return True
    except Exception as e:
        print(f"❌ Lỗi cập nhật mapping: {e}")
        return False

def main(object_name):
    mapping_path = 'D:/GIT_files/8-3_weekend_work/src/object_mapping.json'
    result_file = 'C:/Users/admin/Downloads/result.xlsx'
    api_key = 'AIzaSyCX64LU5zeuA6fiIukS3jhWgPLqdFTv_dc'
    
    object_mapping = get_mapping(object_name, mapping_path)
    if object_mapping == "Chưa có dữ liệu":
        print(f"Object '{object_name}' không có trong mapping.")
        return
    
    explanation = get_EXPLANATION(result_file)
    if not explanation:
        print("Không có dữ liệu EXPLANATION hợp lệ.")
        return
    
    new_mapping_text = update_mapping_via_api(api_key, object_mapping, explanation)
    if not new_mapping_text:
        print("Không nhận được dữ liệu mới từ API.")
        return
    
    cleaned_json = re.search(r"\{.*\}", new_mapping_text, re.DOTALL)
    if cleaned_json:
        try:
            new_mapping = json.loads(cleaned_json.group(0))
        except json.JSONDecodeError as e:
            print("Lỗi khi parse JSON:", e)
            print("Nội dung JSON thô từ API:\n", cleaned_json.group(0))
            return
    else:
        print("Không tìm thấy nội dung JSON hợp lệ từ API.")
        return
    
    update_object_mapping(mapping_path, object_name, new_mapping)

if __name__ == "__main__":
    main("mbbank")
