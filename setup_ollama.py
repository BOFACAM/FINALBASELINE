import json
import subprocess
import pickle

from generate_jsonl import jsonl_main

def get_json_from_jsonl(file_path):
    json_objects = []
    with open(file_path, 'r') as file:
        for line in file:
            json_object = json.loads(line.strip())
            json_objects.append(json_object)
    return json_objects

    

def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def run_llama3(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'llama3'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_gemma(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'gemma'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_mistral(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'mistral'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_stablelm(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'stablelm2'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_falcon2(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'falcon2'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_dbrx(prompt, file_content):
    full_prompt = f"{prompt}\n\nSBOM Content:\n{file_content}"
    process = subprocess.Popen(
        ['ollama', 'run', 'dbrx'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(full_prompt)
    if stderr:
        print("Error:", stderr)
    return stdout

def run_model(model_name, prompt, file_content):
    if model_name == 'llama3':
        return run_llama3(prompt, file_content)
    elif model_name == 'gemma':
        return run_gemma(prompt, file_content)
    elif model_name == 'mistral':
        return run_mistral(prompt, file_content)
    elif model_name == 'stablelm2':
        return run_stablelm(prompt, file_content)
    elif model_name == 'falcon2':
        return run_falcon2(prompt, file_content)
    elif model_name == 'dbrx':
        return run_dbrx(prompt, file_content)
    else:
        raise ValueError(f"Unknown model name: {model_name}")


def list_out_extensions(list_ext):
    if not list_ext:
        return ""
    if len(list_ext) == 1:
        return list_ext[0]
    
    str_ret = list_ext[0]
    for item in list_ext[1:]:
        str_ret = str_ret + " and " + item
    return str_ret


def main():
    # Example usage:
    json_file_path = jsonl_main()
    json_objects = get_json_from_jsonl(json_file_path)
    for obj in json_objects:
        print("obj \n")
        print(obj)
        print("\n")
        ext_str = list_out_extensions(obj.get("extension"))
        prompt = "Suppose you are a professional analyst specializing in Infrastructure as Code (IaC) tools. You have been given a Software Bill of Materials (SBOM) file representing a GitHub repository. Your task is to analyze this SBOM file and, given that the project uses a specific IaC tool, generate the corresponding specification files for that tool.The project in question uses " + obj.get("iac_tool") + ". Please return the specification files in "+ ext_str + " formats that accurately represent the infrastructure of the repository as described in the SBOM."
        print(prompt)
        model_name = 'falcon2'  
        file_content = read_pickle(obj.get("sbom_path"))
        response = run_model(model_name, prompt, file_content) 
        print("Response:", response)


   

main()
