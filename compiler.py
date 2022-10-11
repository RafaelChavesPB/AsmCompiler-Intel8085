#!/usr/bin/python3

from distutils.cmd import Command
import re
from line import Line
import constants 


class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.labels = {}
        self.lines = []
        
    def identifyLabels(self):
        curr_address = 0
        for line in self.lines:
            line.address = curr_address
            if line.label:
                self.labels[line.label] = curr_address
            if line.cmd:
                if line.cmd in constants.command_size:
                    curr_address += constants.command_size[line.cmd]
                elif line.cmd == 'db':
                    pass
                elif line.cmd == 'equ':
                    pass
                elif line.cmd == 'ds':
                    pass
                elif line.cmd == 'org':
                    pass
                else:
                    raise SyntaxError(f'Invalid command at line {line.line} -> "{line.cmd}"')
            else:
                curr_address += 1

    def getLines(self):
        with open(self.filename+'.asm', 'r') as file:
            for index, line in enumerate(file, start=1):
                line = line.lower()
                if not line or re.match(constants.patterns[-1], line):
                    continue
                for p in constants.patterns[:-1]:
                    match = re.match(p, line)
                    if match:
                        self.lines.append(Line(**match.groupdict()))
                        break
                else:
                    raise SyntaxError(
                        f'Invalid syntax at line {index} -> "{line.strip()}".')
       
    def compile(self):
        try:
            self.getLines()
            self.identifyLabels()
            print(*self.lines)
            print(self.labels)
        except FileNotFoundError:
            print(f'File "{self.filename}.asm" not found.')
        except Exception as err:
            print(err)