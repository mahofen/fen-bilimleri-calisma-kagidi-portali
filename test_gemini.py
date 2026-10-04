import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

models_to_test = ["gemini-3.8-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash"]

for m in models_to_test:
    try:
        print(f"Testing model: {m}...")
        response = client.models.generate_content(
            model=m,
            contents="Lütfen sadece 'Bağlantı başarılı!' yaz.",
        )
        print(f"Başarılı! [{m}] -> {response.text.strip()}")
        break
    except Exception as e:
        print(f"Hata [{m}]: {e}")
