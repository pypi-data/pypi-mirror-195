#
# Filename: setup.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 05.03.2023
# Last Modified: Sun 05 Mar 2023 10:50:14 PM EST
# Description: 
#
#

from setuptools import setup, find_packages

setup(
    name='suta_bed',
    version='0.1.1',
    license='MIT',
    author="Simon Redman",
    author_email='simon@ergotech.com',
    packages=find_packages('suta_bed'),
    package_dir={'': 'suta_bed'},
    url='https://github.com/sredman/suta-ble-bed',
    keywords=['SUTA','sleepmotion','i500','i900','i200'],
)
