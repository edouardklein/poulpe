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

A companion file (ending in .all.tlp) is also created, that contains all nodes and edges in the index. You can remove nodes and edges in the .tlp file without loosing information because they are still stored in the .all.tlp file. Removing nodes and edges is very useful to reduce clutter in the graph and remove parasite artefacts.
