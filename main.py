import os, sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.call_function import call_function


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

verbose = False

if len(sys.argv) >= 2:
   user_prompt = sys.argv[1]
else:
   print("No prompt passed")
   sys.exit(1)
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
   verbose = True

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets all the file contents of the file that is passed, as long as it is inside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath from which the contents will be read, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Given a file_path to a python file, you will run this file. The file has to be inside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the python script, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="This function writes content to a file given a filepath, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to which the content will be written, relative to the working directory.",
            ),
            "content": types.Schema(
               type=types.Type.STRING,
               description="The content that will be written to the filepath, as a big string that is truncated if it exceeds 10000 characters."
            )
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file
    ]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

def generate_content(response, verbose=False):
    if response.function_calls:
        for function_call_part in response.function_calls:   
            result = call_function(function_call_part, verbose=verbose)
            if not result.parts[0].function_response:
                raise Exception(f"Function {function_call_part.name} returned no response")
            elif verbose:
                print(f"-> {result.parts[0].function_response.response}")
            



generate_content(response, verbose)