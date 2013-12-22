from setuptools import setup, find_packages
from setuptools.command.test import test

from netengine import get_version


#class TestCommand(test):
#    def run(self):
#        from tests.runtests import runtests
#        runtests()


setup(
    name='netengine',
    version=get_version(),
    description="Abstraction layer for extracting information from network devices.",
    long_description=open('README.rst').read(),
    author='Federico Capoano (nemesisdesign)',
    license='MIT',
    url='https://github.com/nemesisdesign/netengine',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
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
    #cmdclass={"test": TestCommand},
)
