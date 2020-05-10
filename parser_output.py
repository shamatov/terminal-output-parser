#!/usr/bin/python3

import sys

import textfsm
from tabulate import tabulate
import os
import csv
from datetime import datetime
from argparse import ArgumentParser
#from ReportExcel import ReportExcel

__author__ = 'Ravil Shamatov, ravil.shamatov@huawei.com, rav.shamatov@gmail.com'
SCRIPT_DESCRIPTION = f"""This is TextFSM parser that get all needed information and output to CSV report. 
Author: {__author__}. Version: 2020-04-16"""

CSV_DELIMETER = ','

def parse_file(template_filename, output_filename, print_console=False):
    with open(template_filename) as t, open(output_filename, 'r') as output:
        re_table = textfsm.TextFSM(t)
        
        if print_console:
            header = re_table.header
            print(tabulate(re_table.ParseText(output.read()), headers=header))
        else:
            return re_table.ParseText(output.read())
        #result = [[output_filename] + row for row in )]
        #return result


def parse_directory(template_filename, directory_path, report_name=None):
    report_name = report_name or datetime.today().strftime('report_%Y-%m-%d_%H-%M')
    with open(report_name + '.csv', mode='w') as f,  open(template_filename) as t:
        writer = csv.writer(f, quotechar='"', delimiter=CSV_DELIMETER)
        # CSV Header
        writer.writerow(
            ['Filename'] + textfsm.TextFSM(t).header)
        # Parsing every file in directory and write result to CSV report
        for filename in os.listdir(directory_path):
            for row in parse_file(template_filename, directory_path + '/' + filename):
                writer.writerow([filename] + row)
    print(f"Report filename: {report_name}")

def read_arguments():
    parser = ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('-D','--directory_path',help='Absolute or relative path to directory',required=False)
    parser.add_argument('-f','--filename',help='Absolute or relative path to text file',required=False)
    parser.add_argument('-t','--template',help='Absolute or relative path to TextFSM template',required=True)
    parser.add_argument('-R','--report_name',help='Report name',required=False)
    return parser.parse_args()

if __name__ == '__main__':
    """ Main function:
        1. Parse file if command was like ./parser_output.py -t display_elabel.template -f filename.log
        2. Parse all files in directory if command was ./parser_output.py -t display_elabel.template -D data2
    """    
    args = read_arguments()
    if args.directory_path:
        print(f"Parsing all files from directory '{args.directory_path}'\n")
        parse_directory(args.template, args.directory_path, args.report_name)
    elif args.filename:
        print(f"Parsing file '{args.filename}' using template '{args.template}'\n")
        parse_file(args.template, args.filename, print_console=True)
    else:
        print('Please enter path to Directory of File')
    
