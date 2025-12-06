import os
import argparse
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

    # Use argparse to get the prompt as a command line argument
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # Initialize conversation history with user prompt
    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)])]
    
    # API request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    # Ensure request didn't fail
    if response.usage_metadata is None:
        raise RuntimeError("GenerateContentObject 'response' has no 'usage_metadata' property. Likely a failed API request.")

    # Print request data
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")

    return None


if __name__ == "__main__":
    main()
