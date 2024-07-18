
# FINALBASELINE Repository

## Overview

This repository contains scripts and configurations to validate Infrastructure as Code (IaC) tools using various parsers. The following instructions guide you through setting up the necessary tools and executing the `parsing_file.py` script.

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

### Terraform (TF)
LINK- https://developer.hashicorp.com/terraform/install

**WINDOWS INSTALL**
- Click the windows download - it will show either 386 or AMD64 (you will have to click what is compatible with your system).
- You will then have to unzip the folder in whatever directory it was put to. This may be different for others but for me, it was Downloads.
- Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New".
- Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder.
- Go to your terminal and do "Terraform --version"

**MAC OS INSTALL**
- First, you will need to intall Homebrew
  '''
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  '''
**SHOULD SHOW**: (may be different depending on version)
```
Terraform --version
Terraform v1.8.5
on windows_386
```

**MAC/LINUX INSTALL**
Interface as well as CLI installation ways offered, more info in the provided link.

### AWS
LINK- https://github.com/aws-cloudformation/cfn-lint

The documentation should tell you what to do but for Windows assuming you have pip installed:
- Command - pip install cfn-lint

Verify the installation:
```
cfn-lint --version
cfn-lint 0.87.7
```

Make sure you are doing this through the directory that you are working in or doing it through your default directory/root directory.

### Azure (template-analyzer)
LINK: https://github.com/Azure/template-analyzer

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
LINK: https://rubyinstaller.org/downloads/

- Make sure to say put to path it will be a small box regarding to add ruby to path.
- Once installed the terminal will show up prompting you what to download.
- When I did this, I just pressed enter as that downloads everything. You will be prompted twice when you do this.
- Once you are done, go to your terminal and input:

Verify the installation:
```
ruby --version
ruby 3.3.4 (2024-07-09 revision be1089c8ec) [x64-mingw-ucrt]
```

May be different depending on the version. Then we must download foodcritic:

In the same terminal, we do:
```
gem install foodcritic
```

Verify the installation:
```
foodcritic --version
foodcritic 16.3.0
```

### Puppet
LINK: https://www.puppet.com/docs/puppet/5.5/install_windows.html

- Go straight to "Download the Windows puppet-agent package.
- Puppet’s Windows packages can be found here. You need the most recent package for your OS’s"
- You will then see a long list of puppet's downloads don't be frightened just search for "puppet-agent-x64-latest.msi"
- You will then follow the download it and at the top right once it is finished click on it and a prompt should pop up giving you all the steps for download.
- It will specify where the download is taking place, so keep track of where it being placed.
- You can then add that file path to the system environment variables.

Go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New"

### Salt Lint
Install using pip:
```
pip install salt-lint
```

Make sure you are on your root directory. This should be set as default but the command should be done in the user that you are working in.

### Pulumi
LINK: https://www.pulumi.com/docs/install/

- Click Windows Binary Download.
- Unzip file where the Download was placed.
- Then copy the file path of that download (if you currently in file explorer you should be able to hit the top of the search bar and get exact path).
- Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New".
- Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder.

You will need a Pulumi Access Token. 

1) Visit https://app.pulumi.com/ and make an account or log in.

2) Click your profile icon and select 'Personal Access Tokens'

3) Click 'Create New Token'.

4) Give a description and create your token, which will be valid for 30 days.

5) You will see the message : 'This is your new access token. Be sure to copy it, because you won't be able to see it again!' followed by the access token, copy it.

6) Navigate to pulumi_check.py and locate :
"
PULUMI_ACCESS_TOKEN = ''
"
around lines 27-28.


7) Paste your token here.

8) Pulumi will work now.

Verify the installation:
```
pulumi version
v3.123.0
```

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
