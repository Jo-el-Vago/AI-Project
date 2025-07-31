import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_cont import schema_get_files_cont
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = api_key)
parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument("--verbose", action='store_true')
args = parser.parse_args()

user_prompt = args.prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_cont,
        schema_run_python,
        schema_write_file,

    ]
)


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

response = client.models.generate_content(
    model = 'gemini-2.0-flash-001',
    contents= messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt,
                                       tools=[available_functions]),
    )
if response.function_calls:
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")
else:    
    print(response.text)

if args.verbose:
    print (f"User prompt: {args.prompt}")
    print (f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print (f"Response tokens: {response.usage_metadata.candidates_token_count}")
