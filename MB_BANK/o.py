import pandas as pd
import random

def get_random_message_from_excel(file_path):
    try:
        # Đọc file Excel, chỉ định sheet_name là 'SPAM'
        df = pd.read_excel(file_path, sheet_name='SPam')
        
        # Kiểm tra xem cột 'MESSAGE' có tồn tại không
        if 'MESSAGE' not in df.columns:
            return "Không tìm thấy cột MESSAGE trong file Excel"
        
        # Lấy số lượng hàng trong DataFrame
        total_rows = len(df)
        
        # Chọn một số ngẫu nhiên từ 0 đến tổng số hàng
        random_row = random.randint(0, total_rows-1)
        
        # Lấy giá trị từ cột MESSAGE tại hàng ngẫu nhiên
        random_message = df['MESSAGE'].iloc[random_row]
        
        return random_message
    
    except FileNotFoundError:
        return "Không tìm thấy file Excel"
    except Exception as e:
        return f"Có lỗi xảy ra: {str(e)}"

'''# Sử dụng hàm
file_path = r'C:/Users/admin/Downloads/AI_Data_MBBANK.xlsx' 
message = get_random_message_from_excel(file_path)'''
