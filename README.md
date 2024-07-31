
# IAC TOOL\ LANGUAGE MODEL RESEARCH 

## Overview

This repository contains scripts and configurations utilized to run our research project. In a nutshell, the publshed project repository includes the validation
on the use of existing IaC tools through the automated validation based on the latest official configuration-file parsers. 
Furthermore, it collects the project dependecy data from the GitHub generated dependency graph. With the collected data, 
it generates a server-based multi-LLM chat, fitted with generated JSONL files addressing the dependency data (SBOMs). The objective
is to draft the foundations of automated generation of IaC configuration files at diverse stages of a software project based on 
diverse potential _a priori_ information, in the case of this study SBOMs.

To perform this project, the following series of activities were developed/executed:

- **STEP1**: Validate Infrastructure as Code (IaC) tools using various parsers. The following instructions guide you through setting up the necessary tools and executing the `parsing_file.py` script.
- **STEP2**: Generating and collecting the project dependencies from GitHub.
- **STEP3**: Generating JSONL files for chat communication with the adopted Large Language Models.
- **STEP4**: Multi-API LLM integration process for interactive conversation with multiple LLMs for IaC configuration file generation.


## Prerequisites

Ensure you have the following tools installed and configured on your system:

1. **Terraform**
2. **AWS CloudFormation Linter (cfn-lint)**
3. **Azure Template Analyzer**
4. **Chef**
5. **Puppet**
6. **Salt Lint**
7. **Pulumi**

For Windows and Mac OS:
Before the code can be run, we must download the existing parsers on the web running on the files in the repo.

For Mac OS: 
The installations require homebrew. 
- You will need to intall Homebrew. All instructions for Mac OS past this point assume homebrew is downloaded.
  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

### Terraform (TF)
LINK- https://developer.hashicorp.com/terraform/install

**WINDOWS INSTALL**

- Click the windows download - it will show either 386 or AMD64 (you will have to click what is compatible with your system).
- You will then have to unzip the folder in whatever directory it was put to. This may be different for others but for me, it was Downloads.
- Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New".
- Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder.
- Go to your terminal and do "Terraform --version"

**SHOULD SHOW**: (may be different depending on version)
```
Terraform --version
Terraform v1.8.5
on windows_386
```

**LINUX INSTALL**

Interface as well as CLI installation ways offered, more info in the provided link.

**MAC OS INSTALL**

- Run the following commands to download Terraform through homebrew.
  ```
  brew tap hashicorp/tap
  brew install hashicorp/tap/terraform
  ```
- Verfiy the Terraform version to ensure installation
  ```
  terraform -v
  ```
- You should see the version that has downloaded on your system.
  ```
  Terraform v1.9.2
  on darwin_arm64
  
  ```
### AWS

Make sure you are doing this through the directory that you are working in or doing it through your default directory/root directory.
LINK- https://github.com/aws-cloudformation/cfn-lint

**MAC OS INSTALL**

- Ensure Python3 is installed
  ```
  % python3 --version
  Python 3.12.3
  ```
- Ensure pip is installed
  ```
  %brew install pip
  %pip3 --version
  pip 24.1.2 from /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/pip (python 3.12)
  ```
- Install cfn-lint using pip
  ```
  %pip3 install cfn-lint
  ```
- Verify the Installation
  ```
  %cfn-lint --version

  cfn-lint 1.5.3
  ```
**WINDOWS INSTALL**

The documentation should tell you what to do but for Windows assuming you have pip installed:
- Command - pip install cfn-lint

Verify the installation:
```
cfn-lint --version
cfn-lint 0.87.7
```

### Azure (template-analyzer)

LINK: https://github.com/Azure/template-analyzer

**MAC OS INSTALL**

- Install .NET Core SDK
  ```
  %brew install --cask dotnet-sdk
  %dotnet --version

  8.0.303
  ```
- Clone the repository https://github.com/Azure/template-analyzer
  ```
  % git clone https://github.com/Azure/template-analyzer.git
  % cd template-analyzer/src
  ```
- Build the project
  ```
  % dotnet build TemplateAnalyzer.sln
  ```
- You should now see a Analyzer.Cli directory in template-analyzer/src
- Find lines 259-263 in parsing_file.py and use the alternate line
- If you are using Mac OS, use this line instead of 'appear, files = AZ_validation(az_files)' :  
```
        appear, files = AZ_validation_mac(az_files)
```

**WINDOWS INSTALL**

- Go to "Download the latest Template Analyzer release in the releases section."
- You will pick TemplateAnalyzer-win-arm64.zip or TemplateAnalyzer-win-x64.zip
- Again once downloaded make sure you keep track of the directory at which you downloaded and add it to your path.
- Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New".
- Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder.
- Then TemplateAnalyzer --version or TemplateAnalyzer.exe --version

My output for this was:
```
0.7.0+582d9199d19acc60716af8f0874dc51cec6aa01b
```

### Chef

**UPDATED: MUST USE COOKSTYLE INSTEAD OF FOODCRITIC**

