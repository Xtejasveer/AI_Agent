import os 
import json
from dotenv import load_dotenv
from openai import OpenAI
import sys
from functions.get_files_info import schema_get_files_info

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
    ]
    
    print ("Args :", sys.argv)
    response = client.chat.completions.create(
        messages = messages,
        model = "google/gemma-4-26b-a4b-it:free",
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
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling Function: {tool_call.function.name}({function_args})")

main()