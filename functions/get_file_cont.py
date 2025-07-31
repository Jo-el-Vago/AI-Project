import os
from google.genai import types

def get_file_content(working_directory, file_path):
    join_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(join_path)
    abs_working_dir = os.path.abspath(working_directory)
    max_chars = 10000

    if not abs_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file, "r") as f:
            file_content_string = f.read(max_chars + 1)
        if len(file_content_string) <= 10000:
            return file_content_string
        else :
            return file_content_string[:max_chars] + f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {str(e)}"   


schema_get_files_cont = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)