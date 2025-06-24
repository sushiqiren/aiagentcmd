import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Generate content using gemini-2.0-flash-001
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)

# Print the response text
print(response.text)

# Print token usage information
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")