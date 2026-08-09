import os 
import json
from dotenv import load_dotenv
from openai import OpenAI
import sys
from functions.functions_schema import schema_run_python_file, schema_get_files_info, schema_get_file_content, schema_write_file
from call_function import call_function
def main():


    load_dotenv()

    client = OpenAI(
        api_key = os.environ["OPENROUTER_API_KEY"],
        base_url = "https://openrouter.ai/api/v1"
    )

    system_prompt = (
    """You are a helpful AI coding agent working in a specific codebase.

    When a user reports a bug, asks a question about behavior, or asks for a fix,
    you must investigate the actual code first using your available functions
    before answering or proposing a fix. Do not rely on general knowledge alone —
    always look at the relevant files, even if you think you already know the answer,
    because the bug may be specific to this codebase's implementation.

    You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not
    specify the working directory in your function calls — it is automatically
    injected for security reasons."""
)

    if len(sys.argv) < 2 :
        print("I need a prompt")
        sys.exit(1)
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
        
    prompt = sys.argv[1]
    messages = [{"role" : "user", "content" :prompt},
                {"role" : "system", "content" : system_prompt}]

    available_functions = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]


    max_iters = 20

    for i in range(0, max_iters):
        
        print ("Args :", sys.argv)
        response = client.chat.completions.create(
            messages = messages,
            model = "gpt-4o-mini",
            temperature= 0,
            tools = available_functions   
        )

        if response is None or response.usage is None:
            print("response is malformed")
            return 

        if verbose_flag : 
            print(f"User Prompt : {prompt}")
            print(f"Prompt Tokens : {response.usage.total_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result = call_function(tool_call, verbose_flag)
                messages.append(result)
        else:
            #final agent text message
            print(message.content)
            return 
    else :
        print(f"Error: Maximum iterations ({max_iters}) reached without a final response .")
        sys.exit(1)
main()