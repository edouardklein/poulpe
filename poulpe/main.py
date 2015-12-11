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


def add_node(graph, name):
    '''Add the specified node to the graph, return the graph

    Modify graph as well, but this may change in the future'''
    name_prop = graph.getStringProperty('Name')
    view_shape = graph.getIntegerProperty('viewShape')
    view_icon = graph.getStringProperty('viewFontAwesomeIcon')
    view_label = graph.getStringProperty('viewLabel')
    view_texture = graph.getStringProperty('viewTexture')

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
    return graph


def add_edge(graph, edge, no_such_node=lambda e: False):
    '''Add the specified edge to the graph, return the graph

    Modify graph as well, but this may change in the future'''
    name_prop = graph.getStringProperty('Name')
    name2node = lambda name: [n for n in graph.getNodes()
                              if name_prop.getNodeValue(n) == name][0]
    try:
        graph.addEdge(*map(name2node, edge))
    except IndexError as e:  # No such node, callback
        if no_such_node(e):
            raise Exception()
    return graph


def update_graph_with_index(all_graph, graph, index):
    '''Return the given tulip graph updated with the given index.

    Modify graph as well, but this may change in the future.'''
    blob2fnames, artefact2blobs = parse_index(index)

    name_prop = all_graph.getStringProperty('Name')

    known_names = set(name_prop.getNodeValue(n) for n in all_graph.getNodes())
    all_names = set(sum(blob2fnames.values(), [])) | set(artefact2blobs.keys())
    new_names = all_names - known_names
    for name in new_names:
        graph = add_node(graph, name)
        all_graph = add_node(all_graph, name)

    known_edges = set(tuple(map(name_prop.getNodeValue, all_graph.ends(edge)))
                      for edge in all_graph.getEdges())
    all_edges = set((art, fname) for art in artefact2blobs
                    for blob in artefact2blobs[art]
                    for fname in blob2fnames[blob])
    new_edges = all_edges - known_edges
    for edge in new_edges:
        graph = add_edge(graph, edge)
        all_graph = add_edge(all_graph, edge, no_such_node=lambda e: True)
    return all_graph, graph


def viz(graph_file):
    '''Visualize the artefact->file graph'''
    all_graph_file = graph_file[:-3]+'all.tlp'
    all_graph = tlp.loadGraph(all_graph_file) or tlp.newGraph()
    graph = tlp.loadGraph(graph_file) or tlp.newGraph()  # loadGraph() Returns
    # None if error, instead of raising an exception
    all_graph, graph = update_graph_with_index(all_graph, graph,
                                               os.getcwd()+'/index')
    tlp.saveGraph(graph, graph_file)
    tlp.saveGraph(all_graph, all_graph_file)
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
    # Linking executable files
    cmd('ln -s '+src_dir+'/post-commit ' + dst_dir +
        '/.git/hooks/')
    cmd('mkdir '+dst_dir+'/.git/artefacts')
    cmd('ln -s '+src_dir+'/artefacts/* '+dst_dir+'/.git/artefacts/')
    # Linking resources
    cmd('mkdir '+dst_dir+'/.git/icons')
    cmd('ln -s '+src_dir+'/img/* '+dst_dir+'/.git/icons/')
    # Creating a dummy first commit because our post-commit script fails
    # when called on the first commit of a repo
    cmd('touch .gitignore')
    cmd('git add .gitignore')
    cmd('git commit -m "Initial commit"')
    # Creating the branch where the index will be stored
    cmd('git branch index')


def main():
    '''Entry point of the command line utility'''
    arguments = docopt(__doc__)
    if arguments['init']:
        init()
    elif arguments['viz']:
        viz(arguments['<graph_file>'])
