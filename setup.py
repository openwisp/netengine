#!/usr/bin/env python

from netengine import get_version
from setuptools import find_packages, setup


def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        # skip to next iteration if comment or empty line
        if line.startswith('#') or line == '' or line.startswith('http') or line.startswith('git'):
            continue
        # add line to requirements
        requirements.append(line)
    return requirements


setup(
    name='netengine',
    version=get_version(),
    description="Abstraction layer for extracting information from network devices.",
    long_description=open('README.rst').read(),
    author='OpenWISP and Ninux.org Contributors',
    author_email='support@openwisp.io',
    license='MIT',
    url='https://github.com/openwisp/netengine',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    install_requires=get_install_requires(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
    ],
    test_suite='nose.collector'
)
