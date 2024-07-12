# FINALBASELINE Repository(Not done yet)

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

For Windows:
Before the code can be run, we must download the existing parsers on the web running on the files in the repo.

TERRAFORM(TF):
LINK- https://developer.hashicorp.com/terraform/install 
Click the windows download - it will show either 386 or AMD64(you will have to click what is compatible with your system)
You will then have to unzip the folder in whatever directory it was put to. This may be different for others but for me Downloads.
Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New" 
Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder. 
Go to your terminal and do "Terraform --version" 

SHOULD SHOW: (may be different depending on version)
Terraform --version
Terraform v1.8.5
on windows_386


AWS:
LINK- https://github.com/aws-cloudformation/cfn-lint
The documentation should tell you about what to do but for Windows assuming you have pip installed. 
Command - pip install cfn-lint

cfn-lint --version
cfn-lint 0.87.7

Make sure you are doing this through the directory that you are working in or doing it through your default directory/root directory.

Azure(template-analyzer):
LINK:https://github.com/Azure/template-analyzer
Go to "Download the latest Template Analyzer release in the releases section."
you will pick TemplateAnalyzer-win-arm64.zip or TemplateAnalyzer-win-x64.zip
Again once downloaded make sure you keep track of the directory at you downloaded and add it to your path
Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New" 
Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder. 
Then TemplateAnalyzer --version or TemplateAnalyzer.exe --version

my output for this was: 
0.7.0+582d9199d19acc60716af8f0874dc51cec6aa01b


CHEF:
LINK:https://rubyinstaller.org/downloads/
Make sure to say put to path it will be a small box regarding to add ruby to path 
once installed the termainal will show up prompting you what to download
When I did this, i just pressed enter as that downloads everything. you will be prompted twice when you do this. 
Once you are done, go to your terminal and input

ruby --version
ruby 3.3.4 (2024-07-09 revision be1089c8ec) [x64-mingw-ucrt]

May be different depending on the version
Then we must download foodcritic 

In the same terminal, we do 
gem install foodcritic

foodcritic --version
foodcritic 16.3.0

again version may differ

Puppet:
LINK:https://www.puppet.com/docs/puppet/5.5/install_windows.html
go straight to "Download the Windows puppet-agent package
Puppet’s Windows packages can be found here. You need the most recent package for your OS’s"

you will then see a long list of" puppet's downloads dont be frightened just search for "puppet-agent-x64-latest.msi"

you will then follow the download it and at the top right once it is finished click on it and a prompt should pop up giving you all the steps for download. 

it will specifiy where the download is taking place, so keep track of where it being placed. 

You can then add that file path to the system enivornment variables.

go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New"

Paste done

SALT:
pip install salt-lint

Make sure you are on your root directory. This should be set as default but the command should be done in the user that you are working in



This should be 

Pulumi:
Link:https://www.pulumi.com/docs/install/

Click Windows Binary Download 

Unzip file where the Download was placed

Then copy the file path of that download (if you currently in file explorer you should be able to hit the top of the search bar and get exact path)

Then go to your "Edit system environment variables", go to "Environment Variables" --> "System Variables" --> "Path" --> "Edit" --> "New" 
Paste the exact path where you downloaded the parser. This allows your computer to use the executable in that folder. 

Check if downloaded properly:
pulumi version
v3.123.0


#insert Alex's explanation for token


Once all the parsers are downloaded, you should be able to execute parsing_file.py which executes all the parsers for the repos. Again not all of them are using parsers from the web, but instead through our own implementation of finding those files specific to the IAC tool

command line:
https://github.com/BOFACAM/FINALBASELINE.git

git clone https://github.com/BOFACAM/FINALBASELINE.git

python parsing_file.py

you should be seeing validating print statements showing the code working. this process will take along time. There is range for the repos that you might wanna set yourself as well be free to change that.














