import json
import requests

#

ollama_api_url = "http://localhost:11434/api/chat"

"""
Given the JSONL file, return two lists: one containing the system and user dictionaries, 
and another containing the repository identifiers.

@param jsonL(file) : JSONL file with keys 'repo','iac_tool', 'system', and 'user'

@returns: Two lists (data, repo_ids) - data containing system and user dictionaries, and repo_ids containing repository identifiers.
"""
def read_jsonL(jsonL):
    data =[]
    repo_ids = []
    with open(jsonL,"r",encoding="utf-8") as file:
       for line in file:
            content = json.loads(line.strip())
            repo = content["repo"]
            system_line = content["system"]
            user_line = content["user"]
            data.append((system_line,user_line))
            repo_ids.append(repo)
    return data,repo_ids

"""

"""
def curl_to_ollama(model_name,conversation):
    headers = {
    'Content-Type': 'application/json',
}
    json_data = {
        "model": model_name,
        "messages": conversation,
        "stream":False
    }

    response = requests.post(ollama_api_url,headers=headers,json=json_data)
    return response.json()


def run_ollama(data,repo_ids,model_name):
    conversation_per_repo_id = {} 
    ollama_responses ={}
      
    try:
        with open(f"{model_name}.jsonl","a",encoding="utf-8") as file:
            for i in range(len(data)):
                repo_id = repo_ids[i]
                system = data[i][0]
                user = data[i][1]

                if repo_id not in conversation_per_repo_id:
                    conversation_per_repo_id[repo_id] = [system,user]
                else:
                    if repo_id in ollama_responses:
                        latest_assistant_reponse = ollama_responses[repo_id][-1]
                        conversation_per_repo_id[repo_id].append(latest_assistant_reponse)
                    conversation_per_repo_id[repo_id].append(user)
                
                #print(conversation_per_repo_id)

                
                response = curl_to_ollama(model_name,conversation_per_repo_id[repo_id])
                    
                response_json = {
                    "repo": repo_id,
                    "response": response
                }

                if 'message' in response:
                    if repo_id not in ollama_responses:
                        ollama_responses[repo_id] = []
                    ollama_responses[repo_id].append(response["message"])
                
                file.write(json.dumps(response_json) + "\n")

    except Exception as e:
        print(f"Error with ollama:{e}")
        return None


def main():
    jsonL_file = "data.jsonl"
    data,repo_ids = read_jsonL(jsonL_file)


    models = ["llama3"]
    #models = ["llama3", "falcon2", "stablelm2", "mistral", "gemma","vicuna","dbrx"]

    for model in models:
        run_ollama(data,repo_ids,model)


if __name__ == "__main__":
    main()  
