import os
import argparse

from dotenv import load_dotenv
from google import genai

from call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_ITERATIONS

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
    
    # Allow generate_content to run several times
    iterations = 0
    while True:
        if iterations >= MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            break

        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print(f"Final Response:\n{final_response}")
                break
            iterations += 1
        except Exception as e:
            print(f"Error in generate_content: {e}")


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
    
    # Add response candidates information to messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Return response information
    if not response.function_calls:
        return response.text
    
    # Create function responses to append to messages
    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
    
    messages.append(genai.types.Content(role="user", parts=function_responses))
    
    return None


if __name__ == "__main__":
    main()
