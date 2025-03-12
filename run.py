import os
import json
import openai
import fields_mapping

folder_path = fields_mapping

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

def generate_custom_topics(api_key, field_topics, entity_name):
    """Use OpenAI API to generate custom topics for a new entity based on field topics."""
    openai.api_key = api_key
    prompt = f"""
    Dựa trên bộ chủ đề sau đây của lĩnh vực:
    {json.dumps(field_topics, indent=2, ensure_ascii=False)}
    Hãy tạo một bộ chủ đề mới dành riêng cho {entity_name} theo định dạng JSON.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Đóng vai là chuyên gia phân tích dữ liệu xây dựng các báo cáo sức khỏe thương hiệu, báo cáo khủng hoảng, báo cáo truyền thông, báo cáo nghiên cứu người dùng, khách hàng"},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return json.loads(response["choices"][0]["message"]["content"])

def save_to_json(data, output_file):
    """Save the generated topics to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main():
    folder_path = "fields_mapping"  # Thư mục chứa các file JSON mapping
    api_key = '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'  # Thay thế bằng API key của bạn
    
    entity_name = input("Nhập tên đối tượng: ")
    field = input("Nhập lĩnh vực: ")
    
    mappings = load_mapping(folder_path)
    field_topics = get_field_mapping(mappings, field)
    
    if not field_topics:
        print(f"Không tìm thấy mapping cho lĩnh vực: {field}")
        return
    
    
    custom_topics = generate_custom_topics(api_key, field_topics, entity_name)
    output_file = f"{entity_name}.json"
    if os.path.exists(output_file):
        print(f"File {output_file} đã tồn tại, không cần tạo lại.")
        return
    
    save_to_json(custom_topics, output_file)
    
    print(f"Bộ chủ đề dành riêng cho {entity_name} đã được lưu vào {output_file}")

if __name__ == "__main__":
    main()