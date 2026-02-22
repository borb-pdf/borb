#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'SCN' operator: Set the color for stroking operations, supporting additional color spaces.

This operator functions like the 'SC' operator but also supports Pattern, Separation,
DeviceN, and ICCBased color spaces. The number of operands and their interpretation
depend on the current stroking color space.

If the current stroking color space is:

- **Separation**, **DeviceN**, or **ICCBased**: The operands (c1…cn) are numbers, and
  the number of operands varies depending on the color space.
- **Pattern color space**: The operand is the name of an entry in the Pattern subdictionary
  of the current resource dictionary. For an uncolored tiling pattern (PatternType = 1,
  PaintType = 2), the operands (c1…cn) specify a color in the pattern’s underlying color space.
  For other types of patterns, no operands are specified.

The operator sets the color for stroking operations, affecting the current graphics state.

Note:
    The behavior of this operator is influenced by the specifics of the stroking
    color space, which can vary significantly in terms of operands and their meanings.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorSCN(Operator):
    """
    The 'SCN' operator: Set the color for stroking operations, supporting additional color spaces.

    This operator functions like the 'SC' operator but also supports Pattern, Separation,
    DeviceN, and ICCBased color spaces. The number of operands and their interpretation
    depend on the current stroking color space.

    If the current stroking color space is:

    - **Separation**, **DeviceN**, or **ICCBased**: The operands (c1…cn) are numbers, and
      the number of operands varies depending on the color space.
    - **Pattern color space**: The operand is the name of an entry in the Pattern subdictionary
      of the current resource dictionary. For an uncolored tiling pattern (PatternType = 1,
      PaintType = 2), the operands (c1…cn) specify a color in the pattern’s underlying color space.
      For other types of patterns, no operands are specified.

    The operator sets the color for stroking operations, affecting the current graphics state.

    Note:
        The behavior of this operator is influenced by the specifics of the stroking
        color space, which can vary significantly in terms of operands and their meanings.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, source: Source):
        """
        Initialize the 'SCN' operator.

        This operator requires access to the active rendering Source because
        the number and interpretation of operands depend on the currently
        selected stroking color space in the graphics state.

        The Source instance provides access to:
        - The current graphics state
        - The active stroking color space
        - Validation context for operand count and color component semantics

        Since the 'SCN' operator does not explicitly specify a color space
        (it uses the one already set in the graphics state), it must query
        the Source at execution time to determine how many operands are
        expected (e.g., 1 for DeviceGray, 3 for DeviceRGB, 4 for DeviceCMYK,
        or a color-space-defined component count for other spaces).

        :param source: The Source representing the page/content stream
                       currently being rendered. It provides access to
                       the graphics state, including the active
                       stroking color space.
        """
        self.__source = source

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        from borb.pdf.color.grayscale_color import GrayscaleColor
        from borb.pdf.color.rgb_color import RGBColor
        from borb.pdf.color.cmyk_color import CMYKColor

        if self.__source.stroke_color_space == "CalGray":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            self.__source.stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.stroke_color_space == "CalRGB":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            self.__source.stroke_color = RGBColor(
                red=int(operands[0] * 255),
                green=int(operands[1] * 255),
                blue=int(operands[2] * 255),
            )
        if self.__source.stroke_color_space == "DeviceCMYK":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            assert isinstance(operands[3], int) or isinstance(operands[3], float)
            self.__source.stroke_color = CMYKColor(
                cyan=operands[0],
                magenta=operands[1],
                yellow=operands[2],
                key=operands[3],
            )
        if self.__source.stroke_color_space == "DeviceGray":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            self.__source.stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.stroke_color_space == "DeviceRGB":
            assert isinstance(operands[0], int) or isinstance(operands[0], float)
            assert isinstance(operands[1], int) or isinstance(operands[1], float)
            assert isinstance(operands[2], int) or isinstance(operands[2], float)
            self.__source.stroke_color = RGBColor(
                red=int(operands[0] * 255),
                green=int(operands[1] * 255),
                blue=int(operands[2] * 255),
            )
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "SCN"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        if self.__source.stroke_color_space == "CalGray":
            return 1
        if self.__source.stroke_color_space == "CalRGB":
            return 3
        if self.__source.stroke_color_space == "DeviceCMYK":
            return 4
        if self.__source.stroke_color_space == "DeviceGray":
            return 1
        if self.__source.stroke_color_space == "DeviceRGB":
            return 3
        # TODO
        return 0
