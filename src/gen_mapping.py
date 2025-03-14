import os
import json
import google.generativeai as genai

# Load field mapping từ fields.json
def read_field(json_file, field):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get(field, None)
    except Exception as e:
        print(f"Lỗi khi đọc file {json_file}: {e}")
        return None

# Kiểm tra object có tồn tại trong object_mapping.json không
def check_object_exists(json_file, object_name):
    if not os.path.exists(json_file):
        return False  # Nếu file chưa tồn tại, chắc chắn object chưa có

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return object_name in data
    except Exception as e:
        print(f"Lỗi khi đọc file {json_file}: {e}")
        return False

# Xử lý response từ Gemini API
def clean_json_response(response_text):
    content = response_text.strip()
    if content.startswith("```json"):
        content = content[7:]  # Remove "```json\n"
    if content.endswith("```"):
        content = content[:-3]  # Remove "\n```"
    return content

# Gọi Gemini API để tạo mapping mới
def generate_custom_topics(api_key, field_mapping, object_name,def_object):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Đây là các dạng thông tin có liên quan tới 1 lĩnh vực được chia làm hai loại,
    loại thứ nhất là các key bên trên dòng key "###" là SPAM: các thông tin không có ý nghĩa ảnh hưởng tới nhãn hàng hoặc doanh nghiệp
    loại thứ hai là các key bên dưới dòng key "###" là NONSPAM: các thông tin có ảnh hưởng  
    {json.dumps(field_mapping, indent=2, ensure_ascii=False)},
    hãy phát triển các dạng thông tin tương tự cụ thể cho đối tượng {object_name} có định nghĩa là {def_object}
    Đầu ra là dạng JSON, các key và định nghĩa cũng được trình bày giống bộ mapping lĩnh vực, ngăn cách 2 loại bằng key "###" để dễ nhận biết.
    """

    response = model.generate_content(prompt)
    cleaned_content = clean_json_response(response.text)

    try:
        return json.loads(cleaned_content)
    except Exception as e:
        print("Lỗi khi parse JSON từ phản hồi:", e)
        print("Nội dung trả về:", cleaned_content)
        return None

# Lưu dữ liệu vào object_mapping.json (thêm mới mà không ghi đè)
def save_to_json(data, json_file, object_name):
    # Nếu file chưa tồn tại, tạo file mới
    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=2, ensure_ascii=False)

    # Đọc dữ liệu hiện có
    with open(json_file, "r", encoding="utf-8") as file:
        existing_data = json.load(file)

    # Thêm object mới vào
    existing_data[object_name] = data

    # Ghi lại file với dữ liệu mới
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=2, ensure_ascii=False)

# Hàm chính
def main(object_name, field):
    fields_json = "src/fields_mapping.json"
    objects_json = "src/object_mapping.json"  # File lưu object mapping
    api_key = "AIzaSyAthx0l3RraNbsFabULK3vAibm5usY-i6A"  # Thay bằng API key thực tế
    def_object = ''

    # Kiểm tra field có tồn tại trong fields.json không
    field_mapping = read_field(fields_json, field)
    if field_mapping is None:
        print(f"Chưa có field_mapping cho {field}")
        return

    # Kiểm tra object đã có trong object_mapping.json chưa
    if check_object_exists(objects_json, object_name):
        print("Object đã có mapping")
        return

    # Gọi API để tạo custom mapping nếu chưa có
    custom_topics = generate_custom_topics(api_key, field_mapping, object_name, def_object)
    if custom_topics is None:
        print("Không tạo được chủ đề tùy chỉnh.")
        return

    # Lưu vào object_mapping.json (thêm mới mà không ghi đè)
    save_to_json(custom_topics, objects_json, object_name)
    print(f"Bộ chủ đề cho {object_name} đã được lưu vào {objects_json}")

# Chạy chương trình
if __name__ == "__main__":
    object_name = input("Nhập tên đối tượng: ")
    field = input("Nhập lĩnh vực: ")
    main(object_name, field)
