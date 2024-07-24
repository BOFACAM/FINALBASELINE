import csv
import subprocess
from generate_jsonl import json_main
import json

line_gen = None
responses = {}
all_llms = ["llama3","gemma","mistral","stablelm2","falcon2","dbrx"]
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

def append_csv_line(file_path, repo, responses):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([repo, responses])

def main():
    #1. populate jsonl
    json_main()

    responses_path = 'responses.csv'


    #write responses header
    write_csv_header(responses_path)

    

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

        #stores {"iac":responses, "iac": responses, ...}
        temp = {}
        iac_responses = {
            "llama3":"",
            "gemma":"",
            "mistral":"",
            "stablelm2":"",
            "falcon2":"",
            "dbrx":""
        }
        combined_prompt = system + user
        print(combined_prompt)
        #pass in prompt for specific iac in repo for each llm
        for llm in all_llms:
            response = run_model(llm, combined_prompt)
            #store responses for each llm
            iac_responses[llm]=response
            print(llm, iac_responses[llm])
        

        next_line = get_next_jsonl_line()
        if next_line.get("repo")==id:
            #if same repo, then append iac,responses for the prompt to the temp
            temp[iac_label] = iac_responses
        else:
            #if not the same repo, then append new field to responses  = 'repo_x' : { iac1: {}, iac2: {} , .... }
            responses[id_responses_label]=temp
            append_csv_line(responses_path, id_responses_label,temp)

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
