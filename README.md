For Windows:



For Mac:
1)chmod +x install_parsers.sh

2)chmod +x uninstall_parsers.sh

3)chmod +x setup_ansible_parser.sh
4)./install_parsers.sh
5)choose os, choose tool to download (ansible in this case)
6)When done downloading, venv directory should pop up
7)source venv/bin/activate
8)command line will have (venv) at the front
9)(untested) install the rest of the parsers inside the activated environment:
9a)./install_parsers.sh
9b) select os, select 'all'
9c) wait for all to download
10)python path/to/parsing_file.py (in my case it was : python /Users/Focus/Documents/GitHub/FINALBASELINE/parsing_file.py)
11)final output table will start generating
