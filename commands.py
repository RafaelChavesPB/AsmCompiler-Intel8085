from unicodedata import decimal
from line import Line
from functions import *

def aci(line: Line):
    data = verifyNumber(line.arg1, line.line)
    if len(data) > 8:
        raise OverflowError(f'Overflow number at line {line.line} -> "{line.arg1}')
    return ['11001110', data.zfill(8)]