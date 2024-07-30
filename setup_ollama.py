import csv
import os
import subprocess
from generate_jsonl import json_main
import json
from file_writer import write_files

line_gen = None
responses = {}
#all_llms = ["llama3","gemma","mistral","stablelm2","falcon2","dbrx"]
all_llms = ["llama3"]


def delete_file(file_path):
    """
    Deletes the specified file.

    :param file_path: The path to the file to delete.
    """
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")

def jsonl_line_generator(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line.strip())

def init_generator(file_path):
    global line_gen
    line_gen = jsonl_line_generator(file_path)

def get_next_jsonl_line():
    global line_gen
    if line_gen is None:
        return None  # Generator not initialized
    try:
        return next(line_gen)
    except StopIteration:
        return None  # End of file

# Define a single function to handle all model calls
def run_model_generic(model_name, prompt):
    """
    Run the specified model with a given prompt and return the response.
    :param model_name: The name of the model to run.
    :param prompt: The prompt to send to the model.
    :return: The model's response.
    """
    process = subprocess.Popen(
        ['ollama', 'run', model_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if process.returncode != 0:
        print(f"Error from model {model_name}: {stderr}")
    return stdout.strip()  # Return the stripped response

# Map model names to the respective functions
def run_model(model_name, prompt):
    return run_model_generic(model_name, prompt)

def chat_with_model(api_payload):
    """
    Interactive chat with the selected model.
    :param api_payload: The JSON payload to send to the model, including model name, system message, and user message.
    """
    model_name = api_payload["model"]
    print(f"Starting chat with {model_name}. Type 'exit' to end the conversation.")
    chat_history = []

    # Convert api_payload to JSON string
    payload_json = json.dumps(api_payload)

    process = subprocess.Popen(
        ['curl', '-X', 'POST', 'http://localhost:11434/api/chat', 
         '-H', 'Content-Type: application/json', 
         '-d', payload_json],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error from model {model_name}: {stderr}")
    else:
        try:
            # Process stdout line by line
            for line in stdout.splitlines():
                # Parse the line into a JSON object
                response_dict = json.loads(line)
                # Extract the 'content' field
                message = response_dict.get('message', {})
                content_message = message.get('content', '')
                print(content_message, end='', flush=True)
                chat_history.append(content_message.strip())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    # Enter continuous chat loop
    while True:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Ending chat.")
            break

        # Add user input to chat history
        chat_history.append(f"You: {user_input}")

        # Send user input as a new message
        api_payload["messages"].append({ "role": "user", "content": user_input })

        # Convert new payload to JSON string
        payload_json = json.dumps(api_payload)

        process = subprocess.Popen(
            ['curl', '-X', 'POST', 'http://localhost:11434/api/chat', 
             '-H', 'Content-Type: application/json', 
             '-d', payload_json],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error from model {model_name}: {stderr}")
        else:
            try:
                # Process stdout line by line
                for line in stdout.splitlines():
                    # Parse the line into a JSON object
                    response_dict = json.loads(line)
                    # Extract the 'content' field
                    message = response_dict.get('message', {})
                    content_message = message.get('content', '')
                    print(content_message, end='', flush=True)
                    chat_history.append(content_message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    # Optionally, save chat history
    save_chat_history(chat_history, f"{model_name}_chat_history.txt")

def save_chat_history(chat_history, file_path):
    """
    Save the chat history to a file.
    :param chat_history: The chat history to save.
    :param file_path: The file path to save the chat history to.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(chat_history, file, indent=2)
        print(f"Chat history saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving chat history: {e}")

def write_csv_header(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["repo", "responses"])

def write_to_file(file_path, content):
    """
    Writes the given content to the specified file.

    :param file_path: The path to the file where content should be written.
    :param content: The string content to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Example usage:
# write_to_file('example.txt', 'This is some sample content.')
def append_csv_line(file_path, repo, responses):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([repo, responses])

def main():
    #1. populate jsonl
    json_main()
    #2. read jsonl and get 1 line at a time

    file_path = 'data.jsonl'
    init_generator(file_path)
    next_line = get_next_jsonl_line()
    #3. use line
    #while next_line is not None:
        #store system and user prompts and id
    system = next_line.get("system")
    sys_message = system['message']
    print(sys_message)
    print('\n')
    user = next_line.get("user")
    user_message = user['message']
    print(user_message)
    print('\n')
    id = next_line.get("repo")
    id_responses_label = "repo_" + id
    iac_label = next_line.get("iac_tool")

    api_payload = {
        "model": "",  # Assuming you're using the llama3.1 model
        "messages": [
            { "role": "system", "content": sys_message},
            { "role": "user", "content": user_message }
        ]
    }    
    print(api_payload)
    #pass in prompt for specific iac in repo for each llm
    for llm in all_llms:
        api_payload["model"]=llm
        print(api_payload)
        chat_with_model(api_payload)
        """"
        delete_file('response.txt')
        with open('response.txt', 'w') as file:
            file.write(response)
        write_files('response.txt',id_responses_label,iac_label,llm)"""
            
"""
    # Example usage:
    prompt = "Tell me a joke."
    model_name = 'falcon2'  
    #response = run_model(model_name, prompt)
    
    while response is None or " ":
        print("hello")
        response = run_model(model_name, prompt)
    
    #print("Response:", response)
"""

main()
