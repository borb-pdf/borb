#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `RecursiveReferenceVisitor` class: Resolves references in a PDF document post-construction.

The `RecursiveReferenceVisitor` is a specialized visitor that traverses a built PDF document
to resolve references recursively. This approach addresses the challenge of resolving references
during the document-building phase, which may result in cyclical dependencies or incomplete references.

By deferring the resolution of references to post-construction, this visitor ensures that all
objects in the document are fully initialized and that references can be resolved without causing
infinite loops or errors.

This visitor is typically used to finalize a PDF document, ensuring that all indirect references
are replaced with their corresponding objects for accurate rendering or processing.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class RecursiveReferenceVisitor(ReadVisitor):
    """
    The `RecursiveReferenceVisitor` class: Resolves references in a PDF document post-construction.

    The `RecursiveReferenceVisitor` is a specialized visitor that traverses a built PDF document
    to resolve references recursively. This approach addresses the challenge of resolving references
    during the document-building phase, which may result in cyclical dependencies or incomplete references.

    By deferring the resolution of references to post-construction, this visitor ensures that all
    objects in the document are fully initialized and that references can be resolved without causing
    infinite loops or errors.

    This visitor is typically used to finalize a PDF document, ensuring that all indirect references
    are replaced with their corresponding objects for accurate rendering or processing.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def __lookup(self, doc: Document, ref: reference) -> PDFType:
        # IF the reference has been resolved in the past
        # THEN return that value
        ref_referenced_object: typing.Optional[PDFType] = ref.get_referenced_object()
        if ref_referenced_object is not None:
            return ref_referenced_object
        # IF the document XREF contains the reference
        # THEN return that
        matching_ref: typing.Optional[reference] = next(
            iter(
                [
                    r
                    for r in doc["XRef"]
                    if r.get_object_nr() == ref.get_object_nr()
                    and r.get_generation_nr() == ref.get_generation_nr()
                ]
            ),
            None,
        )

        if matching_ref is not None:
            # fmt: off
            matching_ref_referenced_object: typing.Optional[PDFType] = matching_ref.get_referenced_object()
            if matching_ref_referenced_object is not None:
                return matching_ref_referenced_object
            # fmt: on
        # default
        return ref

    #
    # PUBLIC
    #

    def visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
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
        from borb.pdf.document import Document

        if not isinstance(node, Document):
            return node

        # stack
        stk: typing.List[PDFType] = [node["Trailer"]]
        done_ids: typing.Set[int] = set()
        while len(stk) > 0:

            m: PDFType = stk[0]
            stk.pop(0)

            # avoid circles
            if id(m) in done_ids:
                continue
            done_ids.add(id(m))

            # handle parent link for dictionaries
            if isinstance(m, dict):
                for k, v in m.items():
                    if isinstance(v, reference):
                        m[k] = self.__lookup(doc=node, ref=v)
                    if isinstance(m[k], dict) or isinstance(m[k], list):
                        if id(m[k]) not in done_ids:
                            stk += [m[k]]

            # handle parent link for lists
            if isinstance(m, list):
                for i, v in enumerate(m):
                    if isinstance(v, reference):
                        m[i] = self.__lookup(doc=node, ref=v)
                    if isinstance(m[i], dict) or isinstance(m[i], list):
                        if id(m[i]) not in done_ids:
                            stk += [m[i]]

        # return
        return node
