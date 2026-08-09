
import json
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "calculator"

def call_function(tool_call, verbose = False):
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f"- Calling function: {function_name}({function_args})")
    else :
        print(f"- Calling function: {function_name}")


    result = ""

    if function_name == "get_files_info":
        result = get_files_info(working_directory, **function_args)
    if function_name == "get_file_content":
        result = get_file_content(working_directory, **function_args)
    if function_name == "write_file":
        result = write_file(working_directory, **function_args)
    if function_name == "run_python_file":
        result = run_python_file(working_directory, **function_args)

    if result == "":
        return {
            "role" :"tool",
            "tool_call_id" : tool_call.id,
            "content" : f"Unknown function : {function_name}."
        }
    return {
        "role" :"tool",
        "tool_call_id" : tool_call.id,
        "content" : result
    }

