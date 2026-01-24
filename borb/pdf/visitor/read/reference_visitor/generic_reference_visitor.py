#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GenericReferenceVisitor provides the base infrastructure for resolving PDF indirect references.

This class provides shared logic for visitors that resolve indirect PDF references,
either from their textual representation in the byte stream (e.g. "12 0 R") or from
already-parsed `reference` objects. It does not perform resolution itself, but instead
defines the common mechanics required by specialized reference visitors.

Responsibilities of this class include:
- Parsing indirect reference syntax directly from the PDF byte stream
- Mapping parsed references to document-bound references using the cross-reference table
- Tracking references currently being resolved to prevent infinite recursion
- Providing hook methods (`_visit_from_bytes` and `_visit_from_object`) for subclasses
  to implement concrete resolution strategies

GenericReferenceVisitor serves as the foundation for multiple reference-resolution
passes, such as byte-offset-based resolution, object-stream resolution, and deferred
recursive resolution. Subclasses determine *when* and *how* a reference is resolved,
while this class ensures consistent parsing, bookkeeping, and cycle-safety.

This design enables a multi-pass reference resolution pipeline in which different
visitors cooperate to resolve references safely, deterministically, and without
introducing cyclic dependencies.
"""

import typing

from borb.pdf.primitives import reference, PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class GenericReferenceVisitor(ReadVisitor):
    """
    GenericReferenceVisitor provides the base infrastructure for resolving PDF indirect references.

    This class provides shared logic for visitors that resolve indirect PDF references,
    either from their textual representation in the byte stream (e.g. "12 0 R") or from
    already-parsed `reference` objects. It does not perform resolution itself, but instead
    defines the common mechanics required by specialized reference visitors.

    Responsibilities of this class include:
    - Parsing indirect reference syntax directly from the PDF byte stream
    - Mapping parsed references to document-bound references using the cross-reference table
    - Tracking references currently being resolved to prevent infinite recursion
    - Providing hook methods (`_visit_from_bytes` and `_visit_from_object`) for subclasses
      to implement concrete resolution strategies

    GenericReferenceVisitor serves as the foundation for multiple reference-resolution
    passes, such as byte-offset-based resolution, object-stream resolution, and deferred
    recursive resolution. Subclasses determine *when* and *how* a reference is resolved,
    while this class ensures consistent parsing, bookkeeping, and cycle-safety.

    This design enables a multi-pass reference resolution pipeline in which different
    visitors cooperate to resolve references safely, deterministically, and without
    introducing cyclic dependencies.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _get_document_bound_reference(self, r: reference) -> typing.Optional[reference]:
        # go to root visitor
        root_visitor: ReadVisitor = self
        while root_visitor._ReadVisitor__parent is not None:  # type: ignore[attr-defined]
            root_visitor = root_visitor._ReadVisitor__parent  # type: ignore[attr-defined]

        # loop over its xref(s) in reverse order
        for xref_table_entry in root_visitor._RootVisitor__xref[::-1]:  # type: ignore[attr-defined]
            if (
                xref_table_entry.get_object_nr() == r.get_object_nr()
                and xref_table_entry.get_generation_nr() == r.get_generation_nr()
            ):
                return xref_table_entry

        # default
        return None

    def _is_being_resolved(self, r: reference) -> bool:
        # go to root visitor
        root_visitor: ReadVisitor = self
        while root_visitor._ReadVisitor__parent is not None:  # type: ignore[attr-defined]
            root_visitor = root_visitor._ReadVisitor__parent  # type: ignore[attr-defined]

        # lookup
        return id(r) in root_visitor._RootVisitor__references_being_resolved  # type: ignore[attr-defined]

    def _mark_as_being_resolved(self, r: reference) -> None:
        # go to root visitor
        root_visitor: ReadVisitor = self
        while root_visitor._ReadVisitor__parent is not None:  # type: ignore[attr-defined]
            root_visitor = root_visitor._ReadVisitor__parent  # type: ignore[attr-defined]

        # add
        root_visitor._RootVisitor__references_being_resolved.add(id(r))  # type: ignore[attr-defined]

    def _visit_from_bytes(
        self, node: typing.Union[int, PDFType]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:

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

        # IF the reference is not in use
        # THEN return None
        if ref is None:
            return (
                reference(
                    object_nr=object_nr, generation_nr=generation_nr, is_in_use=False
                ),
                i,
            )

        # delegate
        referenced_object_and_blank = self._visit_from_object(node=ref)
        if referenced_object_and_blank is None:
            return None

        # return
        return referenced_object_and_blank[0], i

    def _visit_from_object(
        self, node: reference
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        return None

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
        if isinstance(node, int):
            return self._visit_from_bytes(node=node)
        if isinstance(node, reference):
            return self._visit_from_object(node=node)
        return None
