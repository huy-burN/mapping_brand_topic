import gen_mapping, classification, update_mapping, delete_spam_message
import pandas as pd

def get_info(input_file):
    """
    Trích xuất thông tin từ file Excel.
    """
    df = pd.read_excel(input_file, sheet_name=None)
    
    # Lấy dữ liệu từ tab đầu tiên (giả sử tên sheet không cố định)
    sheet1 = list(df.keys())[0]
    info_df = df[sheet1]
    
    # Giả sử file có các cột: object, field, definition, keyword
    extracted_info = info_df[['object', 'field', 'definition', 'keyword']]
    
    return extracted_info

def main(input_excel):
    """
    Xử lý file Excel đầu vào và thực hiện các bước xử lý dữ liệu.
    """
    df = pd.read_excel(input_excel, sheet_name=None)
    
    # Lấy thông tin từ sheet đầu tiên
    sheet1 = list(df.keys())[0]
    info_df = df[sheet1]
    
    # Lấy thông tin từ sheet raw_data
    sheet2 = list(df.keys())[1]  # Giả sử sheet thứ hai chứa raw_data
    raw_data_df = df[sheet2]
    
    # Lưu ra file mới để chuẩn bị cho classification
    excel_path = "processed_data.xlsx"
    raw_data_df.to_excel(excel_path, index=False)
    
    # Trích xuất thông tin
    for _, row in info_df.iterrows():
        gen_mapping(row['object'], row['field'], row['definition'])
    
    # Thực hiện phân loại
    output_path = "classified_data.xlsx"
    api_key = "your_api_key_here"
    num_messages = len(raw_data_df)
    max_workers = 4
    nonsense_messages = classification(excel_path, output_path, api_key, num_messages, max_workers)
    
    # Xóa tin nhắn rác
    delete_spam_message(nonsense_messages)
    
if __name__ == "__main__":
    input_excel = "input_data.xlsx"
    main(input_excel)
