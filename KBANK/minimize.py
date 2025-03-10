# minimize.py
import re
import emoji
import string
from typing import List

from underthesea import word_tokenize

def process_vietnamese_text(text: str) -> str:
    """Xử lý text tiếng Việt với underthesea"""
    # Tách từ tiếng Việt
    words = word_tokenize(text)
    return ' '.join(words)

def load_stopwords(file_path: str = 'stopwords.txt') -> List[str]:
    """Load stopwords từ file txt"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = set(line.strip() for line in f)
        return stopwords
    except FileNotFoundError:
        print(f"Không tìm thấy file {file_path}")
        return set()

def remove_emoji(text: str) -> str:
    """Loại bỏ emoji từ text"""
    return emoji.replace_emoji(text, '')

def remove_email(text: str) -> str:
    """Loại bỏ địa chỉ email"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, '', text)

def remove_phone_numbers(text: str) -> str:
    """Loại bỏ số điện thoại"""
    # Pattern cho số điện thoại Việt Nam
    phone_pattern = r'(?:(?:\+|0{0,2})84|0)[35789](?:\d{8}|\d{9})'
    return re.sub(phone_pattern, '', text)

def remove_punctuation(text: str) -> str:
    """Loại bỏ dấu câu"""
    # Tạo translation table để loại bỏ punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_extra_spaces(text: str) -> str:
    """Loại bỏ khoảng trắng thừa"""
    return ' '.join(text.split())

def remove_urls(text: str) -> str:
    """Loại bỏ URLs"""
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def remove_special_characters(text: str) -> str:
    """Loại bỏ ký tự đặc biệt"""
    return re.sub(r'[^\w\s]', '', text)

def remove_numbers(text: str) -> str:
    """Loại bỏ số"""
    return re.sub(r'\d+', '', text)

def remove_stopwords(text: str, stopwords: set) -> str:
    """Loại bỏ stopwords"""
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def process_text(text: str = None) -> str:
    """Hàm xử lý chính"""
    if text is None:
        text = "Đây là văn bản mẫu cần được xử lý"
    
    # Load stopwords
    stopwords = load_stopwords('stopwords.txt')
    
    # Chuyển text về lowercase
    text = text.lower()
    
    # Thực hiện các bước xử lý
    text = remove_emoji(text)
    text = remove_email(text)
    text = remove_phone_numbers(text)
    text = remove_urls(text)
    text = remove_special_characters(text)
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = remove_extra_spaces(text)
    text = remove_stopwords(text, stopwords)
    
    return text

def get_minimized_result(input_text: str = None) -> str:
    """Hàm trả về kết quả đã được xử lý"""
    result = process_text(input_text)
    return result

# Ví dụ sử dụng
if __name__ == "__main__":
    test_text = """
    Xin chào! 😊 
    Đây là email của tôi: example@email.com
    Số điện thoại: 0912345678
    Website: https://example.com
    Giá sản phẩm là 1000$ !!!
    """
    
    cleaned_text = get_minimized_result(test_text)
    print("Text gốc:")
    print(test_text)
    print("\nText sau khi xử lý:")
    print(cleaned_text)