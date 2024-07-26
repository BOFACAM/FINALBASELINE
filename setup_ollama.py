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

def run_llama3(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'llama3'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_gemma(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'gemma'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_dolphin_mistral(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'mistral'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_stablelm_zephyr(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'stablelm2'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_falcon2(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'falcon2'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_dbrx(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'dbrx'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_model(model_name, prompt):
    if model_name == 'llama3':
        return run_llama3(prompt)
    elif model_name == 'gemma':
        return run_gemma(prompt)
    elif model_name == 'mistral':
        return run_dolphin_mistral(prompt)
    elif model_name == 'stablelm2':
        return run_stablelm_zephyr(prompt)
    elif model_name == 'falcon2':
        return run_falcon2(prompt)
    elif model_name == 'dbrx':
        return run_dbrx(prompt)
    else:
        raise ValueError(f"Unknown model name: {model_name}")



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
    while next_line is not None:
        #store system and user prompts and id
        system = next_line.get("system")
        user = next_line.get("user")
        id = next_line.get("repo")
        id_responses_label = "repo_" + id
        iac_label = next_line.get("iac_tool")

        combined_prompt = str("role:" + system["role"] + "," + "content:" + system["content"] + "," + "role:" + user["role"] + "," + "content:" + user["content"])
        print(combined_prompt)
        #pass in prompt for specific iac in repo for each llm
        for llm in all_llms:
            response = run_model(llm, combined_prompt)
            delete_file('response.txt')
            with open('response.txt', 'w') as file:
                file.write(response)
            write_files('response.txt',id_responses_label,iac_label,llm)
            
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
