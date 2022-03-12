#!/usr/bin/env python3

from distutils.core import setup
import logging
from setuptools.command.develop import develop
from subprocess import check_call
import shlex


class PostDevelopCommand(develop):
    def run(self):
        try:
            check_call(shlex.split('pre-commit clean'))
            check_call(shlex.split('pre-commit install'))
        except BaseException:
            logging.warning('Unable to install the pre-commit tool hooks')


setup(name='GstServerAPI',
      version='0.1.0',
      description='GStreamer server API',
      author='Daniel Chaves',
      author_email='danichg94@gmail',
      packages=['distutils', 'distutils.command'],
      cmdclass={'develop': PostDevelopCommand}
      )
