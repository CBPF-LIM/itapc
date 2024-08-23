import sys
import pdb

def b():
    pdb.Pdb().set_trace(sys._getframe(1))
