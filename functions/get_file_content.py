import os 

def get_file_content(working_directory, file_path):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      target_dir = abs_working_directory
      if file_path:
         target_dir = os.path.abspath(os.path.join(working_directory, file_path))
      if not target_dir.startswith(abs_working_directory):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      if not os.path.isfile(target_dir):
         return f'Error: File not found or is not a regular file: "{file_path}"'

      with open(target_dir) as file:
         file_content = file.read()
         if len(file_content) >= 10000:
            file_content = file_content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
      return file_content
   except Exception as e:
      return f"Error: {str(e)}"