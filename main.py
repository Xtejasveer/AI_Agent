import os 
from dotenv import load_dotenv
from openai import OpenAI
import sys
from functions.get_files_info import get_files_info

def main():


    load_dotenv()

    client = OpenAI(
        api_key = os.environ["OPENROUTER_API_KEY"],
        base_url = "https://openrouter.ai/api/v1"
    )
    if len(sys.argv) < 2 :
        print("I need a prompt")
        sys.exit(1)
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
        
    prompt = sys.argv[1]
    messages = [{"role" : "user", "content" :prompt}]


    
    print ("Args :", sys.argv)
    response = client.chat.completions.create(
        messages = messages,
        model = "google/gemma-4-26b-a4b-it:free"
    )

    print(response.choices[0].message.content)
    if response is None or response.usage is None:
        print("response is malformed")
        return 

    if verbose_flag : 
        print(f"User Prompt : {prompt}")
        print(f"Prompt Tokens : {response.usage.total_tokens}")

print(get_files_info("calculator"))

# main()