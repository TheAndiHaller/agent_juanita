import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    # Verbose flag
    verbose = False

    if len(sys.argv) < 2:
        print("Error: ADD a prompt as argument")
        sys.exit(1)

    if "--verbose" in sys.argv:
        verbose = True

    user_prompt = sys.argv[1]

    # History of the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # System prompt
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print("")

    print(response.text)

    
    for function_call_part in response.function_calls:

        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error: no function response!")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    if verbose:    
        print("")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    function_result = ""
    if function_name == "get_files_info":
        function_result = get_files_info("./calculator", **function_args)

    elif function_name == "get_file_content":
        function_result = get_file_content("./calculator", **function_args)

    elif function_name == "run_python_file":
        function_result = run_python_file("./calculator", **function_args)

    elif function_name == "write_file":
        function_result = write_file("./calculator", **function_args)

    else:
        return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )

    return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )

if __name__ == "__main__":
    main()