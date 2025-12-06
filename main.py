import os
from dotenv import load_dotenv
from google import genai

api_key_name = "GEMINI_API_KEY"

def main():
    load_dotenv()
    api_key = os.environ.get(api_key_name)
    if api_key is None:
        raise RuntimeError(f"API key not found! Is there a '.env' file with a value for the '{api_key_name}' key?")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(response.text)


if __name__ == "__main__":
    main()
