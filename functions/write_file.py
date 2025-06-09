import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_dir = abs_working_directory
        if file_path:
            target_dir = os.path.abspath(os.path.join(working_directory, file_path))
        if not target_dir.startswith(abs_working_directory):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"