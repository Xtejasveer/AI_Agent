import os

def get_files_info (working_directory, directory = None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = ""
    if directory is None:
        abs_directory = os.path.abspath(working_directory)
    else : 
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        return f"Error : {directory} is not in the working directory"

    final_response = ""

    contents = os.listdir(abs_directory)
    for content in contents:
        content_path =os.path.join(abs_directory,content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f" - {content}: file_size = {size} bytes, is_dir = {is_dir}\n"
    return final_response


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}