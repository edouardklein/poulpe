# -*- coding: utf-8 -*-
"""Usage:
poulpe init
"""
from docopt import docopt
import poulpe

def main():
    arguments = docopt(__doc__)
    if arguments['init']:
        print("INIT")
    print("END")
