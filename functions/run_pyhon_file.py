import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs_path = os.path.abspath(working_directory)
    file_abs_path = os.path.abspath(os.path.join(working_directory_abs_path, file_path))

    if not file_abs_path.startswith(working_directory_abs_path):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

    if not os.path.exists(file_abs_path):
        return f"Error: File \"{file_path}\" not found."

    if not os.path.isfile(file_abs_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""

    if not file_abs_path.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."
    
    dir_path, file_name = os.path.split(file_abs_path)

    args_to_run = ["python3", file_name] + args

    try:
        completed_process = subprocess.run(args_to_run, timeout=30, capture_output=True ,cwd=dir_path, text=True)

        if completed_process.returncode != 0:
            return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}, Process exited with code {completed_process.returncode}"
        elif len(completed_process.stdout) <= 0 and len(completed_process.stderr) <= 0:
            return f"No output produced."
        else:
            return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr} {completed_process.returncode}"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"