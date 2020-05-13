#!/usr/bin/python3

import sys

import textfsm
from tabulate import tabulate
import os
import csv
from datetime import datetime
import logging
from argparse import ArgumentParser
#from ReportExcel import ReportExcel

__author__ = 'Ravil Shamatov, ravil.shamatov@huawei.com, rav.shamatov@gmail.com'
SCRIPT_DESCRIPTION = f"""This is TextFSM parser that get all needed information and output to CSV report. 
Author: {__author__}. Version: 2020-04-16"""

CSV_DELIMETER = ','
logger = logging.getLogger('parser')
LOGGING_LEVELS = {
    0: logging.INFO,
    1: logging.DEBUG
}


def parse_file(output_filename, template_filename, print_console=False):
    with open(template_filename) as t, open(output_filename, 'r') as output:
        re_table = textfsm.TextFSM(t)
        
        if print_console:
            header = re_table.header
            logger.warning(tabulate(re_table.ParseText(output.read()), headers=header))
        else:
            return re_table.ParseText(output.read())
        #result = [[output_filename] + row for row in )]
        #return result

def parse_file_many_templates(output_filename, template_filenames, print_console=False):
    result_line = []
    logger.debug(f"File '{output_filename}' - opened")
    for template in template_filenames:
        logger.debug(f"File '{output_filename}' - template '{template}'")
        row = parse_file(output_filename, template, print_console)
        logger.debug(f"Result: {row}")
        try: 
            result_line.extend(row[0])
        except IndexError:
            logger.info(f"File '{output_filename}' - template '{template}' - matches not found")
    logger.info(f"File '{output_filename}' - done")
    return result_line

def parse_directory(template_filename, directory_path, report_name=None):
    report_name = report_name or datetime.today().strftime('report_%Y-%m-%d_%H-%M')
    with open(report_name + '.csv', mode='w') as f,  open(template_filename) as t:
        writer = csv.writer(f, quotechar='"', delimiter=CSV_DELIMETER)
        # CSV Header
        writer.writerow(
            ['Filename'] + textfsm.TextFSM(t).header)
        # Parsing every file in directory and write result to CSV report
        for filename in os.listdir(directory_path):
            for row in parse_file(os.path.join(directory_path, filename), template_filename):
                writer.writerow([filename].extend(row))
    print(f"Report filename: {report_name}")

def read_templates_list(filename):
    dir_path = os.path.dirname(os.path.abspath(filename))
    template_filenames = []
    for line in open(filename):
        template_path = os.path.join(dir_path, line.strip())
        if os.path.exists(template_path):
            template_filenames.append(template_path)
            logger.warning(f'{template_path}\t- OK')
        else:    
            logger.warning(f'{template_path}\t- not exists')
    logger.warning('')
    return template_filenames

def read_arguments():
    parser = ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('-D','--directory_path',help='Absolute or relative path to directory',required=False)
    parser.add_argument('-f','--filename',help='Absolute or relative path to text file',required=False)
    parser.add_argument('-t','--template',help='Absolute or relative path to TextFSM template',required=False)
    parser.add_argument('-tl','--templates_list',help='Absolute or relative path to TextFSM templates list',required=False)
    parser.add_argument('-R','--report_name',help='Report name',required=False)
    parser.add_argument('-V','--verbose',action='count', default=0)
    return parser.parse_args()

def configure_logging(logging_level):
    logger.setLevel(logging_level)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging_level + logging.DEBUG)
    ch.setFormatter(
        logging.Formatter('%(message)s'))
    
    fh = logging.FileHandler('parser_output.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter('%(asctime)s:%(name)s:%(levelname)s\t%(message)s'))
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('')
    logger.info(f"Logging is configured with level '{logging_level}'")

if __name__ == '__main__':
    """ Main function:
        1. Parse file if command was like ./parser_output.py -t display_elabel.template -f filename.log
        2. Parse all files in directory if command was ./parser_output.py -t display_elabel.template -D data2
    """    
    args = read_arguments()
    configure_logging(LOGGING_LEVELS[args.verbose])
    
    logger.info(f"Starting parser with argumetns {args}")
    if args.directory_path and args.template:
        logger.warning(f"Parsing all files from directory '{args.directory_path}'\n")
        parse_directory(args.template, args.directory_path, args.report_name)
    elif args.filename and args.template:
        logger.warning(f"Parsing file '{args.filename}' using template '{args.template}'\n")
        parse_file(args.filename, args.template, print_console=True)
    elif args.filename and args.templates_list:
        logger.debug(f"Reading TextFSM templates list file '{args.templates_list}':\n")
        logger.warning(f"Parsing file '{args.filename}' using templates: '{args.templates_list}'")
        logger.warning(parse_file_many_templates(
            args.filename, 
            read_templates_list(args.templates_list),
            print_console=False))
    else:
        logger.warning('Please enter path to Directory of File')
    
