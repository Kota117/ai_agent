import os
import argparse

from dotenv import load_dotenv
from google import genai

from prompts import system_prompt
from functions.gather_schemas import available_functions

api_key_name = "GEMINI_API_KEY"

def main():
    # Use argparse to get command line argument(s)
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Load API key
    load_dotenv()
    api_key = os.environ.get(api_key_name)
    if api_key is None:
        raise RuntimeError(f"Environment variable '{api_key_name}' not found! Check for a '.env' file with a value for the '{api_key_name}' key.")

    # Initialize Client
    client = genai.Client(api_key=api_key)

    # Initialize conversation history with user prompt
    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)])]

    # Optionally print User prompt
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    # API request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    # Ensure request didn't fail
    if not response.usage_metadata:
        raise RuntimeError("GenerateContentObject 'response' has no 'usage_metadata' property. Likely a failed API request.")

    # Optionally print request data
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Print response innformation
    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return None
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    return None


if __name__ == "__main__":
    main()
