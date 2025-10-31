import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a file located within a predefined working directory. Automatically creates te file or any missing subdirectories.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=
                    "Relative path to the file to write, within the predefined working directory. Parent directories will be created automatically if they don't exist.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):

    working_directory_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory_abs_path, file_path))

    if not file_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
    
    dir_path = os.path.dirname(file_abs_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(file_abs_path, "w") as f:
            f.write(content)
    
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error writing file \"{file_path}\": {e}"




