============
Installation
============

On MacOSX and Linux, simply call::

    $ pip install poulpe

One needs to install `Tulip <http://tulip.labri.fr>`_ in order to visualize the graphs made by the Poulpe. On Linux, the automatic installation of tulip's python modules as a dependency of poulpe does not work. Tulip must be installed from source before running the pip install poulpe command.

http://tulip.labri.fr/Documentation/current/tulip-dev/html/installation.html

Tulip will install its content in non stadard places, it may be necessary to play with the environment variables PYTHONPATH and DL_LIBRARY_PATH. When installing from sources, the command that worked for me were ::

  $sudo PYTHONPATH=/usr/local/lib/python/ LD_LIBRARY_PATH=/usr/local/lib/ make install

