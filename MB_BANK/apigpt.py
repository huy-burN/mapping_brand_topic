from google import genai

def classify_message_with_gemini(api_key):
    client = genai.Client(api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works"
    )
    print(response.text)

api_key = 'AIzaSyADwbsY0ZfoPv6eACowf1TXXl0RL49lTvk'
if __name__== '__main__':
    classify_message_with_gemini()