**MAC OS AND WINDOWS COOKSTYLE INSTALL**

  - Ensure Ruby is installed
      - MAC OS
        ```
        %brew install ruby
        %ruby -v
      
        ruby 3.1.2p20 (2022-04-12 revision 4491bb740a) [arm64-darwin20]
        ```
      - WINDOWS
        - LINK: https://rubyinstaller.org/downloads/   
        - Make sure to say put to path it will be a small box regarding to add ruby to path.
        - Once installed the terminal will show up prompting you what to download.
        - When I did this, I just pressed enter as that downloads everything. You will be prompted twice when you do this.
        - Once you are done, go to your terminal and input:
        - Verify the installation:
        ```
        ruby --version
        ruby 3.3.4 (2024-07-09 revision be1089c8ec) [x64-mingw-ucrt]
        ```
  - Install Cookstyle
      ```
      %sudo gem install cookstyle
      ```
  - Verify installation
      ```
      % cookstyle -v

      Cookstyle 7.32.8
          * RuboCop 1.25.1
      ```

### Puppet
Make sure you are on your root directory. This should be set as default but the command should be done in the user that you are working in.

**WINDOWS INSTALL**

LINK: https://www.puppet.com/docs/puppet/5.5/install_windows.html

- Go straight to "Download the Windows puppet-agent package.
- Puppet’s Windows packages can be found here. You need the most recent package for your OS’s"
- You will then see a long list of puppet's downloads don't be frightened just search for "puppet-agent-x64-latest.msi"
- You will then follow the download it and at the top right once it is finished click on it and a prompt should pop up giving you all the steps for download.
- It will specify where the download is taking place, so keep track of where it being placed.
- You can then add that file path to the system environment variables.

Go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New"

**MAC INSTALL**

- Install Puppet-agent through Homebrew Cask:
  ```
  %brew install --cask puppet-agent
  ```
- Verify Installation
  ```
  %puppet --version
  7.31.0
  ```
### Salt Lint

**WINDOWS INSTALL**

Install using pip:
```
pip install salt-lint
```
**MAC INSTALL**

- Install using pip
  ```
   % pip install salt-lint
  ```
- Verify Installation
  ```
  % salt-lint --version

  salt-lint 0.9.2
  ```
### Pulumi

LINK: https://www.pulumi.com/docs/install/

**WINDOWS INSTALL**

- Click Windows Binary Download.
- Unzip file where the Download was placed.
- Then copy the file path of that download (if you currently in file explorer you should be able to hit the top of the search bar and get exact path).
- Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New".
- Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder.
- Verify the installation:
  ```
  pulumi version
  v3.123.0
  ```
**MAC INSTALL**

- Install Pulumi with Homebrew
  ```
  %brew install pulumi
  ```
- Verify Installation
  ```
  % pulumi version

  v3.124.0
  ```


***You will need a Pulumi Access Token.** 

1) Visit https://app.pulumi.com/ and make an account or log in.

2) Click your profile icon and select 'Personal Access Tokens'

3) Click 'Create New Token'.

4) Give a description and create your token, which will be valid for 30 days.

5) You will see the message : 'This is your new access token. Be sure to copy it, because you won't be able to see it again!' followed by the access token, copy it.

6) Navigate to pulumi_check.py and locate :
```
PULUMI_ACCESS_TOKEN = ''
```
around lines 27-28.

7) Paste your token here.

8) Pulumi will work now.


### Ansible

Based on the official content parser developed by Ansible, only UNIX OS can be used.
More info on: https://github.com/ansible/ansible-content-parser

We encourage potential contributors on trying a validated approach to identify IaC Ansible use with Windows OS through:
https://github.com/ansible/ansible-lint

**STEPS for macOS:**

