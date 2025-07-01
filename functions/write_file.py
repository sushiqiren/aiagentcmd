import os

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