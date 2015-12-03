'''Some utility functions shared by the rest of the code'''
import subprocess


def cmd(c, raw=False):
    '''Run the command in a shell'''
    b = subprocess.check_output(c, shell=True)
    if not raw:
        return b.decode('utf8')
    return b


def lines(fname):
    '''Return the list of the stripped non blank lines in fname'''
    return [l.strip() for l in
            open(fname, 'r').read().split('\n') if l != '']
