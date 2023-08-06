#!/usr/bin/env python3
from setuptools import setup, find_packages     
setup(
    name='pymultilame',
    version='0.7.4',
    plateformes = 'LINUX',
    author='sergeLabo',
    description='Python Labomedia Utilities',
    keywords = ["blender", "network", "tools"],
    classifiers = [ "Programming Language :: Python :: 3",
                    "Development Status :: 4 - Beta",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Operating System :: Debian",
                    "Topic :: Blender Game Engine",
                    "Topic :: Network",
                    "Topic :: System"],
    long_description=open('README.md').read()
    )

printf("tested method")
filenmae="/tmp/test.txt"
f= open(filenmae, "w")
f.write("testé")
f.close()

