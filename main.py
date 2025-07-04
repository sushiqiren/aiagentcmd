import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Check if a prompt was provided as command line argument
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument")
    print("Example: python3 main.py \"Your prompt here\"")
    sys.exit(1)

# Use the command line argument as the prompt
prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
# Check for verbose flag
verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True

# Print user prompt if verbose mode is enabled
if verbose:
    print(f"User prompt: \"{prompt}\"")

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

# Generate content using gemini-2.0-flash-001
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    ),
)


# Handle the response
if hasattr(response.candidates[0].content, 'parts') and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'function_call') and part.function_call:
            # If this part is a function call
            function_call_part = part.function_call
            # Check if the function_call_part has the expected attributes
            if hasattr(function_call_part, 'name') and hasattr(function_call_part, 'args'):
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                
                # Here can handle the function call and execute the function
            else:
                print("Function call detected but missing name or args:", function_call_part)
        elif hasattr(part, 'text'):
            # Regular text response
            print(part.text)
        else:
            print("Unknown part type:", part)
else:
    # Fallback to just printing the text
    print(response.text)

# Print token usage information if verbose mode is enabled
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

