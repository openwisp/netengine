from setuptools import setup, find_packages

from netengine import get_version


setup(
    name='netengine',
    version=get_version(),
    description="Abstraction layer for extracting information from network devices.",
    long_description=open('README.rst').read(),
    author='Federico Capoano (nemesisdesign)',
    author_email='ninux-dev@ml.ninux.org',
    license='MIT',
    url='https://github.com/ninuxorg/netengine',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    install_requires=[
        'paramiko',
        'pysnmp'
    ],
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
