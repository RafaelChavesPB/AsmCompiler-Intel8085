#!/usr/bin/python3

import re
from functions import *
from translaters import translater
from line import Line
import constants

# TO DO
'''
   ORG
'''


class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.labels = {}
        self.equ = {}
        self.lines = []
        self.binary_code = {}

    def getLines(self):
        with open(self.filename+'.asm', 'r') as file:
            for index, line in enumerate(file, start=1):
                line = line.lower()
                if not line or re.match(constants.patterns[-1], line):
                    continue
                for p in constants.patterns[:-1]:
                    match = re.match(p, line)
                    if match:
                        self.lines.append(
                            Line(**match.groupdict(), line=index, raw_line=line))
                        break
                else:
                    raise SyntaxError(f'Syntax Error: Invalid syntax at line {index} -> "{line.strip()}"')

    def identifyLabels(self):
        curr_address = 0
        for line in self.lines:
            if curr_address >= 256*256:
                raise MemoryError(
                    f'Memory Error: Segmentation fault (core dumped), inadequated memory address ({decimalToHex(curr_address)}) assigned to line {line.line} -> "{line.raw_line.strip()}"')

            line.address = curr_address
            if line.label and line.label in self.labels:
                raise SyntaxError(
                            f'Syntax Error: Redefing label at line {line.line} -> "{line.raw_line.strip()}"')
            if line.cmd:
                if line.cmd in constants.commands:
                    if line.label:
                        self.labels[line.label] = curr_address
                    curr_address += constants.commands[line.cmd]
                elif line.cmd == 'db':
                    self.labels[line.label] = curr_address
                    curr_address += len(line.arg1.split(','))
                elif line.cmd == 'ds':
                    self.labels[line.label] = curr_address
                    if line.arg1 in self.equ:
                        line.arg1 = self.equ[line.arg1]
                    curr_address += verifyNumber(line.arg1, line)
                elif line.cmd == 'equ':
                    if line.label in constants.commands or line.label in constants.directives or line.label in constants.registers:
                        raise SyntaxError(
                            f'Syntax Error: Using protect words as labels at line {line.line} -> "{line.raw_line.strip()}"')
                    self.equ[line.label] = line.arg1
                elif line.cmd == 'org':
                    line.address = curr_address
                    if line.label:
                        self.labels[line.label] = curr_address
                    curr_address = verifyNumber(line.arg1, line)
                    if curr_address >= 256*256:
                        raise MemoryError(
                            f'Memory Error: Segmentation fault (core dumped), inadequated memory address ({decimalToHex(curr_address)}) assigned at line {line.line} -> "{line.raw_line.strip()}"')
                else:
                    raise SyntaxError(
                        f'Syntax Error: Invalid command at line {line.line}')
            else:
                if line.label:
                    self.labels[line.label] = curr_address
                    curr_address += 1

    def replacingLabels(self):
        for line in self.lines:
            if line.cmd in constants.commands:
                if line.arg1 is not None:
                    if line.arg1 in self.labels:
                        line.arg1 = self.labels[line.arg1]
                    elif line.arg1 in self.equ:
                        line.arg1 = self.equ[line.arg1]
                if line.arg2 is not None:
                    if line.arg2 in self.labels:
                        line.arg2 = self.labels[line.arg2]
                    elif line.arg2 in self.equ:
                        line.arg2 = self.equ[line.arg2]
            elif line.cmd == 'ds' or line.cmd == 'org':
                if line.arg1 in self.equ:
                    line.arg1 = self.equ[line.arg1]
            elif line.cmd == 'db':
                args = [self.equ[arg.strip()] if arg.strip(
                ) in self.equ else arg for arg in line.arg1.split(',')]
                line.arg1 = ','.join(args)

    def tranlateToBinary(self):
        top_address = 0
        for line in self.lines:
            if line.cmd:
                cmd_bytes = translater[line.cmd](line)
            else:
                cmd_bytes = ['00000000']
            curr_address = line.address
            top_address = max(curr_address + len(cmd_bytes), top_address)
            for it in range(len(cmd_bytes)):
                self.binary_code[curr_address + it] = [cmd_bytes[it], line]

        for it in range(top_address):
            if it not in self.binary_code:
                self.binary_code[it] = ['00000000', None]

    def saveBinaryCode(self):
        with open(self.filename+'.txt', 'w') as file:
            file.write(
                f'{"Memory":10} {"Opcode":10} {"Line":6}  {"Instruction Souce":30} \n')
            for it in range(len(self.binary_code)):
                if self.binary_code[it][1] is not None:
                    file.write(
                        f'{decimalToHex(it):10} {self.binary_code[it][0]:10} {self.binary_code[it][1].line:4}    {self.binary_code[it][1].raw_line:30}\n')
        with open(self.filename+'.bin', 'w') as file:
            for it in range(len(self.binary_code)):
                file.write(self.binary_code[it][0]+'\n')

    def compile(self):
        try:
            self.getLines()
            self.identifyLabels()
            self.replacingLabels()
            self.tranlateToBinary()
            self.saveBinaryCode()
            pass
        except FileNotFoundError:
            print(f'File "{self.filename}.asm" not found.')
        except Exception as err:
            print(err)
