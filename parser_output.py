#!/usr/bin/python3

import csv
import logging
import os
from argparse import ArgumentParser
from datetime import datetime

import textfsm
from tabulate import tabulate

# from ReportExcel import ReportExcel

__author__ = 'Ravil Shamatov, ravil.shamatov@huawei.com, rav.shamatov@gmail.com'
SCRIPT_DESCRIPTION = f"""This is TextFSM parser that get all needed information and output to CSV report.
Author: {__author__}. Version: 2020-04-16"""

CSV_DELIMETER = ','
logger = logging.getLogger('parser')
LOGGING_LEVELS = {
    0: logging.INFO,
    1: logging.DEBUG
}
LOG_FILENAME = 'parser_output.log'


def parse_file(output_filename, template_filename, print_console=False):
    """ Parse text file using one TextFSM template

    Arguments:
        output_filename {str} -- text file for parsing
        template_filename {str} -- TextFSM template filename

    Keyword Arguments:
        print_console {bool} -- if True - print to console (default: {False})

    Returns:
        [list of list of str] -- result table
    """    
    with open(template_filename) as t, open(output_filename, 'r') as output:
        re_table = textfsm.TextFSM(t)
        result_table = re_table.ParseText(output.read())
        if print_console:
            header = re_table.header
            logger.warning('\n' + tabulate(result_table), headers=header)
        return result_table


def parse_file_many_templates(output_filename, template_filenames, print_console=False):
    """ Parse file using list of TextFSM templates

    Arguments:
        output_filename {str} -- text for parsing
        template_filenames {list of str} -- filenames of TextFSM templates

    Keyword Arguments:
        print_console {bool} -- if True - return tabulated result with header (default: {False})

    Returns:
        [list of list of str] -- result
    """    
    result_rows = [[]]
    header = read_template_headers(template_filenames)

    logger.debug(f"File '{output_filename}' - opened")
    for template in template_filenames:
        logger.debug(f"File '{output_filename}' - template '{template}'")
        rows = parse_file(output_filename, template, False)
        logger.debug(f"Result: {rows}")
        ''' Concatenating results '''
        try:
            result_rows = extend_results(result_rows, rows)
            if not rows:
                logger.warning(
                    f"File '{output_filename}' - template '{template}' - matches not found")
            logger.debug(f"Total file result: {result_rows}")
        except IndexError:
            logger.info(f"File '{output_filename}' - template '{template}' - matches not found")
        logger.debug(f"Summary result: {result_rows}")
        logger.warning(f"File '{output_filename}' - done")
    return tabulate(result_rows, headers=header) if print_console else result_rows


def extend_results(table1, table2):
    """ Concatenate result of parsing by different TextFSM templates

    Arguments:
        table1 {list of list of str} -- output of parsing by TextFSM template #1
        table2 {list of list of str} -- output of parsing by TextFSM template #2

    Returns:
        [list of list of str] -- Result
    """    
    temp_table = []
    if len(table1) == len(table2):
        for line, row in zip(table1, table2):
            logger.debug(f"Extending line {line} + row {row}")
            temp_table.append(line + row)
    elif table2:
        for line in table1:
            for row in table2:
                logger.debug(f"Appending line {line} + row {row}")
                temp_table.append(line + row)
    else:
        return table1
    return temp_table


def write_csv_row(filename, row):
    """ Write row to CSV file

    Arguments:
        filename {str} -- CSV filename
        row {list of str} -- Row that will be written
    """    
    with open(filename, mode='a') as f:
        writer = csv.writer(f, quotechar='"', delimiter=CSV_DELIMETER)
        writer.writerow(row)


def parse_directory(directory_path, template_filenames, report_name=None):
    """ Parse each file in directory with list of TextFSM templates

    Arguments:
        directory_path {str} -- path to logs directory
        template_filenames {str} -- filenames of TextFSM templates

    Keyword Arguments:
        report_name {str} -- CSV report filename (default: generated according datetime)
    """    
    report_name = report_name or datetime.today().strftime('report_%Y-%m-%d_%H-%M.csv')
    # CSV Header
    write_csv_row(report_name, ['FILENAME'] + read_template_headers(template_filenames))
    # Parsing every file in directory and write result to CSV report
    for filename in os.listdir(directory_path):
        for row in parse_file_many_templates(os.path.join(directory_path, filename), template_filenames):
            write_csv_row(report_name, [filename] + row)
    logger.warning(f"Report filename: {report_name}")


