import os
from google.genai import types

def write_file(working_directory, file_path, content):
     # Convert working_directory to absolute path
    abs_working_dir = os.path.abspath(working_directory)
    
    # Join with working_directory to handle relative paths
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file is outside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
        # Write the content to the file
        with open(abs_file_path, 'w') as file:
            file.write(content)
        
        # Return success message
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
    
# Function declaration for write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)