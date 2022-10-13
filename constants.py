
directives = {
    'db', 'ds', 'equ', 'org'
}

commands = {
    'aci': 2,
    'adc': 1,
    'add': 1,
    'adi': 2,
    'ana': 1,
    'ani': 2,
    'call': 3,
    'cc': 3,
    'cm': 3,
    'cma': 1,
    'cmc': 1,
    'cmp': 1,
    'cnc': 3,
    'cnz': 3,
    'cp': 3,
    'cpe': 3,
    'cpi': 2,
    'cpo': 3,
    'cz': 3,
    'daa': 1,
    'dad': 1,
    'dcr': 1,
    'dcx': 1,
    'di': 1,
    'ei': 1,
    'hlt': 1,
    'in': 2,
    'inr': 1,
    'inx': 1,
    'jc': 3,
    'jm': 3,
    'jmp': 3,
    'jnc': 3,
    'jnz': 3,
    'jp': 3,
    'jpe': 3,
    'jpo': 3,
    'jz': 3,
    'lda': 3,
    'ldax': 1,
    'lhld': 3,
    'lxi': 3,
    'mov': 1,
    'mvi': 2,
    'nop': 1,
    'ora': 1,
    'ori': 2,
    'out': 2,
    'pchl': 1,
    'pop': 1,
    'push': 1,
    'ral': 1,
    'rar': 1,
    'rc': 1,
    'ret': 1,
    'rim': 1,
    'rlc': 1,
    'rm': 1,
    'rnc': 1,
    'rnz': 1,
    'rp': 1,
    'rpe': 1,
    'rpo': 1,
    'rrc': 1,
    'rst': 1,
    'rz':1,
    'sbb': 1,
    'sbi': 2,
    'shld': 3,
    'sim': 1,
    'sphl': 1,
    'sta': 3,
    'stax': 1,
    'stc':  1,
    'sub': 1,
    'sui': 1,
    'xchg': 1,
    'xra': 1,
    'xri': 2,
    'xthl': 1,
}

patterns = [
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<cmd>db)\s+(?P<arg1>(?:\s*\w+\s*,\s*)+(?:\s*\w+)+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*)\s*(?P<cmd>equ)\s+(?P<arg1>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<cmd>\w+)\s+(?P<arg1>\w+)\s*,\s*(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<cmd>\w+)\s+(?P<arg1>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<label>[a-z]\w*):\s*(?P<cmd>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<cmd>\w+)\s+(?P<arg1>\w+)\s*,\s*(?P<arg2>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<cmd>\w+)\s+(?P<arg1>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?P<cmd>\w+)\s*(?:;[\w\s\W]*)?$',
    r'^\s*(?:;[\w\s\W]*)?$',
]

registers = {'a': '111', 'b': '000', 'c': '001',
             'd': '010', 'e': '011', 'h': '100', 'l': '101', 'm': '110'}

double_registers = {'b': '00', 'd': '01', 'h':'10', 'sp':'11'}


