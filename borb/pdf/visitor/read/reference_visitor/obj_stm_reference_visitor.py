#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ObjStmReferenceVisitor resolves references to objects stored inside PDF object streams.

This visitor performs a first-pass resolution for indirect references that point to
objects embedded within object streams. PDF object streams allow multiple objects
to be compressed together, which means that references to these objects cannot be
resolved simply by byte offset alone.

The responsibilities of ObjStmReferenceVisitor include:
- Locating objects inside object streams based on the object number and generation
  number
- Safely returning references to the actual objects without triggering cycles
- Deferring any recursive resolution of contained references to later passes, such
  as SecondPassReferenceVisitor
- Integrating with the multi-pass reference resolution framework to ensure that
  all object-stream references are correctly mapped before the second pass

By handling object-stream references explicitly, this visitor allows the PDF parsing
pipeline to resolve all objects efficiently while maintaining cycle-safety and
supporting deferred resolution strategies.
"""

import typing

from borb.pdf.primitives import PDFType, reference, stream
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.read.compression.decode_stream import decode_stream
from borb.pdf.visitor.read.read_visitor import ReadVisitor
from borb.pdf.visitor.read.reference_visitor.generic_reference_visitor import (
    GenericReferenceVisitor,
)


class ObjStmReferenceVisitor(GenericReferenceVisitor):
    """
    ObjStmReferenceVisitor resolves references to objects stored inside PDF object streams.

    This visitor performs a first-pass resolution for indirect references that point to
    objects embedded within object streams. PDF object streams allow multiple objects
    to be compressed together, which means that references to these objects cannot be
    resolved simply by byte offset alone.

    The responsibilities of ObjStmReferenceVisitor include:
    - Locating objects inside object streams based on the object number and generation
      number
    - Safely returning references to the actual objects without triggering cycles
    - Deferring any recursive resolution of contained references to later passes, such
      as SecondPassReferenceVisitor
    - Integrating with the multi-pass reference resolution framework to ensure that
      all object-stream references are correctly mapped before the second pass

    By handling object-stream references explicitly, this visitor allows the PDF parsing
    pipeline to resolve all objects efficiently while maintaining cycle-safety and
    supporting deferred resolution strategies.
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

    def __get_references_related_to_parent_object_stream(
        self, object_nr: int
    ) -> typing.List[reference]:
        # go to root visitor
        root_visitor: ReadVisitor = self
        while root_visitor._ReadVisitor__parent is not None:  # type: ignore[attr-defined]
            root_visitor = root_visitor._ReadVisitor__parent  # type: ignore[attr-defined]

        # loop over its xref(s) in reverse order
        refs = []
        for xref_table_entry in root_visitor._RootVisitor__xref[::-1]:  # type: ignore[attr-defined]
            if xref_table_entry.get_parent_stream_object_nr() == object_nr:
                refs += [xref_table_entry]

        # return
        return refs

    def __root_generic_visit_bytes(self, b: bytes) -> typing.Tuple[PDFType, int]:

        # build a copy of the RootVisitor
        from borb.pdf.visitor.read.root_visitor import RootVisitor

        obj_stm_root_visitor: RootVisitor = RootVisitor()

        # remove the ByteOffsetReferenceVisitor
        from borb.pdf.visitor.read.reference_visitor.byte_offset_reference_visitor import (
            ByteOffsetReferenceVisitor,
        )

        obj_stm_root_visitor._RootVisitor__visitors = [  # type: ignore[attr-defined]
            x
            for x in obj_stm_root_visitor._RootVisitor__visitors  # type: ignore[attr-defined]
            if not isinstance(x, ByteOffsetReferenceVisitor)
        ]

        # replace the ObjStmReferenceVisitor
        from borb.pdf.visitor.read.reference_visitor.no_op_reference_visitor import (
            NoOpReferenceVisitor,
        )

        obj_stm_root_visitor._RootVisitor__visitors = [  # type: ignore[attr-defined]
            (
                x
                if not isinstance(x, ObjStmReferenceVisitor)
                else NoOpReferenceVisitor(root=obj_stm_root_visitor)
            )
            for x in obj_stm_root_visitor._RootVisitor__visitors  # type: ignore[attr-defined]
        ]

        # chain it in the hierarchy
        obj_stm_root_visitor._ReadVisitor__parent = self._ReadVisitor__parent  # type: ignore[attr-defined]

        # call visit
        retval_and_blank = obj_stm_root_visitor.visit(b)
        assert (
            retval_and_blank is not None
        ), f"Unable to process (parent) object stream '{b[0:32].decode()} ... {b[-32:].decode()}'"

        # find all references mentioned in the object
        objs_to_scan: typing.List[PDFType] = [retval_and_blank[0]]
        objs_scanned: typing.List[PDFType] = []
        refs_to_process: typing.List[reference] = []
        while len(objs_to_scan) > 0:
            obj_to_scan = objs_to_scan[0]
            objs_to_scan.pop(0)
            if obj_to_scan in objs_scanned:
                continue
            objs_scanned += [obj_to_scan]
            if isinstance(obj_to_scan, dict):
                for _, v in obj_to_scan.items():
                    objs_to_scan += [v]
            if isinstance(obj_to_scan, list):
                objs_to_scan += obj_to_scan
            if isinstance(obj_to_scan, reference):
                refs_to_process += [obj_to_scan]

        # filter out duplicates
        refs_to_process = list(set(refs_to_process))

        # filter out everything already being resolved
        refs_to_process = [x for x in refs_to_process if not self._is_being_resolved(x)]

        # lookup these references
        for ref in refs_to_process:
            self.root_generic_visit(node=ref)  # type: ignore[arg-type]

        # return
        return retval_and_blank

    def _visit_from_object(
        self, node: reference
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:

        # look up (parent) stream object
        parent_stream_object_nr: typing.Optional[int] = (
            node.get_parent_stream_object_nr()
        )
        index_in_parent_stream: typing.Optional[int] = node.get_index_in_parent_stream()
        if parent_stream_object_nr is None:
            return None
        if index_in_parent_stream is None:
            return None

        # IF we are already resolving the reference
        # THEN do nothing and return
        if self._is_being_resolved(node):
            return node, -1

        # mark the reference as being resolved
        self._mark_as_being_resolved(node)

        # mark every reference derived from the same parent as being resolved
        for derived_ref in self.__get_references_related_to_parent_object_stream(
            object_nr=parent_stream_object_nr
        ):
            self._mark_as_being_resolved(derived_ref)

        # look up (parent) reference
        parent_ref: typing.Optional[reference] = self._get_document_bound_reference(
            reference(object_nr=parent_stream_object_nr, generation_nr=0)
        )

        # ensure the parent reference exists
        # fmt: off
        assert parent_ref is not None, f"Reference {node} points to a (parent) stream object reference {parent_stream_object_nr} 0 R that does not exist."
        # fmt: on

        # ensure the parent reference is a byte offset reference
        # fmt: off
        assert parent_ref.get_byte_offset() is not None, f"Reference {node} points to a (parent) stream object reference that is not a byte-offset type reference."
        # fmt: on

        # fetch the underlying stream
        # fmt: off
        parent_ref_byte_offset: typing.Optional[int] = parent_ref.get_byte_offset()
        assert parent_ref_byte_offset is not None, f"Reference {node} does not point to a byte-offset."
        parent_stream_obj_and_blank = self.root_generic_visit(parent_ref_byte_offset)
        assert parent_stream_obj_and_blank is not None, f"Reference {node} points to a (parent) stream object reference, which did not resolve to an object."
        parent_stream_obj, _ = parent_stream_obj_and_blank
        assert isinstance(parent_stream_obj, stream), f"Reference {node} points to a (parent) stream object reference, which did not resolve to a stream object."
        # fmt: on

        # decode the stream object
        decode_stream(parent_stream_obj)

        # read the header
        # fmt: off
        header_offset: int = parent_stream_obj.get("First", 0)
        object_stm_header: bytes = parent_stream_obj["DecodedBytes"][:header_offset]
        object_stm_bytes_without_header: bytes = parent_stream_obj["DecodedBytes"][header_offset:]
        # fmt: on

        # read the objects in the stream
        objs: typing.List[PDFType] = []
        while len(object_stm_bytes_without_header) > 0:

            # IF we see a space
            # THEN skip
            if object_stm_bytes_without_header[0:1] == b" ":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue

            # IF we see a newline (\n\r)
            # THEN skip
            if object_stm_bytes_without_header[0:2] == b"\n\r":
                object_stm_bytes_without_header = object_stm_bytes_without_header[2:]
                continue
            if object_stm_bytes_without_header[0:2] == b"\r\n":
                object_stm_bytes_without_header = object_stm_bytes_without_header[2:]
                continue
            if object_stm_bytes_without_header[0:1] == b"\n":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue
            if object_stm_bytes_without_header[0:1] == b"\r":
                object_stm_bytes_without_header = object_stm_bytes_without_header[1:]
                continue

            referenced_object_and_i = self.__root_generic_visit_bytes(
                object_stm_bytes_without_header
            )
            if referenced_object_and_i is None:
                break
            objs += [referenced_object_and_i[0]]
            object_stm_bytes_without_header = object_stm_bytes_without_header[
                referenced_object_and_i[1] :
            ]

        # set objects in xref
        for ref_to_update in self.__get_references_related_to_parent_object_stream(
            object_nr=parent_stream_object_nr
        ):
            try:
                ref_to_update._reference__referenced_object = objs[  # type: ignore[attr-defined]
                    ref_to_update.get_index_in_parent_stream()  # type: ignore[index]
                ]
            except:
                pass

        # return
        return node.get_referenced_object() or node, -1

    #
    # PUBLIC
    #
