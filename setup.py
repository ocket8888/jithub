#!/usr/bin/python

import os
from platform import system
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
	long_description = f.read()

setup(
	name="JitHub",
	version="0.0.1",
	description='Transparently connects GitHub projects to JIRA instances',
	long_description=long_description,
	url='https://github.com/ocket8888/JitHub',
	author='ocket8888',
	author_email='ocket8888@gmail.com',
	classifiers=[
		'Development Status :: 5 - Alpha',
		'Intended Audience :: Telecommunications Industry',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'Topic :: Internet',
		'License :: Other/Proprietary License',
		'Environment :: Console',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7'
	],
	keywords='JIRA GitHub git jira Jira Github',
	packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	install_requires=['setuptools'],
	entry_points={
		'console_scripts': [
			'jithub=jithub.__init__:main',
		],
	},
	python_requires='~=3.5'
)
