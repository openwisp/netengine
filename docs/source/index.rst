=========
Netengine
=========

**Netengine** is a python library that aims to provide a single API to extract common
information from network devices with different firwmares (eg: OpenWRT, AirOS) using different protocols
such as the Simple Network Management Protocol (SNMP), and the ability to easily add other backends
like SSH and HTTP (`read more <#status-of-this-project>`_).

You can immagine **Netengine** as a read-only ORM (Object Relational Mapper) equivalent for networks.

===========
Motivations
===========

While dealing with networks in the real world, it's highly probable that you will
deal with a network which is made with very different routers, switches and servers.
Some may support standard SNMP mibs, some may not, some may implement other HTTP APIs,
some may even implement obscure/custom SNMP mibs.

If you need to develop a web application that automates some networking tasks, you
don't want to deal with all those differences in the application code, because it
would become hard to mantain very soon. You also might not want to tie your web
app code to a specific vendor or firmware because that would make your software unflexible.

If we had a single API we could let web developers focus on the task they need to accomplish
rather than dealing with different firmwares, different linux distributions and so on.

The goal of this project is to build that single API.

======================
Status of this project
======================

We are currently in 0.1 alpha version.

The 0.1 final version will be out by August 2021.

.. note::

    The legacy versions of this project had support for SSH and HTTP for extracting information from
    devices. To see how it worked, visit the
    `0.1.0 alpha release <https://github.com/openwisp/netengine/releases/tag/0.1.0a>`_ page on
    github.

=======
Install
=======

Install the development version (tarball)::

    pip install https://github.com/openwisp/netengine/tarball/master

Alternatively, you can install via pip using git::

    pip install -e git+git://github.com/openwisp/netengine#egg=netengine

==========
Contents:
==========

.. toctree::
    :maxdepth: 2

    /topics/usage
    /topics/snmp
    /topics/netengine-utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
