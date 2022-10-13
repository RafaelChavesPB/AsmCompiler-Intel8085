#!/usr/bin/python3

import re
from functions import *
from translaters import translater
from line import Line
import constants

# TO DO
'''
    Remover diretivas org e equ das linhas
'''


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
                        self.lines.append(
                            Line(**match.groupdict(), line=index))
                        break
                else:
                    raise SyntaxError(f'Invalid syntax at line {index}.')

    def identifyLabels(self):
        curr_address = 0
        for line in self.lines:
            line.address = curr_address
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
                    curr_address += verifyNumber(line.arg1, line.line)
                elif line.cmd == 'equ':
                    if line.label in constants.commands or line.label in constants.directives or line.label in constants.registers:
                        raise SyntaxError(
                            f'Label using protect words at line {line.line}')
                    self.equ[line.label] = line.arg1
                elif line.cmd == 'org':
                    curr_address = verifyNumber(line.arg1, line.line)
                    line.address = curr_address
                    if line.label:
                        self.labels[line.label] = curr_address
                    curr_address += 1

                else:
                    raise SyntaxError(
                        f'Invalid command at line {line.line}')

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

    def tranlateToBinary(self):
        for line in self.lines:
            if line.cmd in constants.commands:
                print(translater[line.cmd](line))

    def compile(self):
        self.getLines()
        print(*self.lines)
        self.identifyLabels()
        print(*self.lines)
        self.replacingLabels()
        print(*self.lines)
        self.tranlateToBinary()
        try:
            pass
        except FileNotFoundError:
            print(f'File "{self.filename}.asm" not found.')
        except Exception as err:
            print(err)
