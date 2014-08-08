.. netengine documentation master file, created by
   sphinx-quickstart on Fri Aug  8 15:35:40 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to netengine's documentation!
=====================================


**********
Netengine
**********

Netengine is an open source library developed throughout GSOC2014 with Ninux.
It provides a Python abstraction layer to retrieve info from network devices using different back ends and suiting
the mainly used firmwares in nowadays devices (e.g antennas and routers).

=======================
Status of this project
=======================

The project aims to be completed by the end of August 2013 which is the end of GSOC2014 program.
As it is, it is composed by 3 backends:
 * HTTP
 * SSH
 * SNMP



=============
Install
=============
If you want to install Netengine in your system just continue reading, otherwise please go to "Optional step"

Install via pip::

 pip install -e git+git://github.com/ninuxorg/netengine#egg=netengine


==============
Optional step
==============
Sometimes you don't want to install libraries and dependencies in your main Python env, in this case please consider to create a virtualenv.
Virtualenv is an environment completely detached from your main one, where you can add libraries and dependencies by adding anything to your main environment

To create your virtualenv type on a terminal::

 pip install virtualenv

Now you con crete your own virtualenv by typing::

  virtualenv <foo>

Inside this folder you will find two subdirectories:
 * /bin
 * /src

 Before installing anything in you virtualenv named <foo>, please enter in /bin and type::
 source activate

From now on all you are going to install will be visible only inside the scope of virtualev <foo>
Now you can enter the directory /src and type::
 pip install -e git+git://github.com/ninuxorg/netengine#egg=netengine







Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
