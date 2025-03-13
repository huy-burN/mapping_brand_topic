from google import genai
#AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk



client = genai.Client(api_key="AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=""
)
print(response.text)