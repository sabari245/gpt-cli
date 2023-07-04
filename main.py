import json
import openai
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def execute_command(command):
    print(f"> {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        return json.dumps({"success": True})
    except subprocess.CalledProcessError as e:
        return json.dumps({"success": False, "error": str(e)})


messages = [
    {
        "role": "system",
        "content": "you are a bot which executes windows commands. the user provides you the task to do and you have to execute it with the provided function. if the task involves multiple commands just combine them with the & symbol. on a successful command print done and on a failed command print error: followed by the error message.",
    }
]

function_json = [
    {
        "name": "execute_command",
        "description": "Execute a windows cmd command and returns the success status",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute",
                },
            },
            "required": ["command"],
        },
    }
]


def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=function_json,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "execute_command": execute_command,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]

        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            command=function_args.get("command"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


if __name__ == "__main__":
    while True:
        user_input = input("# ")
        messages.append({"role": "user", "content": user_input})
        response = run_conversation()
        print(f"> {response['choices'][0]['message']['content']}")
