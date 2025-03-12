import openai
import json
import concurrent.futures
import pandas as pd
import time
import random

class RateLimitHandler:
    def __init__(self, max_retries=5, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def wait_with_exponential_backoff(self, retry_count):
        """Implement exponential backoff with jitter"""
        delay = min(
            self.base_delay * (2 ** retry_count),  # Exponential backoff
            60  # Max wait time of 1 minute
        )
        jitter = random.uniform(0, 0.1 * delay)  # Add small random jitter
        wait_time = delay + jitter
        print(f"Waiting {wait_time:.2f} seconds before retry...")
        time.sleep(wait_time)

def classify_message_with_gpt(message, api_key):
    """Phân loại tin nhắn bằng GPT-4 với xử lý rate limit"""
    openai.api_key = api_key
    rate_limiter = RateLimitHandler()
    
    prompt = f"""Hãy phân tích nội dung tin nhắn sau và chọn 1 chủ đề phù hợp nhất từ danh sách mapping (1-36), sau đó chỉ trả về câu trả lời kết quả là 1 hoặc 0
    Nếu thông tin thuộc về chủ đề số <20 thì chỉ trả về số 1
    Nếu thông tin thuộc về chủ đề số >=20 thì chỉ trả về số 0
    
    Tin nhắn: "{message}"
    
   "1": "Tin rao vặt, địa điểm dịch vụ (không liên quan MB Bank): Rao vặt, địa điểm gần chi nhánh MB Bank, không liên quan sản phẩm/dịch vụ.",
    "2": "Vị trí gần MB Bank (không phải nội dung chính): Đề cập vị trí gần MB Bank, không phải nội dung chính về thương hiệu.",
    "3": "Minigame, quà tặng (không ảnh hưởng thương hiệu MB Bank): Minigame, quà tặng không liên quan MB Bank hoặc không ảnh hưởng hình ảnh.",
    "4": "Giáo dục, đào tạo (không liên quan dịch vụ MB Bank): Khóa học nhắc đến MB Bank nhưng không liên quan dịch vụ tài chính.",
    "5": "Thời trang, phụ kiện (không liên quan MB Bank): Sản phẩm thời trang nhắc đến MB Bank nhưng không liên quan thông điệp tài chính.",
    "6": "Ẩm thực (không ảnh hưởng thương hiệu MB Bank): Quảng cáo nhà hàng gần MB Bank, không ảnh hưởng thương hiệu.",
    "7": "Dịch vụ tiện ích (không phản ánh thương hiệu MB Bank): Dịch vụ tiện ích nhắc đến MB Bank nhưng không phản ánh giá trị thương hiệu.",
    "8": "Tuyển dụng (không phải MB Bank): Tuyển dụng ngành khác, nhắc đến MB Bank trong địa chỉ.",
    "9": "Y tế, sức khỏe (đề cập MB Bank theo địa điểm): Bài viết về y tế, bảo hiểm sức khỏe nhắc đến MB Bank theo địa điểm.",
    "10": "Sự kiện, giải trí (không liên quan tài chính MB Bank): Sự kiện văn hóa, giải trí không liên quan hình ảnh tài chính MB Bank.",
    "11": "Công nghệ (không liên quan tài chính MB Bank): Nhắc đến MB Bank trong bối cảnh công nghệ không liên quan tài chính.",
    "12": "Giải trí, văn hóa (không quảng bá MB Bank): Hoạt động nghệ thuật đề cập MB Bank nhưng không quảng bá thương hiệu.",
    "13": "Quảng cáo bất đồng (không ảnh hưởng MB Bank): Tranh cãi quảng cáo không ảnh hưởng hình ảnh MB Bank.",
    "14": "Nhầm lẫn thương hiệu (không nghiêm trọng): Nhầm lẫn MB Bank với thương hiệu khác, không ảnh hưởng nghiêm trọng.",
    "15": "Nội dung không rõ ràng, spam: Bài viết vô nghĩa, lỗi chính tả, không liên quan MB Bank.",
    "16": "Hoạt động xã hội bên thứ ba (nhắc đến MB Bank): Hoạt động từ thiện không do MB Bank tổ chức, nhắc đến tên.",
    "17": "Bán sản phẩm không liên quan (nhắc đến MB Bank): Bán sản phẩm không liên quan, nhắc đến MB Bank.",
    "18": "Cho thuê dịch vụ (không liên quan tài chính MB Bank): Dịch vụ thuê ngoài nhắc đến MB Bank, không liên quan hoạt động tài chính.",
    "19": "Nội dung ngoại ngữ (chứa từ khóa MB Bank): Nội dung tiếng nước ngoài chứa từ khóa MB Bank, không liên quan thương hiệu.",

    "20": "Báo cáo tài chính, định kỳ MB Bank: Báo cáo tài chính, kết quả kinh doanh MB Bank (MBB: HOSE), ảnh hưởng đến đánh giá nhà đầu tư.",
    "21": "Thị trường chứng khoán (liên quan MBB: HOSE): Tin tức chứng khoán liên quan cổ phiếu MBB, ảnh hưởng uy tín tài chính MB Bank.",
    "22": "Tuyển dụng MB Bank: Thông tin tuyển dụng của MB Bank, ảnh hưởng thương hiệu tuyển dụng.",
    "23": "Mời mở thẻ/sản phẩm MB Bank (nhân viên/môi giới): Nhân viên/môi giới MB Bank mời mở thẻ/gói tài khoản/vay vốn, ảnh hưởng hình ảnh dịch vụ.",
    "24": "MB Bank bị phạt, kiện tụng: Thông tin MB Bank bị phạt, kiện tụng, ảnh hưởng tiêu cực đến thương hiệu.",
    "25": "Sự cố bảo mật, rò rỉ dữ liệu MB Bank: Sự cố bảo mật, rò rỉ dữ liệu khách hàng MB Bank, ảnh hưởng niềm tin khách hàng.",
    "26": "Lãnh đạo MB Bank bị bắt, từ chức: Tin tức về lãnh đạo MB Bank (như ông Lưu Trung Thái) bị bắt, từ chức, ảnh hưởng nghiêm trọng thương hiệu.",
    "27": "MB Bank vướng bê bối tài chính: MB Bank liên quan rửa tiền, gian lận, lừa đảo, ảnh hưởng nghiêm trọng danh tiếng.",
    "28": "Khiếu nại, biểu tình về dịch vụ MB Bank: Khách hàng khiếu nại, biểu tình về dịch vụ MB Bank, ảnh hưởng lòng tin khách hàng.",
    "29": "Sập hệ thống, sự cố kỹ thuật MB Bank: Sập hệ thống thanh toán/ứng dụng MB Bank, sự cố kỹ thuật, ảnh hưởng uy tín.",
    "30": "Quảng cáo đối thủ cạnh tranh (ảnh hưởng MB Bank): Quảng cáo sản phẩm tài chính đối thủ cạnh tranh, ảnh hưởng hình ảnh/thị phần MB Bank."
    "31": "Chính sách, quy định của MB Bank: Thông tin về thay đổi chính sách, điều khoản dịch vụ, lãi suất, phí giao dịch... của MB Bank. Những thay đổi này ảnh hưởng trực tiếp đến khách hàng và cần được theo dõi."
    "32": "Tin tức về hoạt động kinh doanh, hợp tác, đầu tư của MB Bank: Ví dụ: MB Bank mở chi nhánh mới, hợp tác với đối tác chiến lược, đầu tư vào lĩnh vực mới... Những thông tin này phản ánh tình hình phát triển và định hướng của ngân hàng."
    "33": "Đánh giá, so sánh sản phẩm/dịch vụ của MB Bank với đối thủ: Bài viết so sánh lãi suất, ưu nhược điểm của sản phẩm MB Bank với các ngân hàng khác. Thông tin này ảnh hưởng đến quyết định lựa chọn của khách hàng."
    "34": "Thảo luận về trải nghiệm khách hàng với MB Bank (trên diễn đàn, mạng xã hội): Ý kiến, phản hồi của khách hàng về dịch vụ, ứng dụng, chất lượng phục vụ của MB Bank. Đây là nguồn thông tin quan trọng để đánh giá mức độ hài lòng của khách hàng."
    "35": "Thông tin khuyến mại, ưu đãi của MB Bank: Các chương trình giảm giá, hoàn tiền, quà tặng khi sử dụng dịch vụ của MB Bank. (Tách riêng với mục 3 - Minigame, quà tặng vì mục này tập trung vào khuyến mại liên quan trực tiếp đến sản phẩm/dịch vụ)."
    "36": "Tin tức về công nghệ, ứng dụng mới của MB Bank: Ví dụ: MB Bank ra mắt tính năng mới trên app MBBank, áp dụng công nghệ AI vào dịch vụ... Những thông tin này thể hiện sự đổi mới và nỗ lực cải thiện dịch vụ của ngân hàng."

    """
    
    for attempt in range(rate_limiter.max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Bạn là assistant phân tích và phân loại nội dung."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500  # Giới hạn token để giảm chi phí
            )
            return response.choices[0].message['content']
        
        except openai.error.RateLimitError as e:
            print(f"Rate limit error on attempt {attempt + 1}: {str(e)}")
            if attempt < rate_limiter.max_retries - 1:
                rate_limiter.wait_with_exponential_backoff(attempt)
            else:
                return f"Quá số lần thử lại. Lỗi: {str(e)}"
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"Có lỗi xảy ra: {str(e)}"

def analyze_messages(messages, api_key):
    """Phân tích nhiều tin nhắn với giới hạn đồng thời"""
    results = []
    # Giảm số lượng worker để tránh quá tải
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Thêm delay giữa các lô xử lý
        chunk_size = 5
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i:i+chunk_size]
            futures = [executor.submit(classify_message_with_gpt, message, api_key) for message in chunk]
            
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
            
            # Delay giữa các lô để tránh rate limit
            time.sleep(2)
    
    return results

def main(excel_path, api_key, sheet_name='test'):
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        messages = df['MESSAGE'].tolist()
        
        # Giới hạn số lượng tin nhắn để xử lý
        max_messages = 50
        messages = messages[:max_messages]
        
        results = analyze_messages(messages, api_key)
        
        print("\nKết quả phân loại:")
        for i, result in enumerate(results):
            print(f"Tin nhắn {i+1}:\n{result}\n")

    except FileNotFoundError:
        print(f"File Excel '{excel_path}' không tồn tại.")
    except KeyError:
        print(f"Sheet '{sheet_name}' hoặc cột 'Tin nhắn' không tồn tại trong file Excel.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

# Sử dụng hàm
excel_path = r'C:/Users/admin/Downloads/AI_Data_MBBANK.xlsx'
papipipey = ''
main(excel_path, api_key)