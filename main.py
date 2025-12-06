import os
from dotenv import load_dotenv

api_key_name = "GEMINI_API_KEY"

def main():
    load_dotenv()
    api_key = os.environ.get(api_key_name)
    if api_key is None:
        raise RuntimeError(f"API key not found! Is there a '.env' file with a value for the '{api_key_name}' key?")


if __name__ == "__main__":
    main()
