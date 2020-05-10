# terminal-output-parser
Parsing output of SSH commands on Network devices and generate CSV report.

This script is based on TextFSM module.

Usage:

    parser_output.py
      -h, --help            show this help message and exit
      -D DIRECTORY_PATH, --directory_path DIRECTORY_PATH
                  Absolute or relative path to directory
      -f FILENAME, --filename FILENAME
                  Absolute or relative path to text file
      -t TEMPLATE, --template TEMPLATE
                  Absolute or relative path to TextFSM template
      -R REPORT_NAME, --report_name REPORT_NAME
                  Report name


Example 1.

Parse **output-show-version.log** file using TextFSM template **cisco-show-version.template**.
    
    parser_output.py -f path/to/log/output-show-version.log -t /path/to/template/cisco-show-version.template

Example 2.

Parse all files in **cisco-logs** directory using TextFSM template **cisco-show-version.template**.
    
    parser_output.py -f path/to/dir/cisco-logs/ -t /path/to/template/cisco-show-version.template

