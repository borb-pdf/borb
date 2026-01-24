#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `ByteOffsetReferenceVisitor` class resolves indirect PDF references using byte offsets.

This visitor performs a first-pass resolution of indirect object references by locating
objects directly via their byte offsets in the PDF file. It operates on the physical
structure of the document rather than the fully constructed object graph, allowing it
to resolve references deterministically without triggering recursive traversal.

Any references that cannot be resolved safely or completely during this phase are
intentionally left unresolved and deferred to later passes, such as the
`SecondPassReferenceVisitor`, which operates on the fully constructed document graph.

This visitor is a critical component of the multi-pass reference resolution strategy,
ensuring that structurally addressable references are resolved early while maintaining
correctness and avoiding infinite recursion.
"""

import logging
import typing

from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.read.reference_visitor.generic_reference_visitor import (
    GenericReferenceVisitor,
)


class ByteOffsetReferenceVisitor(GenericReferenceVisitor):
    """
    The `ByteOffsetReferenceVisitor` class resolves indirect PDF references using byte offsets.

    This visitor performs a first-pass resolution of indirect object references by locating
    objects directly via their byte offsets in the PDF file. It operates on the physical
    structure of the document rather than the fully constructed object graph, allowing it
    to resolve references deterministically without triggering recursive traversal.

    Any references that cannot be resolved safely or completely during this phase are
    intentionally left unresolved and deferred to later passes, such as the
    `SecondPassReferenceVisitor`, which operates on the fully constructed document graph.

    This visitor is a critical component of the multi-pass reference resolution strategy,
    ensuring that structurally addressable references are resolved early while maintaining
    correctness and avoiding infinite recursion.
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

    def _visit_from_object(
        self, node: reference
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:

        # IF there is no byte offset
        # THEN return
        node_byte_offset: typing.Optional[int] = node.get_byte_offset()
        if node_byte_offset is None:
            return None

        # IF we are already resolving the reference
        # THEN do nothing and return
        if self._is_being_resolved(node):
            return node, -1

        # mark the reference as being resolved
        self._mark_as_being_resolved(node)

        # visit the byte offset
        referenced_object_and_blank = self.root_generic_visit(node_byte_offset)
        if referenced_object_and_blank is None:
            # fmt: off
            logger = logging.getLogger(__name__)
            logger.debug(f"Unable to resolve {node} R (redirects to byte {node.get_byte_offset()}), read returns None")
            return node, -1
            # fmt: on

        # set the referenced_object in the reference
        node._reference__referenced_object = referenced_object_and_blank[0]  # type: ignore[attr-defined]

        # return
        return referenced_object_and_blank[0], -1
