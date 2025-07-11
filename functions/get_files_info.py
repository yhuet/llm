import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory:
        full_path = os.path.join(working_directory, directory)
    else:
        full_path = working_directory
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)
    if not absolute_full_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    contents = os.listdir(full_path)
    result = []
    try:
        for file_name in contents:
            file_size = os.path.getsize(os.path.join(full_path, file_name))
            is_dir = os.path.isdir(os.path.join(full_path, file_name))
            result.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result)
    except Exception as e:
        print(f"Error: {e}")

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