"""
I provide an interface between the Eye_ reasoning engine and RDFlib_.

.. _Eye: http://eulersharp.sourceforge.net/
.. _RDFlib: http://rdflib.readthedocs.org/
"""
__version__ = "0.0.1"

from contextlib import contextmanager
from subprocess import Popen, PIPE

from rdflib.graph import Graph, QuotedGraph
from rdflib.namespace import Namespace
from rdflib.term import BNode

LOG = Namespace('http://www.w3.org/2000/10/swap/log#')
R = Namespace('http://www.w3.org/2000/10/swap/reason#')

@contextmanager
def add_rule_in(graph):
    """
    Helper function for defining N3 rules in a Graph.

    Usage::

        g = Graph()
        wih add_rule_in(g) as (ifgraph, thengraph):
           ifgraph.add((...))
           thengraph.add((...))
    """
    store = graph.store
    assert store.formula_aware
    ifgraph = QuotedGraph(store, BNode())
    thengraph = QuotedGraph(store, BNode())
    try:
        yield (ifgraph, thengraph)
        graph.add((ifgraph, LOG.implies, thengraph))
    except:
        raise

def eye(graphs, eye_path="eye", include_proof=False):
    """
    Process a set of graphs with EYE, and return the inferred triples.
    """
    pass_opt = '--pass-only-new' if not include_proof else '--pass-all'
    out_parser = 'turtle' if not include_proof else 'n3'

    eyep = Popen([eye_path, '-', pass_opt],
                 stdin=PIPE, stdout=PIPE, stderr=PIPE)

    for graph in graphs:
        graph.serialize(eyep.stdin, format='n3')
    eyep.stdin.close()

    infered = Graph()
    infered.load(eyep.stdout, format=out_parser)
    log = eyep.stderr.read()
    eyep.wait()

    return infered, log
