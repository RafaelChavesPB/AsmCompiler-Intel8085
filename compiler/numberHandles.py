import re
from .constants import *
from .line import Line


def isHex(num: str) -> str:
    match = re.match(r'^\s*(0[0-9a-f]*)h\s*$', num)
    if match:
        return match.group(1)
    return None


def isBinary(num: str) -> str:
    match = re.match(r'^\s*([0-1]+)b\s*$', num)
    if match:
        return match.group(1)
    return None


def isOctal(num: str) -> str:
    match = re.match(r'^\s*([0-7]+)[q|o]\s*$', num)
    if match:
        return match.group(1)
    return None


def isDecimal(num: str) -> int:
    if isinstance(num, int):
        return num
    match = re.match(r'^\s*([0-9]+)d?\s*$', num)
    if match:
        return int(match.group(1))
    return None


def octalToDecimal(num: str) -> int:
    dec = 0
    num = num[::-1]
    for i in range(len(num)):
        dec += int(num[i])*8**i
    return dec


def binaryToDecimal(num: str):
    dec = 0
    num = num[::-1]
    for i in range(len(num)):
        dec += int(num[i])*2**i
    return dec


def hexToDecimal(num: str) -> int:
    table = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    dec = 0
    num = num[::-1]
    for i in range(len(num)):
        dec += (table[num[i]] if num[i] in table else int(num[i]))*16**i
    return dec


def decimalToBinary(num: int):
    bin = ''
    while num > 0:
        bin += ('1' if num & 1 else '0')
        num = num >> 1
    return bin[::-1] if bin else '0'


def decimalToHex(num: int) -> str:
    table = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hex = ''
    while num > 0:
        res = num % 16
        hex += (table[res] if res in table else str(res))
        num = num >> 4
    hex = hex[::-1]
    hex = hex.zfill(len(hex)+len(hex) % 2)
    return '0x' + (hex.upper() if hex else '00')


def octalToBinary(num: str) -> str:
    dec = octalToDecimal(num)
    binary = decimalToBinary(dec)
    return binary


def hexToBinary(num: str) -> str:
    dec = hexToDecimal(num)
    binary = decimalToBinary(dec)
    return binary


def verifyNumber(num: str, line: Line):
    data = ''
    if isDecimal(num) is not None:
        data = isDecimal(num)
    elif isHex(num) is not None:
        data = hexToDecimal(isHex(num))
    elif isOctal(num) is not None:
        data = octalToBinary(isOctal(num))
    elif isBinary(num) is not None:
        data = binaryToDecimal(isBinary(num))
    else:
        raise SyntaxError(
            f'Syntax Error: Number not valid at line {line.line} -> {line.raw_line.strip()}')
    return data
