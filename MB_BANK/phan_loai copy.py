
import json
import pandas as pd
import random
import pathlib
import requests
import textwrap
import google.generativeai as genai
#moiAIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk

from google import genai

# Khởi tạo client
client = genai.Client(api_key="#moiAIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk")

while True:
    user_input = input("Nhập câu hỏi của bạn (hoặc nhập 'exit' để thoát): ")
    if user_input.lower() == 'exit':
        break
    
    response = client.models.generate(
        model="gemini-2.0-flash",
        prompt=user_input,
    )
    
    # Trích xuất nội dung trả lời từ model
    try:
        text_response = response.candidates[0].content.parts[0].text.strip()
        print("Bot:", text_response)
    except (IndexError, AttributeError, KeyError):
        print("Bot: Không thể lấy phản hồi hợp lệ.")

