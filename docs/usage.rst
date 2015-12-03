========
Usage
========

To use Poulpe, you need to version control your directory and install the appropriate hooks and scripts. To do this, simply call::

    $ poulpe init

You can then use git to stage your files, and when you commit, the index will automatically get updated::

    $ git add somefile.txt
    $ git commit -m "Some file"

It is then possible to visualize the corresponding graph by calling::

    $ pouple viz example.tlp

The .tlp file you specify on the command line will be created if it does not exist, and updated if it exists.
