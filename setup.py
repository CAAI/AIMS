#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='AIMS',
     version="0.1",
     author="Claes Ladefoged",
     author_email="claes.noehr.ladefoged@regionh.dk",
     description="MS lesion segmentation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/CAAI/AIMS",
     scripts=[
             'AIMS/AIMS',
             'AIMS/AIMS_folder',
     ],
     packages=find_packages(include=['AIMS']),
     install_requires=[
         'numpy',
         'nibabel',
         'nnunet>=1.6.6'
     ],
     classifiers=[
         'Programming Language :: Python :: 3.8',
     ],
 )
