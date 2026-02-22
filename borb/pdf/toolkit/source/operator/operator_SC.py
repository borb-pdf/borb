#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'SC' operator: Set the color for stroking operations in a device, CIE-based, or Indexed color space.

This operator sets the color to use for stroking paths, depending on the current
stroking color space. The number of operands required and their interpretation
varies based on the specific color space in use:

- For DeviceGray, CalGray, and Indexed color spaces, one operand is required.
- For DeviceRGB, CalRGB, and Lab color spaces, three operands are required.
- For DeviceCMYK color space, four operands are required.

The operands represent the components of the color in the corresponding color space.
For example, in DeviceRGB, the three operands represent the red, green, and blue components.

Note:
    This operator applies only to stroking operations and will not affect non-stroking
    color or other graphics state parameters.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorSC(Operator):
    """
    The 'SC' operator: Set the color for stroking operations in a device, CIE-based, or Indexed color space.

    This operator sets the color to use for stroking paths, depending on the current
    stroking color space. The number of operands required and their interpretation
    varies based on the specific color space in use:

    - For DeviceGray, CalGray, and Indexed color spaces, one operand is required.
    - For DeviceRGB, CalRGB, and Lab color spaces, three operands are required.
    - For DeviceCMYK color space, four operands are required.

    The operands represent the components of the color in the corresponding color space.
    For example, in DeviceRGB, the three operands represent the red, green, and blue components.

    Note:
        This operator applies only to stroking operations and will not affect non-stroking
        color or other graphics state parameters.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, source: Source):
        """
        Initialize the 'SC' operator.

        This operator requires access to the active rendering Source because
        the number and interpretation of operands depend on the currently
        selected stroking color space in the graphics state.

        The Source instance provides access to:
        - The current graphics state
        - The active stroking color space
        - Validation context for operand count and color component semantics

        Since the 'SC' operator does not explicitly specify a color space
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
            self.__source.stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.stroke_color_space == "CalRGB":
            self.__source.stroke_color = RGBColor(
                red=operands[0], green=operands[1], blue=operands[2]
            )
        if self.__source.stroke_color_space == "DeviceCMYK":
            self.__source.stroke_color = CMYKColor(
                cyan=operands[0],
                magenta=operands[1],
                yellow=operands[2],
                key=operands[3],
            )
        if self.__source.stroke_color_space == "DeviceGray":
            self.__source.stroke_color = GrayscaleColor(level=operands[0])
        if self.__source.stroke_color_space == "DeviceRGB":
            self.__source.stroke_color = RGBColor(
                red=operands[0], green=operands[1], blue=operands[2]
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
        return "SC"

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
