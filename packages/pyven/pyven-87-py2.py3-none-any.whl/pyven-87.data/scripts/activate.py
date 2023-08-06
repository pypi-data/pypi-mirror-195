#!python

# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from shlex import quote
from shutil import copyfileobj
from subprocess import check_call
from tempfile import TemporaryDirectory
from urllib.request import urlopen
import os, sys

initbinname = 'initbin.py'

def activate():
    parser = ArgumentParser()
    parser.add_argument('projectdir', type = lambda s: Path(s).resolve())
    projectdir = parser.parse_args().projectdir
    bindir = projectdir / 'bin'
    bindir.mkdir(exist_ok = True)
    venvpoolpath = bindir / 'venvpool.py'
    with urlopen('https://raw.githubusercontent.com/combatopera/pyven/v87/venvpool.py') as f, venvpoolpath.open('wb') as g:
        copyfileobj(f, g)
    with TemporaryDirectory() as bootdir:
        bootdir = Path(bootdir)
        (bootdir / 'requirements.txt').write_text('pyven>=87\n')
        initbinpath = bootdir / initbinname
        initbinpath.write_text(getsource(sys.modules[__name__]))
        venvpoolpathstr = str(venvpoolpath)
        bindirstr = str(bindir)
        check_call([sys.executable, venvpoolpathstr, '--', str(initbinpath), str(projectdir), bindirstr, venvpoolpathstr])
    try:
        dirstrs = os.environ['PATH'].split(os.pathsep)
    except KeyError:
        dirstrs = []
    if bindirstr in dirstrs:
        print('# Already activated.')
    else:
        dirstrs.append(bindirstr)
        print('# Please eval this line in your shell:')
        print('PATH=' + quote(os.pathsep.join(dirstrs)))

def initbin():
    from pyven.initscripts import scan
    parser = ArgumentParser()
    parser.add_argument('projectdir')
    parser.add_argument('bindir')
    parser.add_argument('venvpoolpath')
    args = parser.parse_args()
    scan(args.projectdir, args.bindir, 3, args.venvpoolpath)

if ('__main__' == __name__):
    (initbin if initbinname == Path(sys.argv[0]).name else activate)()
