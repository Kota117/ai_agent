import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    # This should ensure cross-compatability across operating systems
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    # Ensure 'directory' is in 'working_directory'
    if not target_dir.startswith(abs_working_dir):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    
    # Ensure 'directory' is a directory
    if not os.path.isdir(target_dir):
        return f"Error: \"{directory}\" is not a directory"

    # Catch any and all errors from the standard library functions
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"


# Declaration schema for the Gemini LLM
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
