import subprocess

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

# Example usage:
prompt = "Tell me a joke."
model_name = 'falcon2'  
response = run_model(model_name, prompt)
"""
while response is None or " ":
    print("hello")
    response = run_model(model_name, prompt)
"""

print("Response:", response)
