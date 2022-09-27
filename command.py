class Command:
    def __init__(self, **kwarg):
        self.label = kwarg.get('label')
        self.arg1 = kwarg.get('arg1')
        self.arg2 = kwarg.get('arg2')
        self.arg3 = kwarg.get('arg3')
    
    def __str__(self):
        line = ""
        line += self.label + " " if self.label else ""
        line += self.arg1 + " " if self.arg1 else ""
        line += self.arg2 if self.arg2 else ""
        line += ", " + self.arg3 if self.arg3 else ""
        return line