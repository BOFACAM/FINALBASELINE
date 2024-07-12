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
LINK:
