import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):

    working_directory_abs_path = os.path.abspath(working_directory)
    directory_path = os.path.abspath(os.path.join(working_directory_abs_path, directory))

    if not directory_path.startswith(working_directory_abs_path):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

    if not os.path.exists(directory_path):
        return f"Error: \"{directory}\" does not exist"

    if not os.path.isdir(directory_path):
        return f"Error: \"{directory}\" is not a directory"



    result = []
    dir_content = os.listdir(directory_path)

    try:
        for entry in dir_content:
            entry_path = os.path.abspath(os.path.join(directory_path, entry))
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)

            result.append(f" - {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result)
    except Exception as e:
        return f"Error listing files: {e}"

