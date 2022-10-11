import re
from constants import *


def isHex(num: str) -> str:
    match = re.match(r'^(0[0-9a-f]+)h$', num)
    if match:
        return match.group(1)
    return None


def isBinary(num: str) -> str:
    match = re.match(r'^([0-1]+)b$', num)
    if match:
        return match.group(1)
    return None


def isOctal(num: str) -> str:
    match = re.match(r'^([0-7]+)[q|o]$', num)
    if match:
        return match.group(1)
    return None


def isDecimal(num: str) -> int:
    match = re.match(r'^([0-9]+)d?$', num)
    if match:
        return match.group(1)
    return None


def decimalToBinary(num: int):
    bin = ''
    while num > 0:
        bin += ('1' if num & 1 else '0') 
        num = num >> 1
    return bin[::-1] if bin else '0'


def octalToDecimal(num: str) -> int:
    dec = 0
    num = num[::-1]
    for i in range(len(num)):
        dec += int(num[i])*8**i
    return dec


def hexToDecimal(num: str) -> int:
    table = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    dec = 0
    num = num[::-1]
    for i in range(len(num)):
        dec += (table[num[i]] if num[i] in table else int(num[i]))*16**i
    return dec


def decimalToHex(num: int) -> str:
    table = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hex = ''
    while num > 0:
        res = num % 16
        hex += (table[res] if res in table else str(res)) 
        num = num >> 4
    hex = hex[::-1]
    hex = hex.zfill(len(hex)+len(hex)%2)
    return '0x'+ (hex.upper() if hex else '00')

def octalToBinary(num: str) -> str:
    dec = octalToDecimal(num)
    binary = decimalToBinary(dec)
    return binary


def hexToBinary(num: str) -> str:
    dec = hexToDecimal(num)
    binary = decimalToBinary(dec)
    return binary


def verifyNumber(num: str, line: int):
    data = ''
    if isHex(num):
        data = octalToBinary(isHex(num))
    elif isOctal(num):
        data = octalToBinary(isOctal(num))
    elif isBinary(line):
        data = isBinary(line)
    elif isDecimal(num):
        data = decimalToBinary(isDecimal(num))
    else:
        raise SyntaxError(f'Number not valid at line {line.line} -> {num}')
    return data
