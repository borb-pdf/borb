#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing string objects in a PDF byte stream.

`StrVisitor` extends `ReadVisitor` to identify and process string objects
within a PDF, converting them into Python strings. Using the visitor pattern,
`StrVisitor` traverses PDF nodes, extracting and decoding string values
according to the PDF specification, allowing for structured handling of
text content in the document.
"""

import typing

from borb.pdf.primitives import PDFType
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class StrVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing string objects in a PDF byte stream.

    `StrVisitor` extends `ReadVisitor` to identify and process string objects
    within a PDF, converting them into Python strings. Using the visitor pattern,
    `StrVisitor` traverses PDF nodes, extracting and decoding string values
    according to the PDF specification, allowing for structured handling of
    text content in the document.
    """

    __STR_CLOSE_BRACKET = b")"
    __STR_OPEN_BRACKET = b"("

    #
    # CONSTRUCTOR
    #

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
        if self.get_bytes()[node : node + 1] != StrVisitor.__STR_OPEN_BRACKET:
            return None

        # 7.3.4.2 Literal Strings
        retval: bytes = b""
        i: int = node
        j: int = node + 1
        nested_bracket_depth: int = 1
        while nested_bracket_depth > 0:

            # Within a literal string, the REVERSE SOLIDUS is used as an escape character. The character immediately
            # following the REVERSE SOLIDUS determines its precise interpretation as shown in Table 3. If the character
            # following the REVERSE SOLIDUS is not one of those shown in Table 3, the REVERSE SOLIDUS shall be
            # ignored.
            ch = self.get_bytes()[j : j + 1]
            if ch == b"\\":

                # Sequence              Meaning
                # \nLINE FEED           (0Ah) (LF)
                # \rCARRIAGE RETURN     (0Dh) (CR)
                # \tHORIZONTAL TAB      (09h) (HT)
                # \bBACKSPACE           (08h) (BS)
                # \fFORM FEED           (FF)
                # \(LEFT PARENTHESIS    (28h)
                # \)RIGHT PARENTHESIS   (29h)
                # \\REVERSE SOLIDUS     (5Ch) (Backslash)
                nxt_ch = self.get_bytes()[j + 1 : j + 2]
                if nxt_ch in b"nrtbf":
                    retval += {
                        b"n": b"\n",
                        b"r": b"\r",
                        b"t": b"\t",
                        b"b": b"\b",
                        b"f": b"\f",
                    }[nxt_ch]
                    j += 2
                    continue
                if nxt_ch in b"()\\":
                    retval += nxt_ch
                    j += 2
                    continue

                # \ddd                  Character code ddd (octal)
                try:
                    tmp: bytes = self.get_bytes()[j : j + 3]
                except:
                    pass

            # update nesting depth
            if ch == b"(":
                nested_bracket_depth += 1
            elif ch == b")":
                nested_bracket_depth -= 1

            # IF we hit the final bracket (depth == 0)
            # THEN break
            if nested_bracket_depth == 0:
                break

            # default
            retval += ch
            j += 1

        # return
        return retval.decode(encoding="latin-1"), j + 1
