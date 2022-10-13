#!/usr/bin/python3

from distutils.cmd import Command
import re
from functions import verifyNumber
from line import Line
import constants 


class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.labels = {}
        self.equ = {}
        self.lines = []

    def getLines(self):
        with open(self.filename+'.asm', 'r') as file:
            for index, line in enumerate(file, start=1):
                line = line.lower()
                if not line or re.match(constants.patterns[-1], line):
                    continue
                for p in constants.patterns[:-1]:
                    match = re.match(p, line)
                    if match:
                        self.lines.append(Line(**match.groupdict(), line = index))
                        break
                else:
                    raise SyntaxError(
                        f'Invalid syntax at line {index} -> "{line.strip()}".')
       

    def identifyLabels(self):
        curr_address = 0
        for line in self.lines:
            line.address = curr_address
            if line.cmd:
                if line.cmd in constants.command_size:
                    if line.label:
                        self.labels[line.label] = curr_address
                    curr_address += constants.command_size[line.cmd]
                elif line.cmd == 'db':
                    self.labels[line.label] = curr_address
                    curr_address += len(line.arg1.split(','))
                elif line.cmd == 'ds':
                    self.labels[line.label] = curr_address
                    curr_address += verifyNumber(line.arg1, line.line)
                elif line.cmd == 'equ':
                    self.equ[line.label] = line.arg1
                elif line.cmd == 'org':
                    if line.label:
                        self.labels[line.label] = curr_address
                    curr_address = verifyNumber(line.arg1,line.line)

                else:
                    raise SyntaxError(f'Invalid command at line {line.line} -> "{line.cmd}"')
                
            else:
                if line.label:
                    self.labels[line.label] = curr_address
                    curr_address += 1


    def compile(self):
        self.getLines()
        self.identifyLabels()
        print(*self.lines)
        print(self.labels)
        try:
            pass
        except FileNotFoundError:
            print(f'File "{self.filename}.asm" not found.')
        except Exception as err:
            print(err)