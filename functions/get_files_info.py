import os

def get_files_info(working_directory, directory="."):

    working_directory_abs_path = os.path.abspath(working_directory)
    directory_path = os.path.abspath(os.path.join(working_directory_abs_path, directory))

    if not os.path.exists(directory_path):
        return f"Error: \"{directory}\" does not exist"

    if not os.path.isdir(directory_path):
        return f"Error: \"{directory}\" is not a directory"

    if not directory_path.startswith(working_directory_abs_path):
        #raise Exception(f"Cannot list \"{directory}\" as it is outside the permitted working directory")
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

    result = []
    result.append("Result for current directory:")
    dir_content = os.listdir(directory_path)

    for entry in dir_content:
        entry_path = os.path.abspath(os.path.join(directory_path, entry))
        file_size = os.path.getsize(entry_path)
        is_dir = os.path.isdir(entry_path)

        result.append(f" - {entry}: file_size={file_size} bytes, is_dir={is_dir}")
    
    return "\n".join(result)


