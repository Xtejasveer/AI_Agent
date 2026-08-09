
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


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the contents of the given file as a string, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, from the working directory",
                },
            },
        },
    },
}


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the python file using the python3 interpreter. Accepts additional CLI args as an optional array",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": " The file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": " An optional array of strings to be used as the CLI args for the python file",
                },
            },
        },
    },
}


schema_write_file= {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites an existing file or writes to a new file if it doesn't exists and creates required parent dirs safely, constrained to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write.",
                },
                "content": {
                    "type": "string",
                    "description": "The contents to write to the file as a string.",
                },
            },
        },
    },
}