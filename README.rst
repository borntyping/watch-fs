watch-fs
========

.. image:: https://img.shields.io/pypi/v/watch-fs.svg?style=flat-square
    :target: https://warehouse.python.org/project/watch-fs/
    :alt: watch-fs on PyPI

.. image:: https://img.shields.io/pypi/l/watch-fs.svg?style=flat-square
    :target: https://warehouse.python.org/project/watch-fs/
    :alt: watch-fs on PyPI

.. image:: https://img.shields.io/travis/borntyping/watch-fs/master.svg?style=flat-square
    :target: https://travis-ci.org/borntyping/watch-fs
    :alt: Travis-CI build status for watch-fs

.. image:: https://img.shields.io/github/issues/borntyping/watch-fs.svg?style=flat-square
    :target: https://github.com/borntyping/watch-fs/issues
    :alt: GitHub issues for watch-fs

|

``watch-fs`` is a command line tool to run commands when files change.

* `Source on GitHub <https://github.com/borntyping/watch-fs>`_
* `Packages on PyPI <https://warehouse.python.org/project/watch-fs/>`_
* `Builds on Travis CI <https://travis-ci.org/borntyping/watch-fs>`_

Usage
-----

``watch-fs`` will watch any number of directories and files, and run a command
when any of them are changed. By default, ``watch-fs`` will watch the current
directory.

.. code::

    Usage: watch-fs [OPTIONS] COMMAND

    Options:
      -d, --directory DIRECTORY  A directory to watch for file changes - can be
                                 used multiple times, and defaults to the current
                                 directory.
      -c, --clear                Clear the terminal before running the command
      -w, --wait FLOAT           A minium wait before running the command again,
                                 in seconds
      -v, --verbose              -v prints commands before running, and -vv shows
                                 debug information

Installation
------------

I recommend you use pipsi_ to install ``watch-fs`` in it's own virtualenv and link it from ``~/.local/bin``:

.. code-block:: bash

    pipsi install watch-fs

Alternatively, you can install system-wide using pip_:

.. code-block:: bash

    pip install watch-fs

Licence
-------

``watch-fs`` is licensed under the MIT Licence.

Author
------

``watch-fs`` was written by `Sam Clements <https://github.com/borntyping>`_.

.. _pipsi: https://github.com/mitsuhiko/pipsi
.. _pip: https://pip.readthedocs.org/
