import os
from google.genai import types

def write_file(working_directory, file_path, new_content):
    joined_path = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(joined_path)
    abs_dir = os.path.abspath(working_directory)

    if not abs_file.startswith(abs_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        #print(f"Debug: Creating directory for {os.path.dirname(abs_file)}")
        os.makedirs(os.path.dirname(abs_file), exist_ok=True)
    except Exception as e:
        return f"Error: {str(e)}"
    try:
        #print(f"Debug: Writing to file {abs_file}")
        with open(abs_file, "w") as f:
            f.write(new_content)
            return f'Successfully wrote to "{file_path}" ({len(new_content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified file with a specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",    
            ),
            "new_content": types.Schema(
                type=types.Type.STRING,
                description="Message to be written onto the specified file"
            )
        },
    ),
)