watch-fs
========

``watch-fs`` is a command line tool to run commands when files change.

Usage
-----

``watch-fs`` will watch any number of directories and files, and run a command
when any of them are changed. By default, ``watch-fs`` will watch the current
directory.

::

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

I recommend you use `pipsi <https://github.com/mitsuhiko/pipsi>`_ to install ``watch-fs`` as a script::

  pipsi install watch-fs

Alternatively, you can install it as a global python module with::

	pip install watch-fs

Licence
-------

``watch-fs`` is licensed under the MIT Licence.

Author
------

``watch-fs`` was written by `Sam Clements <https://github.com/borntyping>`_.