- Follow the procedure in the provided first link. (It is clearly explained, we just automate it's use for our purposes)
- Don't read the Execution section, that work is on us! ;)
- Once the ansible-lint and ansible-content-parser are in the same version the parser should be ready to use.

**Use of parser**
- Check documentation of ```ansible_main()``` within ```ansible_check.py``` file.

## Running the Script

Once all the parsers are downloaded, you should be able to execute `parsing_file.py` which executes all the parsers for the repos. Again not all of them are using parsers from the web, but instead through our own implementation of finding those files specific to the IAC tool.

Command line:
```
https://github.com/BOFACAM/FINALBASELINE.git
```

Clone the repository:
```
git clone https://github.com/BOFACAM/FINALBASELINE.git
```

Navigate to the repository directory:
```
cd FINALBASELINE
```

Create Python virtual environment (More information in [here](https://docs.python.org/3/library/venv.html#how-venvs-work)):
```
python3 -m venv venv
```

After activating the virtual environment, install the required dependencies:
```
pip install -r requirements.txt
```

Run the script:
```
python parsing_file.py
```

## IMPORTANT:

There are some GitHub links that aren't compatible with Windows due to its sensitivity to formatting (e.g., file names being too long or characters missing).

### Known Issues:
- **Cali-open** (Line 83)
- **CovenantSQL_CovenantSQL** (Line 94)
- **digirati-co-uk/madoc-platform** (Line 106)
- **lblod_app-demo-editor** (Line 125)
- **makeitfine-org_mif** (Line 229)
- **RedHatInsights_insights-puptoo** (Line 240)
- **TibebeJS_masterlance** (Line 293)

You should be seeing validating print statements showing the code working. This process will take a long time. There is range for the repos that you might wanna set yourself as well be free to change that. you wont be able to run this the whole way through due to the issues above. This has not been fully tested on linux or mac.

# GENERATE PROJECT DEPENDENCIES (STEP 2)

With the option to be performed while executing STEP 1, the following stage collects the data related to the project dependencies of each of
the projects included in the adopted MS dataset. For that, we collect the _Software Bill of Materials_ (SBOM) which can be collected from
the GitHub generated [Dependency Graph](https://docs.github.com/en/rest/dependency-graph/sboms?apiVersion=2022-11-28) through its REST API for instance.

To execute this stage the reader need only to activate the specified `python virtual environment` and run:

  1.    Inside the project folder `/sbom-generator`, specify the global paths in `commons.py` as documented in the comments writen in the same file.
2. In the same folder, within the file `get_sbom.py` introduce the generated GitHub token in **line 34**.
3. Inside the project folder, execute `/sbom-generator/main.py`
 


# GENERATING JSONL FILE (STEP 3)



To generate the .jsonl file storing the file dependencies, IaC tool usage flags and their respective prompts, the table from (STEP 1) must be fully generated for every repository.

The .jsonl file is generated by running setup_ollama.py, in which the main calls generate_jsonl.py's main to generate the file. 

For the inquisitive users, the procedure for generating the .jsonl file is listed below. (generate_jsonl.py) 
  1. Store the row for one repository in a dictionary, call this the working_row
  2. Go through the values of the working_row, checking which IaC tools tested true in the first screening (value = 1), and temporarily store the marked IaC tool, its corresponding extensions for their configuration files, the repository id, and its corresponding project dependencies generated in (STEP 2).
  3. Take all of these fields in 2. and mention them in a formatted prompt, having the prompts as the tailored fields of a new json row.
  4. Append the new json row to the jsonl file.
  5. This results in 1-13 IaC-tool-distinct json rows per repository, in the jsonl file.




# Multi-API LLM Integration (STEP 4)

This project integrates multiple LLM APIs including OpenAI, Anthropic's Claude, Google's Gemini, and Cohere. It reads input data from a JSONL file, processes it, and stores the responses from each API into a JSONL file for that respective JSONL file.

## Setup Instructions

### Step 1: Setting Up API Keys for LLMs (Windows)

1. **OpenAI**
- Visit the [OpenAI Quickstart](https://platform.openai.com/docs/quickstart) to get started.
- Obtain your API key from the [OpenAI API Keys](https://platform.openai.com/api-keys) page and save it securely.

 2. **Claude 3.5**
- Sign up and get your API key from the [Anthropic Console](https://console.anthropic.com/). Save your key securely.

3. **Gemini**
- Sign up and obtain your API key from [Google AI Studio](https://aistudio.google.com/app/prompts/new_chat). Save your key securely.

 4. **Cohere**
- Sign up and get your API key from the [Cohere Dashboard](https://dashboard.cohere.com/api-keys). Save your key securely.

Once you have all your API keys, set the environment variables using the `setx` command. This command sets environment variables permanently for the user.

For each API key, use the following template:
```
setx ANTHROPIC_KEY "apikey"
setx GOOGLE_API_KEY "apikey"
setx OPENAI_API_KEY "apikey"
setx CO_API_KEY "apikey"
```

### Step 2: Setting Up Virtual Environment and Necessary Installations

1. **Create a Virtual Environment**
   
  Run the following command in your VSCode terminal or in the terminal where you cloned this project:
  ```
  venv/Scripts/activate
  pip install google-generativeai langchain-google-genai streamlit pillow
  pip install --upgrade openai
  pip install anthropic
  pip install cohere
  ```

### Step 3: Running the Code

1. **Run the Script**

   ```bash
   python APISKELTON.py

The output will be appended to your respective JSONL files for each LLM.
The process will go through OpenAI, Claude 3.5, Gemini, and then Cohere.

1. **Run the Script**

   ```bash
   python setup_ollama.py

By running this file, you will be able to chat and ask for revisions of the configuration files response, and when you are happy with the results, simply type 'exit' to save the chat history.
This file populates a directory hierarchy as such:

For example:

📁responses
	
 	📁project_x
		
  		📁Google
			
   			🗄️wizard-vicuna.txt
			
   			. . .
			
   			🗄️dbrx.txt
    		
      		📁Kubernetes
    			
       			🗄️wizard-vicuna.txt
    			
       			. . .
    			
       			🗄️dbrx.txt
  
  	📁project_y
  . . .

Where Google and Kubernetes were indicated as IaC tools for project_x, obtained in results from (STEP 1)
	

> **Note:** **This is a base version and hasn't been fully tested. Adjustments may be necessary. Thank you!**

    








