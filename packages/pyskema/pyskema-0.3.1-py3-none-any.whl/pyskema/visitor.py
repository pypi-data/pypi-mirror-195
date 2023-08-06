"""Schema base visitor.

:mod:`pyskema` uses the `visitor patter <https://en.wikipedia.org/wiki/Visitor_pattern>`_
to implement various operations on schema.
This module implement the base class that should be extended to implement such operation.
"""
from .schema import Node


class Visitor:
    "The base visitor."

    def visit(self, node: Node, *args, **kwargs):
        "The entry point for all :class:`scheme.Node`."
        return node.structure.accept(self, *args, **kwargs)

    def visit_atom(self, atom, *args, **kwargs):
        "Visit an :class:`pyskema.schema.Atom` instance."
        pass

    def visit_union(self, union, *args, **kwargs):
        "Visit an :class:`pyskema.schema.Union` instance."
        for node in union.options:
            self.visit(node, *args, **kwargs)

    def visit_record(self, rec, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Record` instance."
        for _, node in rec.fields.items():
            self.visit(node, *args, **kwargs)

    def visit_collection(self, collection, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Collection` instance."
        self.visit(collection.element)

    def visit_map(self, map_, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Map` instance."
        self.visit(map_.element)

    def visit_tuple(self, tup, *args, **kwargs):
        "Visit a :class:`pyskema.schema.Tuple` instance."
        for node in tup.fields:
            self.visit(node, *args, **kwargs)
