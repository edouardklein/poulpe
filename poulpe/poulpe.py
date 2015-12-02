# -*- coding: utf-8 -*-
"""Usage:
poulpe init
"""
from docopt import docopt
import os
import logging
from poulpe import cmd

logging.basicConfig(level=logging.INFO)


def init():
    '''Install the Poulpe's hooks and scripts.'''
    src_dir = os.path.dirname(os.path.realpath(__file__))
    dst_dir = os.getcwd()
    logging.info('Creating a new case')
    cmd('git init')
    cmd('git remote add origin '+src_dir)
    cmd('git fetch')
    cmd('git checkout -t origin/master')
    cmd('ln -s '+src_dir+'/poulpe/post-commit ' + dst_dir +
        '/.git/hooks/')
    cmd('mkdir '+dst_dir+'/.git/artefacts')
    cmd('ln -s '+src_dir+'/src/artefacts/* '+dst_dir+'/.git/artefacts/')


def main():
    arguments = docopt(__doc__)
    if arguments['init']:
        init()
