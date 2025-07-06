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

def call_function(function_call_part, verbose=False):
    # Get the function name
    func_name = function_call_part.name
    
    # Get the arguments
    func_args = function_call_part.args

    # Set the working directory
    working_directory = "./calculator"
    
    # Print info based on verbosity level
    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    try:
        # Dispatch to the correct function based on name
        if func_name == "get_files_info":
            from functions.get_files_info import get_files_info
            function_result = get_files_info(working_directory, **func_args)
        
        elif func_name == "get_file_content":
            from functions.get_file_content import get_file_content
            function_result = get_file_content(working_directory, **func_args)
        
        elif func_name == "write_file":
            from functions.write_file import write_file
            function_result = write_file(working_directory, **func_args)
        
        elif func_name == "run_python_file":
            from functions.run_python import run_python_file
            function_result = run_python_file(working_directory, **func_args)
        
        else:
            return f"Error: Unknown function '{func_name}'"
        
        if verbose:
            print(f"-> {{'result': {function_result}}}")
            
        return function_result
        
    except Exception as e:
        error_message = f"Error executing function: {str(e)}"
        if verbose:
            print(f"-> {{'error': {error_message}}}")
        return error_message

# Define max iterations to prevent infinite loops
MAX_ITERATIONS = 20

# Initialize a flag to track if we're done
done = False
iterations = 0

# Start the conversation loop
while not done and iterations < MAX_ITERATIONS:
    iterations += 1
    
    if verbose:
        print(f"\n--- Iteration {iterations} ---")
    
    # Generate content using the current messages
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )
    
    # Track if a function was called in this iteration
    function_called = False
    
    # Process all candidates
    if hasattr(response, 'candidates') and response.candidates:
        # Add each candidate's content to our messages
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and candidate.content:
                # Process the parts in this candidate
                if hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            # Function call detected
                            function_call_part = part.function_call
                            
                            if hasattr(function_call_part, 'name') and hasattr(function_call_part, 'args'):
                                # Call the function
                                function_result = call_function(function_call_part, verbose)
                                function_called = True
                                
                                # Print the result
                                if verbose:
                                    print(f"Result: {function_result}")
                                else:
                                    print(f"Result of {function_call_part.name}: {function_result}")
                                
                                # Add the function call to messages
                                messages.append(candidate.content)
                                
                                # Add a message with the function result
                                function_response = types.Content(
                                    role="user",  # Using 'user' role avoids the API error
                                    parts=[types.Part(text=f"Function {function_call_part.name} returned: {function_result}")]
                                )
                                messages.append(function_response)
                            else:
                                print("Function call detected but missing name or args:", function_call_part)
                        elif hasattr(part, 'text') and part.text.strip():
                            # Text response
                            print(part.text)
                            # Don't add text parts individually as we already added the whole content
    
    # If no function was called in this iteration, we're done
    if not function_called:
        done = True
        # Print the final response
        if hasattr(response, 'text'):
            print("\nFinal response:")
            print(response.text)
    
    # Print token usage if in verbose mode
    if verbose:
        if hasattr(response, 'usage_metadata'):
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# Report if we hit the max iterations
if iterations >= MAX_ITERATIONS:
    print(f"\nReached maximum number of iterations ({MAX_ITERATIONS}).")
