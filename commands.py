from line import Line
from functions import *
from constants import * 

def opcode_data(opcode:str, line: Line):
    data = decimalToBinary(verifyNumber(line.arg1, line.line))
    if len(data) > 8:
        raise OverflowError(f'Overflow number at line {line.line} -> "{line.arg1}')
    return [opcode, data.zfill(8)]

def opcode_(opcode:str, line: Line):
    return opcode

def opcode_reg(opcode:str, line: Line):
    if line.arg1 in registers:
        return 