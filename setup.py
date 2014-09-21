#!/usr/bin/env python

from distutils.core import setup
from mgcli import __version__ as VERSION


REQUIRES = [s.strip() for s in open('requirements.txt').readlines()]


setup(name='mgcli',
      version=VERSION,
      description='A Simple CLI and MailGun',
      author='Pili Hu',
      author_email='e@hupili.net',
      url='https://github.com/hupili/mgcli',
      license="MIT",
      scripts=['mgcli.py'],
      requires=REQUIRES
     )
