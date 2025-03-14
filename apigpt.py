from google import genai
#AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk



client = genai.Client(api_key="AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="""Trả về 0 hoặc 1 hoặc 2 và lời giải thích
     Định dạng phản hồi:
    {{"classification": 1 hoặc 0 hoặc 2, "explanation": "Giải thích về phân loại."}}

    Nếu tin nhắn thuộc chủ đề từ 1 đến 19, trả về 1.
- Nếu tin nhắn thuộc chủ đề từ 20 đến 36, trả về 0.
- Nếu tin nhắn không khớp với bất kỳ chủ đề nào, trả về 2.
    
    Tin nhắn: "
Gấp Gấp e cần bán 2 lô liền kề B03+04. mặt đg đôi quỳ xuyên, mb87 hoằng quỳ, ngay đầu đg ql1a đi vào. 
- dt 1 lô là: 150m2 ( rộng 7,5 x 20). hướng bắc.
- đối diện là khu công nghiệp phú quý 540ha.
- vị trí mb là cửa ngõ giao thông chính của KCN. kết nối 2 tuyến đg chính ql1a và ql10.
 giá bán nhanh: 2 tỷ 4xx/ lô. có ra lộc cho khách thiện chí mua.
☎lh e hoàn: 0979664404"
    
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
    
    
    Định dạng phản hồi:
    {{"classification": 1 hoặc 0 hoặc 2, "explanation": "Giải thích về phân loại."}}"""
)
print(response.text)