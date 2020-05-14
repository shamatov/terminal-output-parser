# Overview
Parsing terminal output of network devices and generate CSV report.

This script is based on TextFSM module and provide scalable solution for parsing different terminal output. Everytime we need to parse one more output - just need to create one more TextFSM template.

Supported OS: Windows, Unix

# One file - one template

    parser_output.py -f path/to/log/output-display-version.log -t path/to/template/display_version.template
    
TextFSM template example: 
    
    Value Required VERSION (V\d+R\d+C.*)
    Value Required HARDWARE (.*)
    Value UPTIME (.*)

    Start
      ^VRP \S+ software.*${VERSION}\) 
      ^${HARDWARE} uptime is ${UPTIME} -> Record

# One file - many templates

    parser_output.py -f path/to/log/output-show-version.log -tl path/to/template/inventory_templates.list

File **inventory_templates.list** contains list of TextFSM templates in same directory as **inventory_templates.list** file.
    
    display_version.template
    display_esn.template
    display_elabel.template

# Many files - one template

Parse all files(!) in directory **path/to/dir**:

    parser_output.py -d path/to/dir -t path/to/template/display_version.template
    
# Many files - many templates

    parser_output.py -d path/to/dir -tl path/to/template/inventory_templates.list

# Usage examples

**Full list of script arguments**

    >>>parser_output.py -h
      -h, --help            show this help message and exit
      -D DIRECTORY_PATH, --directory_path DIRECTORY_PATH
                            Absolute or relative path to directory
      -f FILENAME, --filename FILENAME
                            Absolute or relative path to text file
      -t TEMPLATE, --template TEMPLATE
                            Absolute or relative path to TextFSM template
      -tl TEMPLATES_LIST, --templates_list TEMPLATES_LIST
                            Absolute or relative path to TextFSM templates list
      -R REPORT_NAME, --report_name REPORT_NAME
                            Report name
      -V, --verbose


**Example 1**

Parse **output-show-version.log** file using TextFSM template **cisco-show-version.template**.
    
    parser_output.py -f path/to/log/output-show-version.log -t path/to/template/cisco-show-version.template

**Example 2**

Parse all files in **cisco-logs** directory using TextFSM template **cisco-show-version.template**.
    
    parser_output.py -f path/to/dir/cisco-logs/ -t path/to/template/cisco-show-version.template

**Example 3**

Parse all files in **cisco-logs** directory using TextFSM template **cisco-show-version.template**.
Generate report **cisco-versions.csv**:

    parser_output.py -f path/to/dir/cisco-logs/ -t path/to/template/cisco-show-version.template -R cisco-versions
