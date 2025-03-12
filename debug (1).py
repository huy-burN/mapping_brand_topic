from typing import List, Dict, Any
import json
import re
import hashlib
from underthesea import word_tokenize

class GeminiClient():
    def __init__(self):
        self.input_token_price = 0.1
        self.output_token_price = 0.4
        self.dollar_exchange_rate = 25000

        self.stop_words = set(
            [
                # Các nguyên âm có dấu
                "a",
                "à",
                "ả",
                "ã",
                "ạ",
                "ă",
                "ắ",
                "ằ",
                "ẳ",
                "ẵ",
                "ặ",
                "â",
                "ấ",
                "ầ",
                "ẩ",
                "ẫ",
                "ậ",
                # Các từ nối và từ chức năng
                "bản_thân",
                "bao",
                "bấy",
                "bởi",
                "bởi_vì",
                "các",
                "cái",
                "cả",
                "càng",
                "chỉ",
                "cho",
                "chứ",
                "chưa",
                "chuyện",
                "cứ",
                "do",
                "dẫu",
                "dù",
                "dĩ",
                # Đại từ, giới từ và trạng từ thông dụng
                "đang",
                "đâu",
                "đều",
                "điều",
                "đó",
                "đấy",
                "đến",
                "gì",
                "ha",
                "hơi",
                "hay",
                "hơn",
                "hoặc",
                "hết",
                # Từ chung, từ chỉ định thời gian, không gian, số lượng
                "là",
                "lại",
                "lên",
                "lúc",
                "mà",
                "mấy",
                "mỗi",
                "mới",
                "này",
                "nên",
                "nếu",
                "nữa",
                "rất",
                "sau",
                "sẽ",
                "siêu",
                "so",
                "sự",
                "tại",
                "theo",
                "thì",
                "thôi",
                "trên",
                "trong",
                "trước",
                "và",
                "vẫn",
                "vào",
                "vậy",
                "vì",
                "với",
                # Một số từ khác thường xuất hiện không mang nhiều ý nghĩa riêng
                "như",
                "khi",
                "đấy",
                "đó",
            ]
        )

        self.short_words = {
            "nội dung bài viết": "S_ndbv",
            "nhãn hàng": "S_nh",
        }
        self.field_config = self.get_field_config()
        self.sentiment_mapping = self.field_config["sentiment_score"]["mapping"]

        self.reverse_mapping_by_short = {
            config["short"]: key for key, config in self.field_config.items()
        }

        self.explain_field_from_db = {
            "content_from_name": "tên người đăng bài",
            "object_name": "Tên của nhãn hàng",
            "message": "nội dung bài viết",
        }
        
    def get_field_config(self):
        with open("field_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config

    def get_sentiment(self, sentiment_value: float) -> str:
        for range_str, description in self.sentiment_mapping.items():
            low_str, high_str = range_str.split("->")
            low, high = float(low_str.strip()), float(high_str.strip())
            if low <= sentiment_value <= high:
                return description.strip()
        return "Không xác định"

    def hash_content(self, content: str) -> str:
        return hashlib.sha256(content.strip().encode()).hexdigest()

    def remove_blank_space(self, text):
        return re.sub(r"\s+", " ", text).replace("\n", " ").strip()

    def clean_text(self, text):
        text = self.remove_blank_space(text)
        text = re.sub(r"([!?.,;:])\1+", r"\1", text)
        tokens = word_tokenize(text, format="text").split()
        filtered_tokens = [
            token for token in tokens if token.lower() not in self.stop_words
        ]
        cleaned_text = " ".join(filtered_tokens)
        cleaned_text = re.sub(r"((-\s*){2,})", "", text)
        return cleaned_text

    def extract_analysed_response(self, text: str):
        return (
            self.remove_blank_space(text.strip("```json\n").strip("```"))
            .replace("\n", "")
            .replace('""', '"')
        )

    def estimate_cost(self, input_usage):
        input_token = input_usage["prompt_token_count"]
        output_token = input_usage["candidates_token_count"]

        input_cost = (input_token / 1000000) * self.input_token_price
        output_cost = (output_token / 1000000) * self.output_token_price
        total_dollar = input_cost + output_cost
        total_vnd = total_dollar * self.dollar_exchange_rate
        return {
            "input_token": input_token,
            "output_token": output_token,
            "input_cost_in_dollar": f"{input_cost:.6f}",
            "output_cost_in_dollar": f"{output_cost:.6f}",
            "total_dollar": f"{total_dollar:.6f}",
            "total_vnd": f"{total_vnd:.3f}",
        }

    def get_require_input_fields(self, output_fields):
        require_input_fields = []
        for field_name in output_fields:
            field_config = self.field_config.get(field_name, None)
            if field_config is None:
                raise Exception(
                    (
                        "[ERROR][GEMINI CLIENT] field config not found: "
                        f"{field_name}"
                    )
                )
            require_input_fields += field_config["input_required"]
        return tuple(set(require_input_fields))

    def analyze_batch(
        self,
        news_items: List,
        model_name: str,
        prompt_template: str,
        module_configs: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        # build field name explain
        profession = module_configs.get("profession", "")
        require_output_fields = module_configs.get("require_output_fields", [])
        require_input_fields = self.get_require_input_fields(
            require_output_fields
        )
        field_name_explain_text = ""
        field_name_order_list = []
        for field in require_input_fields:
            field_name_explain_text += (
                "                - "
                f"{field}: {self.explain_field_from_db[field]}\n"
            )
            field_name_order_list.append(field)
        field_name_order_text = "|".join(field_name_order_list)

        # build input data in text format
        id_mapping = {}
        final_result_mapping = {}
        filtered_data_list = []
        for i, item in enumerate(news_items):
            item_keys = list(item.keys())
            missing_keys = set(require_input_fields) - set(item_keys)
            if missing_keys:
                raise Exception(f"Fields missing: {missing_keys}")

            id_int = i + 1
            id_mapping[id_int] = {
                "news_id": item["news_id"],
                "message": item["message"],
                "object_id": str(item["object_id"]),
            }
            final_result_mapping[item["news_id"]] = {
                "news_id": item["news_id"],
                "message": item["message"],
                "object_id": str(item["object_id"]),
                # "doc_type": item["doc_type"],
            }
            filtered_data_list.append(
                (
                    f"{id_int}|{item['content_from_name']}|"
                    f"{self.clean_text(item['message'])}|"
                    f"{item['object_name']}"
                )
            )
        filtered_data_text = " || ".join(filtered_data_list)

        # build output json format
        final_json_format = """
"total_post": // mảng chứa các object là kết quả đã phân tích của mỗi bài viết
[{
    id: string // ID bài viết
"""
        for field_name in require_output_fields:
            if not self.field_config[field_name]["active"]:
                continue
            final_json_format += (
                f'    {self.field_config[field_name]["short"]}: '
                f'{self.field_config[field_name]["type"]} // '
                f'{self.field_config[field_name]["definition"]}'
            )
            if self.field_config[field_name]["mapping"]:
                final_json_format += ". Kết quả theo quy tắc sau: "
                for key in self.field_config[field_name]["mapping"]:
                    final_json_format += (
                        f"{key}: "
                        f'{self.field_config[field_name]["mapping"][key]} | '
                    )
            final_json_format += "\n"
        final_json_format += "}]"

        final_prompt = self._format_prompt(
            prompt_template,
            profession,
            filtered_data_text,
            final_json_format,
            field_name_explain_text,
            field_name_order_text,
        )

        print("**********************************************")
        print(final_prompt)
        print("**********************************************")
        print()
        return final_prompt
        
    def _format_prompt(
        self,
        prompt_template: str,
        profession: str,
        filtered_data_text: str,
        json_format: str,
        field_name_explain_text: str,
        field_name_order_text: str,
    ) -> str:
        final_prompt = prompt_template.replace(
            "prompt_config_profession", profession
        )
        final_prompt = final_prompt.replace(
            "prompt_config_filtered_data_text", filtered_data_text
        )
        final_prompt = final_prompt.replace(
            "prompt_config_json_format", json_format
        )
        final_prompt = final_prompt.replace(
            "prompt_config_field_name_explain_text", field_name_explain_text
        )
        final_prompt = final_prompt.replace(
            "prompt_config_field_name_order_text", field_name_order_text
        )
        return final_prompt

    def _parse_response(
        self, response: Any, id_mapping: dict, require_output_fields: list
    ) -> Dict[str, Any]:
        final_data = []
        # TODO change package to get total used token
        # print(response.__dict__)
        # estimate_cost = self.estimate_cost()

        raw_analysed_text = self.extract_analysed_response(response.text)
        json_data = json.loads(raw_analysed_text)
        # print(">>>>>>>>>> json_data", json_data)
        total_post = json_data["total_post"]
        for item in total_post:
            result = {}
            result["news_id"] = id_mapping[int(item["id"])]["news_id"]
            result["message"] = id_mapping[int(item["id"])]["message"]
            result["object_id"] = id_mapping[int(item["id"])]["object_id"]
            result["analysis"] = {}
            result["status"] = "ok"
            try:
                for field_name in self.field_config:
                    # print(">>>>>>>>>> field_name", field_name)
                    short_field_name = self.field_config[field_name]["short"]
                    result["analysis"][field_name] = item.get(short_field_name, None)
                    if field_name in require_output_fields and result["analysis"][field_name] is None:
                        result["error"] = "Data for require_output_fields is missing"
                        result["status"] = "fail"
                # print(">>>>>>>>>> result", result)
            except Exception as err:
                result["error"] = str(err)
                result["status"] = "fail"

            final_data.append(result)
        return final_data






# ---------------- Start ----------------
news = [
    # {
    #   "news_id": "10586_11535_0_100003816695541_3538174789653043",
    #   "message": "🍃Đẹp quá không thể cưỡng lại sức hút của Quy Nhơn nên e lên tiếp cho các bác combo Quy Nhơn bay #Bamboo ở kết hợp Crown Retreat ăn 2 bữa 🎁 4N3Đ chỉ #4x99k/người! Zá này không đẹp thì zá nào đẹp\n\nBao gồm: \n▪️Vé máy bay khứ hồi \n▪️01 đêm Crown Retreat - Quy Nhơn triệu góc sống ảo + Ăn 2 bữa + Bể Bơi \n▪️02 đêm FLC Sea Tower Quy Nhơn + Phòng view biển\n▪️Trà nước cf, tiện ích phòng",
    #   "object_id": 11535,
    #   "object_name": "Vincom",
    #   "content_from_name": "Huyền Diamond FLC Group",
    #   "page_name": "Huyền Diamond",
    #   "brand_id": 10586,
    #   "brand_name": "Property",
    #   "created": 1741054701
    # },
    {
      "news_id": "10586_11535_0_588844503184094_1008933217841885",
      "message": "Thích làm việc với flc group ! Không như Vincom thấy chán",
      "object_id": 11535,
      "object_name": "Vincom",
      "content_from_name": "Hà Ngô",
      "page_name": "Hà Ngô",
      "brand_id": 10586,
      "brand_name": "Property",
      "created": 1741054689
    }
]

prompt_template = """
-- Đóng vai là chuyên gia phân tích hoạt động truyền thông của các doanh nghiệp ngành prompt_config_profession.
-- Định dạng dữ liệu dùng cho phân tích:
prompt_config_field_name_explain_text
-- Dưới đây là các bài báo cần phân tích, phân cách bởi dấu '||' và mỗi bài có ID riêng, với định dạng mỗi bài truyền vào là (ID|prompt_config_field_name_order_text)
prompt_config_filtered_data_text
-- Yêu cầu phân tích:
- Phân tích kỹ nội dung của từng bài báo dựa vào các trường content và object.
- Mỗi bài báo được nhận diện bởi ID duy nhất và chỉ có 1 kết quả phân tích duy nhất.
- Kết quả phân tích của mỗi bài báo chỉ bao gồm các trường sau:
prompt_config_json_format
-- Kết quả trả về phải theo định dạng JSON trong yêu cầu phân tích, nằm trên 1 dòng duy nhất (không có văn bản bổ sung hay mô tả nào khác ngoài JSON)
-- Lưu ý:
+ Đảm bảo số lượng đối tượng trong "total_data" bằng đúng số bài báo đầu vào.
+ Giá trị của trường sc và các giá trị % (nếu có) phải nằm trong khoảng từ 0 đến 1.
+ Trả về các kết quả với độ tự tin (chắn chắn) trong suy luận là cao nhất
            """

module_configs= {
    "profession": "bất động sản",
    "require_output_fields": [
        "sentiment_score",
        "tag",
        "topic",
        "relation_score",
        "value_score",
        "summary",
        "explain",
        "info_source_id",
        "predict_info_source_id",
        "language",
        "service_id",
        "attribute",
        "sub_brand",
        "spam_filter",
        "confidence_score",
    ],
}

cls_ = GeminiClient()
final_prompt = cls_.analyze_batch(news, "gemini-2", prompt_template, module_configs)

from google import genai
client = genai.Client(api_key="AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=final_prompt,
)
data = response.model_dump()
pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
print(pretty_json)