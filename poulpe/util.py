'''Some utility functions shared by the rest of the code'''
import subprocess


def cmd(c):
    '''Run the command in a shell'''
    return subprocess.check_output(c, shell=True).decode('utf8')
