#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NoOpReferenceVisitor is a specialized visitor that deliberately does not resolve references.

This visitor is used when a reference should be recognized but left unresolved during
a particular pass, for example to prevent infinite recursion or cycles in the object
graph. It acts as a placeholder in multi-pass reference resolution pipelines, allowing
other visitors to safely traverse the PDF document without triggering dereferencing
for certain references.

Typical use cases include:
- Skipping resolution of references inside object streams during the first pass
- Deferring resolution to a later pass such as SecondPassReferenceVisitor
- Acting as a safe “no-op” handler in traversal pipelines where reference resolution
  is conditionally applied

NoOpReferenceVisitor does not modify the document, return resolved objects, or otherwise
perform any action on the references it encounters. Its role is purely structural and
protective within the reference resolution framework.
"""

import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.read.reference_visitor.generic_reference_visitor import (
    GenericReferenceVisitor,
)


class NoOpReferenceVisitor(GenericReferenceVisitor):
    """
    NoOpReferenceVisitor is a specialized visitor that deliberately does not resolve references.

    This visitor is used when a reference should be recognized but left unresolved during
    a particular pass, for example to prevent infinite recursion or cycles in the object
    graph. It acts as a placeholder in multi-pass reference resolution pipelines, allowing
    other visitors to safely traverse the PDF document without triggering dereferencing
    for certain references.

    Typical use cases include:
    - Skipping resolution of references inside object streams during the first pass
    - Deferring resolution to a later pass such as SecondPassReferenceVisitor
    - Acting as a safe “no-op” handler in traversal pipelines where reference resolution
      is conditionally applied

    NoOpReferenceVisitor does not modify the document, return resolved objects, or otherwise
    perform any action on the references it encounters. Its role is purely structural and
    protective within the reference resolution framework.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize a ReadVisitor instance.

        This constructor initializes the `ReadVisitor` class, which is a visitor
        for processing PDF nodes. The visitor may optionally be given a reference
        to a root visitor (`FacadeVisitor`) to delegate the processing of PDF nodes.
        The root visitor serves as the main controller for node traversal, and this
        class allows for interaction with that root instance.

        :param root: An optional reference to the root visitor (`FacadeVisitor`)
                     which will be used to delegate the visiting of PDF nodes.
        """
        super().__init__(root=root)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def visit(
        self, node: typing.Union[int, PDFType]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        if not isinstance(node, int):
            return None
        if self.get_bytes()[node] not in b"0123456789":
            return None

        # read object nr
        i: int = node
        j: int = node
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        object_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read generation number
        i = j
        if self.get_bytes()[i] not in b"0123456789":
            return None
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        generation_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read 'R'
        i = j
        if self.get_bytes()[i : i + 1] != b"R":
            return None
        i += 1

        # ALWAYS swap out the reference for the document bound reference
        ref: typing.Optional[reference] = self._get_document_bound_reference(
            reference(object_nr=object_nr, generation_nr=generation_nr)
        )
        assert (
            ref is not None
        ), f"Unable to retrieve document-bound reference for {object_nr} {generation_nr} R."

        # return
        return ref, i
