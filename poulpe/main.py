# -*- coding: utf-8 -*-
"""Usage:
poulpe init
poulpe viz <graph_file>
"""
from docopt import docopt
import os
import logging
from poulpe import cmd, lines
from tulip import *
from tulipogl import *
from tulipgui import *
from collections import defaultdict
from glob import glob


logging.basicConfig(level=logging.INFO)


def parse_index(index):
    '''Return the index parsed as two dicts.

    The first one maps a git blob to a list of strings of
    the form file:<filename>

    The second one maps an artefact (a string of the form
    <art_type>:<art_value>) to a blob.
    '''
    b2f = defaultdict(list)
    a2b = defaultdict(list)
    for objpath in glob(index + '/objects/*'):
        blob = objpath.split('/')[-1]
        b2f[blob].extend(['file:'+x for x in lines(objpath + '/files')])
        for artpath in [art for art in glob(objpath + '/*')
                        if art[-5:] != 'files']:
            artefact_type = artpath.split('/')[-1]
            for artefact in [a for a in lines(artpath)]:
                a2b[artefact_type + ':' + artefact].append(blob)
    return b2f, a2b


def update_graph_with_index(graph, index):
    '''Return the given tulip graph updated with the given index.

    Modify graph as well, but this may change in the future.'''
    name_prop = graph.getStringProperty('Name')
    view_shape = graph.getIntegerProperty('viewShape')
    view_icon = graph.getStringProperty('viewFontAwesomeIcon')
    view_label = graph.getStringProperty('viewLabel')
    view_texture = graph.getStringProperty('viewTexture')
    blob2fnames, artefact2blobs = parse_index(index)

    known_names = set(name_prop.getNodeValue(n) for n in graph.getNodes())
    all_names = set(sum(blob2fnames.values(), [])) | set(artefact2blobs.keys())
    new_names = all_names - known_names
    for name in new_names:
        node = graph.addNode()
        name_prop.setNodeValue(node, name)
        view_label.setNodeValue(node, ':'.join(name.split(':')[1:]))
        view_shape.setNodeValue(node, tlp.NodeShape.FontAwesomeIcon)
        shape = name.split(':')[0]
        if shape == 'file':
            if name.split(':')[1][:2] == 'PV':
                view_icon.setNodeValue(node, tlp.TulipFontAwesome.Legal)
            else:
                view_icon.setNodeValue(node, tlp.TulipFontAwesome.File)
        elif shape == 'IPv4':
            view_icon.setNodeValue(node, tlp.TulipFontAwesome.Desktop)
        elif shape == 'email':
            view_icon.setNodeValue(node, tlp.TulipFontAwesome.Envelope)
        elif shape == 'domain':
            view_icon.setNodeValue(node, tlp.TulipFontAwesome.MapSigns)
        elif shape == 'BTC':
            view_icon.setNodeValue(node, tlp.TulipFontAwesome.Dollar)
        elif shape == 'onion':
            view_shape.setNodeValue(node, tlp.NodeShape.Billboard)
            view_texture.setNodeValue(node, os.getcwd()+'/.git/icons/onion.png')
        else:
            view_icon.setNodeValue(node, tlp.TulipFontAwesome.Stop)

    known_edges = set(tuple(map(name_prop.getNodeValue, graph.ends(edge)))
                      for edge in graph.getEdges())
    all_edges = set((art, fname) for art in artefact2blobs
                    for blob in artefact2blobs[art]
                    for fname in blob2fnames[blob])
    new_edges = all_edges - known_edges
    for edge in new_edges:
        name2node = lambda name: [n for n in graph.getNodes()
                                  if name_prop.getNodeValue(n) == name][0]
        graph.addEdge(*map(name2node, edge))
    return graph


def viz(graph_file):
    '''Visualize the artefact->file graph'''
    graph = tlp.loadGraph(graph_file) or tlp.newGraph()  # loadGraph() Returns
    # None if error, instead of raising an exception
    graph = update_graph_with_index(graph, os.getcwd()+'/index')
    tlp.saveGraph(graph, graph_file)
    tlpgui.createNodeLinkDiagramView(graph)
    action = input("Tulip visualization launched, press [Enter] to quit,"
                   "type 'discard' and then [Enter] not to save the graph"
                   "on exit.")
    if action != 'discard':
        tlp.saveGraph(graph, graph_file)


def init():
    '''Install the Poulpe's hooks and scripts.'''
    src_dir = os.path.dirname(os.path.realpath(__file__))
    dst_dir = os.getcwd()
    logging.info('Creating a new case')
    cmd('git init')
    cmd('ln -s '+src_dir+'/post-commit ' + dst_dir +
        '/.git/hooks/')
    cmd('mkdir '+dst_dir+'/.git/artefacts')
    cmd('ln -s '+src_dir+'/artefacts/* '+dst_dir+'/.git/artefacts/')
    cmd('mkdir '+dst_dir+'/.git/icons')
    cmd('ln -s '+src_dir+'/img/* '+dst_dir+'/.git/icons/')
    cmd('touch .gitignore')
    cmd('git add .gitignore')
    cmd('git commit -m "Initial commit"')


def main():
    '''Entry point of the command line utility'''
    arguments = docopt(__doc__)
    if arguments['init']:
        init()
    elif arguments['viz']:
        viz(arguments['<graph_file>'])
