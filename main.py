#!/usr/bin/python3
import sys
from compiler import Compiler

comp = Compiler(sys.argv[1] if len(sys.argv) > 1 else input('filename: '))
comp.compile()