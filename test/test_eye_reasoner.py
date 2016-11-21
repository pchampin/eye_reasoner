"""
Unit tests for eye_reasoner.
"""

from rdflib.graph import Graph
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib.term import URIRef, Variable

from eye_reasoner import add_rule_in, eye

def test0():
    """
    Testing this module with a simple example.
    """
    # pylint: disable=invalid-name
    rules = Graph()
    #g.load("eye.n3", format="n3")
    vs = Variable('s')
    vp = Variable('p')
    vo = Variable('o')
    with add_rule_in(rules) as (p, c):
        p.add((vs, vp, vo))
        c.add((vs, RDF.type, RDFS.Resource))
        c.add((vp, RDF.type, RDF.Property))
    with add_rule_in(rules) as (p, c):
        p.add((vs, RDF.type, vo))
        c.add((vo, RDF.type, RDFS.Class))

    pa = URIRef('http://champin.net/#pa')
    data = Graph()
    data.add((pa, RDF.type, FOAF.Person))

    infered, _ = eye([rules, data])

    expected = [
        (pa, RDF.type, RDFS.Resource),
        (RDFS.Resource, RDF.type, RDFS.Class),
        (RDFS.Resource, RDF.type, RDFS.Resource),
        (RDFS.Class, RDF.type, RDFS.Class),
        (RDFS.Class, RDF.type, RDFS.Resource),
        (RDF.Property, RDF.type, RDFS.Class),
        (RDF.Property, RDF.type, RDFS.Resource),
        (FOAF.Person, RDF.type, RDFS.Class),
        (FOAF.Person, RDF.type, RDFS.Resource),
        (RDF.type, RDF.type, RDF.Property),
        (RDF.type, RDF.type, RDFS.Resource),
    ]
    for triple in expected:
        assert triple in infered
    assert len(infered) == len(expected), len(infered)


if __name__ == '__main__':
    test0()
