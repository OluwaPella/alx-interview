#!/usr/bin/python3
"""A script for parsing HTTP request logs.
"""
import re

def parse_log_line(log_line):
    """Parses a line of an HTTP request log and extracts relevant information.

    Args:
        log_line (str): A line from the HTTP request log.

    Returns:
        dict: A dictionary containing status code and file size.
    """
    pattern = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)'
    )
    log_fmt = '{}\\-{}{}{}{}\\s*'.format(pattern[0], pattern[1], pattern[2],
                                         pattern[3], pattern[4])
    match = re.fullmatch(log_fmt, log_line)
    info = {
        'status_code': 0,
        'file_size': 0,
    }
    if match:
        info['status_code'] = match.group('status_code')
        info['file_size'] = int(match.group('file_size'))
    return info


def update_metrics(log_line, current_total_size, status_code_counts):
    """Updates the metrics based on a given HTTP request log line.

    Args:
        log_line (str): A line from the HTTP request log.
        current_total_size (int): The current total file size.
        status_code_counts (dict): Dictionary counts for each status code.

    Returns:
        int: The new total file size.
    """
    log_info = parse_log_line(log_line)
    status_code = log_info.get('status_code', '0')
    if status_code in status_code_counts.keys():
        status_code_counts[status_code] += 1
    new_total_size = current_total_size + log_info['file_size']
    return new_total_size


def print_statistics(total_file_size, status_codes_counts):
    """Prints the accumulated statistics of the HTTP request log.

    Args:
        total_file_size (int): The total file size.
        status_code_counts (dict): Dictionary counts for each status code.
    """
    print('File size: {:d}'.format(total_file_size), flush=True)
    for status_code in sorted(status_codes_counts.keys()):
        num = status_codes_counts.get(status_code, 0)
        if num > 0:
            print('{:s}: {:d}'.format(status_code, num), flush=True)


def start_log_parser():
    """Starts the log parser.
    """
    line_num = 0
    total_file_size = 0
    status_codes_stats = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    try:
        while True:
            line = input()
            total_file_size = update_metrics(
                line,
                total_file_size,
                status_codes_stats,
            )
            line_num += 1
            if line_num % 10 == 0:
                print_statistics(total_file_size, status_codes_stats)
    except (KeyboardInterrupt, EOFError):
        print_statistics(total_file_size, status_codes_stats)


if __name__ == '__main__':
    start_log_parser()