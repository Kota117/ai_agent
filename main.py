import os
from dotenv import load_dotenv
from google import genai

api_key_name = "GEMINI_API_KEY"

def main():
    # Load API key
    load_dotenv()
    api_key = os.environ.get(api_key_name)
    if api_key is None:
        raise RuntimeError(f"API key not found! Is there a '.env' file with a value for the '{api_key_name}' key?")

    # Initialize Client
    client = genai.Client(api_key=api_key)

    # Hardcoded prompt
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    
    # API request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Ensure request didn't fail
    if response.usage_metadata is None:
        raise RuntimeError("GenerateContentObject 'response' has no 'usage_metadata' property. Likely a failed API request.")

    # Print request data
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")

    return None


if __name__ == "__main__":
    main()
