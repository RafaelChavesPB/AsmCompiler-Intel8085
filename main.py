#!/usr/bin/python3
import sys
import re
from command import Command

pattern = [
    r'^\s*(?P<label>\w+:)\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*,\s*(?P<arg3>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>\w+:)\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>\w+:)\s*(?P<arg1>\w+)\s+(?:;[\w\s\W]*)?$',
    r'^\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*,\s*(?P<arg3>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<arg1>\w+)\s+(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<arg1>\w+)\s+(?:;[\w\s\W]*)?$',
    r'^\s*(?:;[\w\s\W]*)?$'
]

filename = sys.argv[1] if len(sys.argv) > 1 else input('Asm file name: ')
try:
    with open(filename+'.asm', 'r') as file:
        for index, line in enumerate(file, start=1):
            if not line or re.match(pattern[-1], line):
                continue
            for p in pattern[:-1]:
                match = re.match(p, line)
                if match:
                    print(Command(**match.groupdict()))
                    break
            else:
                raise SyntaxError(f'Invalid syntax at line {index} -> "{line.strip()}".')
except FileNotFoundError:
    print(f'File "{filename}.asm" not found.')
except Exception as err:
    print(err)
