#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name="django-json-rpc",
  version="1.0",
  description="A simple JSON-RPC implementation for Django",
  author="Andrew Naoum",
  author_email="andrew@naoum.me",
  license="MIT",
  url="http://github.com/anaoum/django-json-rpc",
  download_url="http://github.com/anaoum/django-json-rpc/tree/master",
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'],
  packages=['djangojsonrpc'],
  install_requires=['Django>=1.3'])
