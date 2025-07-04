import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    # Convert working_directory to absolute path
    abs_working_dir = os.path.abspath(working_directory)
    
    # Join with working_directory to handle relative paths
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the file is outside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file exists
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if the file is a Python file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Run the Python file and capture output with a 30-second timeout
        result = subprocess.run(
            ['python3', abs_file_path],
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
            timeout=30
        )
        
        # Format the output
        output_parts = []
        
        # Add stdout if present
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        
        # Add stderr if present
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        
        # Add exit code message if non-zero
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        # If no output was produced
        if not output_parts:
            return "No output produced."
        
        # Join all output parts with newlines between them
        return "\n\n".join(output_parts)
        
    except subprocess.TimeoutExpired:
        return f"Error: Execution of '{file_path}' timed out after 30 seconds"
    except Exception as e:
        return f"Error executing Python file: {str(e)}"


# Function declaration for run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. Must have a .py extension.",
            ),
        },
        required=["file_path"],
    ),
)