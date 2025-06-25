import os
import sys
from dotenv import load_dotenv
from google import genai

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

# Generate content using gemini-2.0-flash-001
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)

# Print the response text
print(response.text)

# Print token usage information
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")