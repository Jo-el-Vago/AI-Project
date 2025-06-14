import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = api_key)
parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument("--verbose", action='store_true')
args = parser.parse_args()

user_prompt = args.prompt

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

response = client.models.generate_content(
    model = 'gemini-2.0-flash-001',
    contents= messages,

    )
print(response.text)

if args.verbose:
    print (f"User prompt: {args.prompt}")
    print (f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print (f"Response tokens: {response.usage_metadata.candidates_token_count}")
