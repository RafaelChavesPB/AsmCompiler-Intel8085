class Line:
    def __init__(self, raw_line='', **kwarg):
        self.raw_line = raw_line
        self.line = kwarg.get('line')
        self.label = kwarg.get('label')
        self.cmd = kwarg.get('cmd')
        self.arg1 = kwarg.get('arg1')
        self.arg2 = kwarg.get('arg2')
        self.address = 0

    def __str__(self):
        line = f"{self.address}"
        line += " " + self.label + ": " if self.label else ""
        line += " " + self.cmd + " " if self.cmd else ""
        line += " " + str(self.arg1) + " " if self.arg1 else ""
        line += " " + str(self.arg2) if self.arg2 else ""
        return line + '\n'
