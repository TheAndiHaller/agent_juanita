import os
from config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be read. The path is always relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    working_directory_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory_abs_path, file_path))

    if not file_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

    if not os.path.exists(file_abs_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    if not os.path.isfile(file_abs_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    try:
        with open(file_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    
        if len(file_content_string) >= MAX_CHARS:
            file_content_string = file_content_string + f"[...File \"{file_path}\" truncated at 10000 characters]"
    
        return file_content_string
    except Exception as e:
        return f"Error reading file \"{file_path}\": {e}"
