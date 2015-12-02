# -*- coding: utf-8 -*-
import subprocess

__author__ = 'Edouard Klein'
__email__ = 'edou -at- rdklein.fr'
__version__ = '0.0.0'


def cmd(c):
    '''Run the command in a shell'''
    return subprocess.check_output(c, shell=True).decode('utf8')
