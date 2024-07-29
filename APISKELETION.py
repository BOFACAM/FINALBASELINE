from openai import OpenAI
import openai
import anthropic
import google.generativeai as genai
import cohere
import json
import os

#set up virtual environment
"""python -m venv venv
    venv/Scripts/activate
    pip install google-generativeai langchain-google-genai streamlit pillow
    pip install --upgrade openai
    pip install anthropic
    pip install cohere

    setx ANTHROPIC_KEY "apikey"
    setx GOOGLE_API_KEY "apikey"
    setx OPENAI_API_KEY "apikey"
    setx COHERE_API_KEY "apikey"
"""

#https://platform.openai.com/docs/quickstart chatgpt
#https://www.datacamp.com/tutorial/claude-sonnet-api-anthropic claude

#https://ai.google.dev/gemini-api/docs/system-instructions?lang=python gemini
#https://codemaker2016.medium.com/build-your-own-chatgpt-using-google-gemini-api-1b079f6a8415

#https://www.datacamp.com/tutorial/cohere-api-tutorial cohere
#https://cohere.com/llmu/building-a-chatbot


openai.api_key = os.environ["OPENAI_API_KEY"]
anthropic_key = os.getenv("ANTHROPIC_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
cohere_api_key = os.getenv("CO_API_KEY")

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

    try:
        with open("claude3responses.jsonl","a",encoding="utf-8") as file:
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

                file.write(json.dumps(response_json) + "\n")

    except Exception as e:
        print(f"Error with Claude3:{e}")
        return None


def run_gemini(data,repo_ids):
    genai.configure(api_key=google_api_key)#os.environ["GOOGLE_API_KEY"]

    try:
        with open("geminiresponses.jsonl","a",encoding="utf-8") as file:
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

                file.write(json.dumps(response_json) + "\n")

    except Exception as e:
        print(f"Error with Gemini3: {e}")
        return None

    
def run_openai(data,repo_ids):
    client = OpenAI()

    try:
        with open("chatgptresponses.jsonl","a",encoding="utf-8") as file:
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

                file.write(json.dumps(response_json) + "\n")

    except Exception as e:
        print(f"Error with ChatGpt:{e}")
        return None

def run_cohere(data,repo_ids):
    co = cohere.Client(cohere_api_key)

    try:
        with open("cohereresponses.jsonl","a",encoding="utf-8") as file:
            for i in range(len(data)):
                system = data[i][0]
                user = data[i][1]
                response = co.chat(message = user["content"],
                                model = "command-r-plus",
                                preamble=system["content"]

                )

                response_json = {
                    "repo":repo_ids[i],
                    "response": response.text
                }

                file.write(json.dumps(response_json)+ "\n")
            

    except Exception as e:
        print(f"Error with Claude:{e}")
    

def main():
    jsonL_file = "data.jsonl"
    data,repo_ids = read_jsonL(jsonL_file)
    
    if not data:
        print("Invalid data in file")
        return

    run_openai(data,repo_ids)
    run_claude3(data,repo_ids)
    run_gemini(data,repo_ids)
    run_cohere(data,repo_ids)

if __name__ == "__main__":
    main()
