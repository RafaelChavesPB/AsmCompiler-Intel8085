#!/usr/bin/python3
import sys
import re
from line import Line


class Compiler:

    patterns = [
        r'^\s*(?P<label>\w+):\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*,\s*(?P<arg3>\w+)\s*(?:;[\w\s\W]*)?$',
        r'^\s*(?P<label>\w+):\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
        r'^\s*(?P<label>\w+):\s*(?P<arg1>\w+)\s+(?:;[\w\s\W]*)?$',
        r'^\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*,\s*(?P<arg3>\w+)\s*(?:;[\w\s\W]*)?$',
        r'^\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
        r'^\s*(?P<arg1>\w+)\s+(?:;[\w\s\W]*)?$',
        r'^\s*(?:;[\w\s\W]*)?$'
    ]

    registers = {'A': 0, 'B': 1, 'C': 2,
                 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

    def __init__(self):
        pass

    def compile(self):
        filename = sys.argv[1] if len(
            sys.argv) > 1 else input('Asm file name: ')
        try:
            with open(filename+'.asm', 'r') as file:
                for index, line in enumerate(file, start=1):
                    if not line or re.match(self.pattern[-1], line):
                        continue
                    for p in self.pattern[:-1]:
                        match = re.match(p, line)
                        if match:
                            print(Line(**match.groupdict()))
                            break
                    else:
                        raise SyntaxError(
                            f'Invalid syntax at line {index} -> "{line.strip()}".')
        except FileNotFoundError:
            print(f'File "{filename}.asm" not found.')
        except Exception as err:
            print(err)
