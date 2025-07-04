import os
from google.genai import types

def get_file_content(working_directory, file_path):
    # Convert working_directory to absolute path
    abs_working_dir = os.path.abspath(working_directory)
    
    # Join with working_directory to handle relative paths
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file is outside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the path is a valid regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read and return the file content
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read(10001)  # Read up to 10001 chars to check if file is longer
            
        # Check if the content needs to be truncated
        if len(content) > 10000:
            truncated_content = content[:10000]
            truncated_content += f"\n[...File \"{file_path}\" truncated at 10000 characters]"
            return truncated_content
        else:
            return content
            
    except Exception as e:
        return f"Error reading file: {e}"

# Function declaration for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)