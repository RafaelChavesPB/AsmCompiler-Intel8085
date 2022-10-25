from line import Line
from functions import *
import constants


def opcode_(opcode: str, line: Line):
    if line.arg1 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')
    return [opcode]


def opcode_data(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    data = decimalToBinary(verifyNumber(line.arg1, line)).zfill(8)
    if len(data) > 8:
        raise SyntaxError(
            f'Syntax Error: Overflow number at line {line.line} -> "{line.raw_line.strip()}')
    return [opcode, data]


def opcode_ddd(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    if line.arg1 not in constants.registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')
    return [opcode1 + constants.registers[line.arg1] + opcode2]


def opcode_ddd_data(opcode1: str, opcode2: str, line: Line):
    data = decimalToBinary(verifyNumber(line.arg2, line)).zfill(8)
    if len(data) > 8:
        raise SyntaxError(
            f'Syntax Error: Overflow number at line {line.line} -> "{line.raw_line.strip()}')

    if line.arg1 not in constants.registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')
    return [opcode1 + constants.registers[line.arg1] + opcode2, data]


def opcode_ddd_sss(opcode1: str, line: Line):
    if line.arg1 not in constants.registers or line.arg2 not in constants.registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')
    return [opcode1 + constants.registers[line.arg1] + constants.registers[line.arg2]]


def opcode_double_data(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    data = decimalToBinary(verifyNumber(line.arg1, line)).zfill(16)
    if len(data) > 16:
        raise SyntaxError(
            f'Syntax Error: Overflow number at line {line.line} -> "{line.raw_line.strip()}')
    return [opcode, data[8:16], data[0:8]]


def opcode_r(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    if line.arg1 not in {'b', 'd'}:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    return [opcode1 + ('0' if line.arg1 == 'b' else '1') + opcode2]


def opcode_rp(opcode1: str, opcode2: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    if line.arg1 not in constants.double_registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    return [opcode1 + constants.double_registers[line.arg1] + opcode2]


def opcode_rp_double_data(opcode1: str, opcode2: str, line: Line):

    data = decimalToBinary(verifyNumber(line.arg2, line)).zfill(16)
    if len(data) > 16:
        raise SyntaxError(
            f'Syntax Error: Overflow number at line {line.line} -> "{line.raw_line.strip()}')

    if line.arg1 not in constants.double_registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    return [opcode1 + constants.double_registers[line.arg1] + opcode2, data[8:16], data[0:8]]


def opcode_sss(opcode: str, line: Line):
    if line.arg2 is not None:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')

    if line.arg1 not in constants.registers:
        raise SyntaxError(
            f'Syntax Error: Invalid syntax at line {line.line} -> "{line.raw_line.strip()}"')
    return [opcode + constants.registers[line.arg1]]


def db_translater(line: Line):
    args = [decimalToBinary(verifyNumber(num, line)).zfill(8)
            for num in line.arg1.split(',')]
    values = []
    for arg in args:
        if len(arg) > 8:
            raise SyntaxError(
                f'Syntax Error: Overflow number at line {line.line} -> "{line.raw_line.strip()}')
        values.append(arg)
    return values


def ds_translater(line: Line):
    return ['00000000' for it in range(verifyNumber(line.arg1, line))]


translater = {
    'aci': lambda line: opcode_data('11001110', line),
    'adc': lambda line: opcode_sss('10001', line),
    'add': lambda line: opcode_sss('10000', line),
    'adi': lambda line: opcode_data('11000110', line),
    'ana': lambda line: opcode_sss('10100', line),
    'ani': lambda line: opcode_data('11100110', line),
    'call': lambda line: opcode_double_data('11001101', line),
    'cc': lambda line: opcode_double_data('11011100', line),
    'cm': lambda line: opcode_double_data('11111100', line),
    'cma': lambda line: opcode_('00101111', line),
    'cmc': lambda line: opcode_('00111111', line),
    'cmp': lambda line: opcode_sss('10111', line),
    'cnc': lambda line: opcode_double_data('11010100', line),
    'cnz': lambda line: opcode_double_data('11000100', line),
    'cp': lambda line: opcode_double_data('11110100', line),
    'cpe': lambda line: opcode_double_data('11101100', line),
    'cpi': lambda line: opcode_data('11111110', line),
    'cpo': lambda line: opcode_double_data('11100100', line),
    'cz': lambda line: opcode_double_data('11001100', line),
    'daa': lambda line: opcode_('00100111', line),
    'dad': lambda line: opcode_rp('00', '1001', line),
    'dcr': lambda line: opcode_ddd('00', '101', line),
    'dcx': lambda line: opcode_rp('00', '1011', line),
    'di': lambda line: opcode_('11110011', line),
    'ei': lambda line: opcode_('11111011', line),
    'hlt': lambda line: opcode_('01110110', line),
    'in': lambda line: opcode_data('11011011', line),
    'inr': lambda line: opcode_ddd('00', '100', line),
    'inx': lambda line: opcode_rp('00', '0011', line),
    'jc': lambda line: opcode_double_data('11011010', line),
    'jm': lambda line: opcode_double_data('11111010', line),
    'jmp': lambda line: opcode_double_data('11000011', line),
    'jnc': lambda line: opcode_double_data('11010010', line),
    'jnz': lambda line: opcode_double_data('11000010', line),
    'jp': lambda line: opcode_double_data('11110010', line),
    'jpe': lambda line: opcode_double_data('11101010', line),
    'jpo': lambda line: opcode_double_data('11100010', line),
    'jz': lambda line: opcode_double_data('11001010', line),
    'lda': lambda line: opcode_double_data('00111010', line),
    'ldax': lambda line: opcode_r('000', '1010', line),
    'lhld': lambda line: opcode_double_data('00101010', line),
    'lxi': lambda line: opcode_rp_double_data('00', '0001', line),
    'mov': lambda line: opcode_ddd_sss('01', line),
    'mvi': lambda line: opcode_ddd_data('00', '110', line),
    'nop': lambda line: opcode_('00000000', line),
    'ora': lambda line: opcode_sss('10110', line),
    'ori': lambda line: opcode_data('11110110', line),
    'out': lambda line: opcode_data('11010011', line),
    'pchl': lambda line: opcode_('11101001', line),
    'pop': lambda line: opcode_rp('11', '0001', line),
    'push': lambda line: opcode_rp('11', '0101', line),
    'ral': lambda line: opcode_('00010111', line),
    'rar': lambda line: opcode_('00011111', line),
    'rc': lambda line: opcode_('01010101', line),
    'ret': lambda line: opcode_('11001001', line),
    'rim': lambda line: opcode_('00100000', line),
    'rlc': lambda line: opcode_('00000111', line),
    'rm': lambda line: opcode_('11111000', line),
    'rnc': lambda line: opcode_('11010000', line),
    'rnz': lambda line: opcode_('11000000', line),
    'rp': lambda line: opcode_('11110000', line),
    'rpe': lambda line: opcode_('11101000', line),
    'rpo': lambda line: opcode_('11100000', line),
    'rrc': lambda line: opcode_('00001111', line),
    'rst': lambda line: opcode_ddd('11', '111', line),
    'rz': lambda line: opcode_('11001000', line),
    'sbb': lambda line: opcode_sss('10011', line),
    'sbi': lambda line: opcode_data('11011110', line),
    'shld': lambda line: opcode_double_data('00100010', line),
    'sim': lambda line: opcode_('00110000', line),
    'sphl': lambda line: opcode_('11111001', line),
    'sta': lambda line: opcode_double_data('00110010', line),
    'stax': lambda line: opcode_r('000', '0010', line),
    'stc': lambda line: opcode_('00110111', line),
    'sub': lambda line: opcode_sss('10010', line),
    'sui': lambda line: opcode_data('11010110', line),
    'xchg': lambda line: opcode_('11101011', line),
    'xra': lambda line: opcode_sss('10101', line),
    'xri': lambda line: opcode_data('11101110', line),
    'xthl': lambda line: opcode_('11100011', line),
    'db': lambda line: db_translater(line),
    'ds': lambda line: ds_translater(line),
    'org': lambda line: ['00000000'] if line.label else [],
    'equ': lambda line: []
}
