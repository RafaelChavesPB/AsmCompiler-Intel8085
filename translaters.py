from line import Line
from functions import *
import constants


def opcode_(opcode: str, line: Line):
    if line.arg1 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')
    return opcode


def opcode_sss(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    if line.arg1 in constants.registers:
        return [opcode + constants.registers[line.arg1]]


def opcode_ddd(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    if line.arg1 in constants.registers:
        return [opcode1 + constants.registers[line.arg1] + opcode2]


def opcode_ddd_sss(opcode1: str, line: Line):
    if line.arg1 not in constants.registers or line.arg2 not in constants.registers:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')
    return [opcode1 + constants.registers[line.arg1] + constants.registers[line.arg2]]


def opcode_rp(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    if line.arg1 not in constants.double_registers:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    return [opcode1 + constants.double_registers[line.arg1] + opcode2]


def opcode_r(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    if line.arg1 not in {'b': 'd'}:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    return [opcode1 + ('0' if line.arg1 == 'b' else '1') + opcode2]


def opcode_data(opcode1: str, opcode2: str, line: Line):
    data = decimalToBinary(verifyNumber(line.arg2, line.line)).zfill(8)
    if len(data) > 8:
        raise OverflowError(f'Overflow number at line {line.line}')

    if line.arg1 not in constants.registers:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')
    return [opcode1 + constants.registers[line.arg1] + opcode2, data]


def opcode_ddd_data(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    data = decimalToBinary(verifyNumber(line.arg1, line.line)).zfill(8)
    if len(data) > 8:
        raise OverflowError(f'Overflow number at line {line.line}')
    return [opcode, data]


def opcode_double_data(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    data = decimalToBinary(verifyNumber(line.arg1, line.line)).zfill(16)
    if len(data) > 16:
        raise OverflowError(f'Overflow number at line {line.line}')
    return [opcode, data[0:8], data[8:16]]


def opcode_rp_double_data(opcode1: str, opcode2: str, line: Line):

    data = decimalToBinary(verifyNumber(line.arg2, line.line)).zfill(16)
    if len(data) > 16:
        raise OverflowError(f'Overflow number at line {line.line}')

    if line.arg1 not in constants.double_registers:
        raise SyntaxError(f'Invalid syntax at line {line.line}.')

    return [opcode1 + constants.double_registers[line.arg1] + opcode2, data[0:8], data[8:16]]