def read_templates_list(filename):
    """ Read file with TextFSM templates and return list of filenames.

    Arguments:
        filename {str} -- path+filename of text file that contains list of TextFSM filenamess

    Returns:
        [list of str] -- list of absolute paths to TextFSM filenames
    """
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


def read_template_headers(template_filenames):
    """ Read summary header from all TextFSM templates

    Arguments:
        template_filenames {list of str} -- filenames of TextFSM tempates

    Returns:
        [list of str] -- summary header ([SYSNAME, VERSION, HARDWARE, etc..])
    """    
    logger.debug(f'Reading header for templates {template_filenames}')
    template_headers = []
    for filename in template_filenames:
        with open(filename) as t:
            header = textfsm.TextFSM(t).header
            logger.debug(f"Template '{filename}' - header {header}")
            template_headers.extend(header)
        '''except:
            logger.error(
                "Error during reading header from TextFSM template '{filename}'", exc_info=True)
        '''
    logger.debug(f"Total header: {template_headers}")
    return template_headers


def read_arguments():
    """ Parse script arguments

    Returns:
        [namespace] -- all entered arguments
    """    
    parser = ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('-D', '--directory_path', help='Absolute or relative path to directory', required=False)
    parser.add_argument('-f', '--filename', help='Absolute or relative path to text file', required=False)
    parser.add_argument('-t', '--template', help='Absolute or relative path to TextFSM template', required=False)
    parser.add_argument('-tl', '--templates_list', help='Absolute or relative path to TextFSM templates list', required=False)
    parser.add_argument('-R', '--report_name', help='Report name', required=False)
    parser.add_argument('-V', '--verbose', action='count', default=0)
    return parser.parse_args()


def configure_logging(logging_level):
    """ Configure logging (console and to file)

    Arguments:
        logging_level {int} -- level of logging (10/20/30/40/50)
    """    
    logger.setLevel(logging_level)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level + logging.DEBUG)
    ch.setFormatter(
        logging.Formatter('%(message)s'))

    fh = logging.FileHandler(LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter('%(asctime)s:%(name)s:%(levelname)s\t%(message)s'))

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('')
    logger.info(f"Logging level '{logging_level}', handlers {logger.handlers}")


if __name__ == '__main__':
    """ Main function:
        1. Parse one file by one template 
            >>> ./parser_output.py -t display_elabel.template -f filename.log
        2. Parse all files in directory by one template
            >>> ./parser_output.py -t display_elabel.template -D data2
        3. Parse one file by several templates
            >>> ./parser_output.py -tl file-with-templates-list.txt -f filename.log
        4. Parse all files in directory by several templates
            >>> ./parser_output.py -tl file-with-templates-list.txt -D data2
    """
    args = read_arguments()
    # If no -V arg          then file logging level is INFO
    # If arg is -V or -VV   then file logging level is DEBUG
    configure_logging(LOGGING_LEVELS.get(args.verbose, logging.DEBUG))

    logger.info(f"Starting parser with arguments {args}")
    if args.directory_path and args.template:
        logger.warning(f"Parsing all files from directory '{args.directory_path}'")
        parse_directory(args.directory_path, [args.template], args.report_name)
    elif args.filename and args.template:
        logger.warning(f"Parsing file '{args.filename}' using template '{args.template}'")
        parse_file(args.filename, args.template, print_console=True)
    elif args.filename and args.templates_list:
        logger.warning(f"Parsing file '{args.filename}' using templates: '{args.templates_list}'")
        logger.warning(parse_file_many_templates(
            args.filename,
            read_templates_list(args.templates_list),
            print_console=True))
    elif args.directory_path and args.templates_list:
        logger.warning(f"Parsing all files from directory '{args.directory_path}'")
        template_filenames = read_templates_list(args.templates_list)
        parse_directory(args.directory_path, template_filenames, args.report_name)
    else:
        logger.warning('Please enter path to Directory of File')
