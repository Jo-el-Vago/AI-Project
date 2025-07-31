import os
from google.genai import types


def get_files_info(working_directory, directory = None):
    if directory == None:
        directory = "."
    rel_dir = os.path.join(working_directory, directory)
    abs_dir = os.path.abspath(rel_dir)
    abs_working_dir = os.path.abspath(working_directory)
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(abs_dir)
        file_formats = []
        for file in files:  # Use the files variable you already got!
            fpath_file = os.path.join(abs_dir, file)
            file_formats.append(f"- {file}: file_size={os.path.getsize(fpath_file)} bytes, is_dir={os.path.isdir(fpath_file)}")
        return "\n".join(file_formats)  # Convert list to string
    except PermissionError:
        return "Error: Permission denied"
    except FileNotFoundError:
        return "Error: Directory not found"
    except Exception as e:
        return f"Error: {str(e)}"
    
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

