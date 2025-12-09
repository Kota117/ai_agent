import os

# Need to use the ".config" notation when running from test_get_file_content.py,
# but need the "config" notation when running script directly. This is a hacky way
# to accomplish both
try:
    from config import MAX_CHARS
except ModuleNotFoundError:
    from .config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    
    if not os.path.isfile(target_file):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    try:
        with open(target_file, 'r') as inFile:
            file_content_string = inFile.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f"[...File \"{target_file}\" truncated at 10000 characters]"
            return file_content_string
    except Exception as e:
        return f"Error listing file contents: {e}"
