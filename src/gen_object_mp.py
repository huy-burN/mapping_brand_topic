import os
import json
import google.generativeai as genai

def load_mapping(folder_path):
    """Load all field mappings from the given folder."""
    mappings = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            field_name = filename.replace(".json", "")
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                mappings[field_name] = json.load(file)
    return mappings

def get_field_mapping(mappings, field):
    """Retrieve the mapping for a given field."""
    return mappings.get(field, None)

def clean_json_response(response_text):
    """Clean Gemini API response by removing markdown code block if present."""
    content = response_text.strip()
    if content.startswith("```json"):
        content = content[7:]  # Remove "```json\n"
    if content.endswith("```"):
        content = content[:-3]  # Remove "\n```"
    return content

def generate_custom_topics(api_key, field_topics, entity_name):
    """
    Use Gemini API to generate custom topics for a given entity based on field_topics.
    """
    # Configure API key for Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
Dựa trên bộ chủ đề sau đây của lĩnh vực:
{json.dumps(field_topics, indent=2, ensure_ascii=False)}
Hãy tạo một bộ chủ đề mới dành riêng cho {entity_name} theo định dạng JSON.
"""
    
    # Call Gemini API
    response = model.generate_content(prompt)
    cleaned_content = clean_json_response(response.text)
    
    try:
        return json.loads(cleaned_content)
    except Exception as e:
        print("Lỗi khi parse JSON từ phản hồi:", e)
        print("Nội dung trả về:", cleaned_content)
        return None

def save_to_json(data, output_file):
    """Save JSON data to a file."""
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main():
    folder_path = "src/fields_mapping"  # Directory containing JSON mappings
    api_key = "AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk"  # Replace with your Gemini API key
    
    entity_name = input("Nhập tên đối tượng: ")
    field = input("Nhập lĩnh vực: ")
    
    mappings = load_mapping(folder_path)
    field_topics = get_field_mapping(mappings, field)
    
    if not field_topics:
        print(f"Không tìm thấy mapping cho lĩnh vực: {field}")
        return
    
    custom_topics = generate_custom_topics(api_key, field_topics, entity_name)
    if custom_topics is None:
        print("Không tạo được chủ đề tùy chỉnh do lỗi khi gọi API hoặc parse kết quả.")
        return
    
    output_file = f"{entity_name}.json"
    if os.path.exists(output_file):
        print(f"File {output_file} đã tồn tại, không cần tạo lại.")
        return
    
    save_to_json(custom_topics, output_file)
    print(f"Bộ chủ đề dành riêng cho {entity_name} đã được lưu vào {output_file}")

if __name__ == "__main__":
    main()