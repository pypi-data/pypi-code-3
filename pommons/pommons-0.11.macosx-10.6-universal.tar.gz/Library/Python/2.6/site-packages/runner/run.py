import subprocess as sp

def run_block(cmd):
    p=sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    return p.communicate()[0]
