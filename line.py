class Line:
    def __init__(self, **kwarg):
        self.line = kwarg.get('line')
        self.label = kwarg.get('label')
        self.cmd = kwarg.get('cmd')
        self.arg1 = kwarg.get('arg1')
        self.arg2 = kwarg.get('arg2')
        self.address = 0

    def __str__(self):
        line = f"{self.address} - "
        line += self.label + ": " if self.label else ""
        line += self.cmd + " " if self.cmd else ""
        line += self.arg1 + " " if self.arg1 else ""
        line += self.arg2 if self.arg2 else ""
        return line + '\n'