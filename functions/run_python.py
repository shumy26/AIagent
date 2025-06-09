import os
import subprocess

def run_python_file(working_directory, file_path):
   try:
      abs_working_directory = os.path.abspath(working_directory)
      target_dir = abs_working_directory
      if file_path:
         target_dir = os.path.abspath(os.path.join(working_directory, file_path))
      if not target_dir.startswith(abs_working_directory):
         return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
      if not os.path.exists(target_dir):
         return f'Error: File "{file_path}" not found.'
      if not file_path.endswith(".py"):
         return f'Error: "{file_path}" is not a Python file.'
      result = subprocess.run(
         ["python3", target_dir],
         cwd=abs_working_directory,
         capture_output=True,
         text=True,
         timeout=30
      )
      output = result.stdout
      error = result.stderr
      response = []
      if output:
            response.append(f"STDOUT:\n{output}")
      if error:
         response.append(f"STDERR:\n{error}")
      if result.returncode != 0:
         response.append(f"Process exited with code {result.returncode}")
      if not response:
         return "No output produced."
      return "\n".join(response)
      
   except Exception as e:
      return f"Error: executing Python file: {e}"