from openai import OpenAI
import openai
import anthropic
#import google.generativeai as genai

import json
import os


#set up virtual environment
"""python -m venv venv
    venv/Scripts/activate
    pip install google-generativeai langchain-google-genai streamlit pillow
    pip install --upgrade openai
    pip install anthropic

    setx ANTHROPIC_KEY "apikey"
    setx GOOGLE_API_KEY "apikey"
    setx OPENAI_API_KEY "apikey"
"""

#https://platform.openai.com/docs/quickstart chatgpt
#https://www.datacamp.com/tutorial/claude-sonnet-api-anthropic claude

#https://ai.google.dev/gemini-api/docs/system-instructions?lang=python gemini
#https://codemaker2016.medium.com/build-your-own-chatgpt-using-google-gemini-api-1b079f6a8415


openai.api_key = os.environ["OPENAI_API_KEY"]
anthropic_key = os.getenv("ANTHROPIC_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

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
            

def run_claude3(data,repo_ids):
    client = anthropic.Anthropic(api_key = anthropic_key)
    list_of_responses = []

    try:
        for i in range(len(data)):#when first testing may be good to set the end of the range to 1 not len(data)
            system = data[i][0]
            user = data[i][1]
            response = client.messages.create(
                model ="claude-3.5-sonnet-20240620",
                max_tokens=1024,
                messages = [user],
                system = system["content"],
                temperature=0.7
            )
            
            response_json = {
                "repo":repo_ids[i],
                "response":response #im not sure if it is just reponse it wasnt clear in the documentation
            }

            list_of_responses.append(response_json)
        

        with open("claude3responses.jsonl","w",encoding="utf-8") as file:
            for jsons in list_of_responses:
                file.write(json.dumps(jsons) + "\n")

    except Exception as e:
        print(f"Error with Claude3:{e}")
        return None

    return list_of_responses

"""def run_gemini(data,repo_ids):
    list_of_responses = []
    genai.configure(api_key=google_api_key)#os.environ["GOOGLE_API_KEY"]

    try:
        for i in range(len(data)):
            system = data[i][0]
            user = data[i][1]

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction = system["content"]
            )

            response = model.generate_content(user["content"])

            response_json = {
                "repo":repo_ids[i],
                "response": response
            }

            list_of_responses.append(response_json)
        
        with open("geminiresponses.jsonl","w",encoding="utf-8") as file:
                for jsons in list_of_responses:
                    file.write(json.dumps(jsons) + "\n")
        

    except Exception as e:
        print(f"Error with Gemini3: {e}")
        return None

    return list_of_responses"""
    

def run_openai(data,repo_ids):
    client = OpenAI()
    list_of_responses =[]

    try:
        for i in range(len(data)): #when first testing may be good to set the end of the range to 1 not len(data)
            system = data[i][0]
            user = data[i][1]
            completion = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    system,
                    user,
                ],
            
                max_tokens=1024,
                temperature=0.7
            )

            response_json={
                "repo":repo_ids[i],
                "response": completion.choices[0].message
            }

            list_of_responses.append(response_json)

        with open("chatgptresponses.jsonl","w",encoding="uft-8") as file:
            for jsons in list_of_responses:
                file.write(json.dumps(jsons)+ "\n")
            
    except Exception as e:
        print (f"Error with ChatGpt:{e}")
        return None
    
    return list_of_responses

def main():
    jsonL_file = "data.jsonl"
    data,repo_ids = read_jsonL(jsonL_file)
    
    if not data:
        print("Invalid data in file")
        return

    #result_openai = run_openai(data,repo_ids)
    #result_claude3 = run_claude3(data,repo_ids)
    #result_gemini = run_gemini(data,repo_ids)

if __name__ == "__main__":
    main()