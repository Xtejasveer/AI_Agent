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
        """You are a helpful AI coding agent.
        When a user asks a question or makes a request, amke afunction call plan. You can perform the following operations:
        - List files adn directories
        - Read file contents
        - Execute Pyhton files with optional arguments
        - Write or overwrite files
         
        All paths you provide should be relative to the working directory. You donot specify the wroking directory in your function calls as it is automatically injected for security reasons."""
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

    if not message.tool_calls:
        print(f"No tool calls made. The message content is : {message.content}")
    else :
        for tool_call in message.tool_calls:
            result = call_function(tool_call, verbose_flag)
            print(result)

main()