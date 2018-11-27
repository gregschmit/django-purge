import os
from subprocess import Popen, PIPE, STDOUT


def cmd_out(cmd):
    wd = os.path.dirname(os.path.realpath(__file__))
    p = Popen(cmd, shell=True, cwd=wd, stdout=PIPE, stderr=STDOUT)
    r, e = p.communicate()
    res = r.strip().decode()
    return res, p.returncode


def get_version():
    d = os.path.dirname(os.path.realpath(__file__))
    try:
        x = open(os.path.join(d, 'VERSION_STAMP'), 'rb').read().strip().decode()
        if x: return x
    except FileNotFoundError:
        pass
    gitver, code = cmd_out('git describe --tags --always')
    gitver = gitver.replace('v', '').split('-g')[0].replace('-', '.dev')
    if not gitver or 'fatal' in gitver or '\n' in gitver:
        return '0'
    gitchanged, code = cmd_out('git diff-index --quiet HEAD --')
    if code:
        gitver += '+changed'
    return gitver


def stamp_directory(d):
    v = get_version()
    with open(os.path.join(d, 'VERSION_STAMP'), 'wb') as f:
        f.write(v.encode() + b'\n')


def unstamp_directory(d):
    os.remove(os.path.join(d, 'VERSION_STAMP'))


if __name__ == '__main__':
    print(get_version())
