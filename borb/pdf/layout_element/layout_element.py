#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for various types of layout elements.

This class serves as a foundation for layout elements such as text, images, tables, and lists.
A layout element can calculate its size based on available space and render itself on a page.
"""

import enum
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.conformance import Conformance
from borb.pdf.document import Document
from borb.pdf.page import Page


class LayoutElement:
    """
    Base class for various types of layout elements.

    This class serves as a foundation for layout elements such as text, images, tables, and lists.
    A layout element can calculate its size based on available space and render itself on a page.
    """

    class HorizontalAlignment(enum.Enum):
        """Enum for specifying horizontal alignment options."""

        LEFT = 1
        MIDDLE = 2
        RIGHT = 3

    class TextAlignment(enum.Enum):
        """Enum for specifying text alignment options."""

        CENTERED = 1
        JUSTIFIED = 2
        LEFT = 3
        RIGHT = 4

    class VerticalAlignment(enum.Enum):
        """Enum for specifying vertical alignment options."""

        BOTTOM = 1
        MIDDLE = 2
        TOP = 3

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.Optional[typing.List[int]] = None,
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        horizontal_alignment: HorizontalAlignment = HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: VerticalAlignment = VerticalAlignment.TOP,
    ):
        """
        Initialize a new `LayoutElement` object that serves as a base class for all layout elements in a PDF.

        This constructor provides fundamental layout properties that can be customized for all
        derived elements, such as background color, border styles, margins, and padding.
        These properties dictate the visual appearance and positioning of layout elements within
        the PDF, allowing for a flexible and structured layout.

        :param background_color:        Optional background color for the layout element.
        :param border_color:            Optional border color for the layout element.
        :param border_dash_pattern:     Dash pattern used for the border lines of the element.
        :param border_dash_phase:       Phase offset for the dash pattern in the borders.
        :param border_width_bottom:     Width of the bottom border of the element.
        :param border_width_left:       Width of the left border of the element.
        :param border_width_right:      Width of the right border of the element.
        :param border_width_top:        Width of the top border of the element.
        :param horizontal_alignment:     Horizontal alignment of the element (default is LEFT).
        :param margin_bottom:           Space between the element and the element below it.
        :param margin_left:             Space between the element and the left page margin.
        :param margin_right:            Space between the element and the right page margin.
        :param margin_top:              Space between the element and the element above it.
        :param padding_bottom:          Padding inside the element at the bottom.
        :param padding_left:            Padding inside the element on the left side.
        :param padding_right:           Padding inside the element on the right side.
        :param padding_top:             Padding inside the element at the top.
        :param vertical_alignment:       Vertical alignment of the element (default is TOP).
        """
        # fmt: off
        assert margin_bottom >= 0, "Margin bottom must be non-negative"
        assert margin_left >= 0, "Margin left must be non-negative"
        assert margin_right >= 0, "Margin right must be non-negative"
        assert margin_top >= 0, "Margin top must be non-negative"
        assert padding_bottom >= 0, "Padding bottom must be non-negative"
        assert padding_left >= 0, "Padding left must be non-negative"
        assert padding_right >= 0, "Padding right must be non-negative"
        assert padding_top >= 0, "Padding top must be non-negative"
        assert border_width_bottom >= 0, "Border width bottom must be non-negative"
        assert border_width_left >= 0, "Border width left must be non-negative"
        assert border_width_right >= 0, "Border width right must be non-negative"
        assert border_width_top >= 0, "Border width top must be non-negative"
        # fmt: on
        self.__background_color: typing.Optional[Color] = background_color
        self.__border_color: typing.Optional[Color] = border_color
        self.__border_dash_pattern: typing.List[int] = border_dash_pattern or []
        self.__border_dash_phase: int = border_dash_phase
        self.__border_width_bottom: int = border_width_bottom
        self.__border_width_left: int = border_width_left
        self.__border_width_right: int = border_width_right
        self.__border_width_top: int = border_width_top
        self.__horizontal_alignment: LayoutElement.HorizontalAlignment = (
            horizontal_alignment
        )
        self.__margin_bottom: int = margin_bottom
        self.__margin_left: int = margin_left
        self.__margin_right: int = margin_right
        self.__margin_top: int = margin_top
        self.__padding_bottom: int = padding_bottom
        self.__padding_left: int = padding_left
        self.__padding_right: int = padding_right
        self.__padding_top: int = padding_top
        self.__previous_paint_box: typing.Optional[typing.Tuple[int, int, int, int]] = (
            None
        )
        self.__vertical_alignment: LayoutElement.VerticalAlignment = vertical_alignment

    #
    # PRIVATE
    #

    @staticmethod
    def _append_newline_to_content_stream(page: Page) -> None:
        if "Contents" not in page:
            return
        from borb.pdf.primitives import stream

        last_stream: typing.Optional[stream] = None
        if isinstance(page["Contents"], stream):
            last_stream = page["Contents"]
        if isinstance(page["Contents"], list):
            last_stream = page["Contents"][-1]
        if last_stream is None:
            return
        if not isinstance(last_stream, stream):
            return
        if (
            len(last_stream["DecodedBytes"]) > 0
            and last_stream["DecodedBytes"][-1] != b"\n"[0]
        ):
            last_stream["DecodedBytes"] += b"\n"

    @staticmethod
    def _append_space_to_content_stream(page: Page) -> None:
        if "Contents" not in page:
            return
        from borb.pdf.primitives import stream

        last_stream: typing.Optional[stream] = None
        if isinstance(page["Contents"], stream):
            last_stream = page["Contents"]
        if isinstance(page["Contents"], list):
            last_stream = page["Contents"][-1]
        if last_stream is None:
            return
        if not isinstance(last_stream, stream):
            return
        if (
            len(last_stream["DecodedBytes"]) > 0
            and last_stream["DecodedBytes"][-1] != b" "[0]
        ):
            last_stream["DecodedBytes"] += b" "

    @staticmethod
    def _append_to_content_stream(
        page: Page, bytes_or_string: typing.Union[bytes, str]
    ) -> None:
        if "Contents" not in page:
            return

        # IF the input argument is a string
        # THEN convert it to bytes
        bytes_to_append = (
            bytes_or_string
            if isinstance(bytes_or_string, bytes)
            else bytes_or_string.encode("latin1")
        )

        # IF page / Contents is a stream
        # THEN append to the stream
        from borb.pdf.primitives import stream

        if isinstance(page["Contents"], stream):
            page["Contents"]["DecodedBytes"] += bytes_to_append
            return

        # IF page / Contents is an array
        # THEN append to the last stream of the array
        if isinstance(page["Contents"], list):
            last_stream: stream = page["Contents"][-1]
            if not isinstance(last_stream, stream):
                return
            last_stream["DecodedBytes"] += bytes_to_append
            return

    @staticmethod
    def _begin_marked_content_with_dictionary(
        page: Page,
        structure_element_type: str,
        alt: typing.Optional[str] = None,
    ) -> None:
        # check whether the conformance level requires us to do this
        document: typing.Optional[Document] = page.get_document()
        if document is None:
            return
        conformance: typing.Optional[Conformance] = document.get_conformance_at_create()
        if conformance is None:
            return
        if not conformance.requires_tagged_pdf():
            return

        # leading newline (if needed)
        LayoutElement._append_newline_to_content_stream(page=page)

        # find existing BDC declarations
        # TODO: handle Page / Contents / <list>
        import re

        mcids: typing.Set[int] = set()
        for m in re.finditer(
            r"/([A-Za-z0-9]+)\s*<<[^>]*?/MCID\s+(\d+)[^>]*?>>\s*BDC",
            page["Contents"]["DecodedBytes"].decode("latin1"),
        ):
            try:
                mcids.add(int(m[2]))
            except:
                pass

        # determine next MCID
        next_mcid: int = max([x for x in mcids] + [0]) + 1

        # inject "/P << /MCID 0 >> BDC"
        # fmt: off
        if alt is None:
            LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"/{structure_element_type} << /MCID {next_mcid} >> BDC\n")
        else:
            LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"/{structure_element_type} << /MCID {next_mcid} /Alt {alt} >> BDC\n")
        # fmt: on

    @staticmethod
    def _end_marked_content(page: Page) -> None:
        # check whether the conformance level requires us to do this
        document: typing.Optional[Document] = page.get_document()
        if document is None:
            return
        conformance: typing.Optional[Conformance] = document.get_conformance_at_create()
        if conformance is None:
            return
        if not conformance.requires_tagged_pdf():
            return

        # leading newline (if needed)
        LayoutElement._append_newline_to_content_stream(page=page)

        # inject "EMC"
        LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"EMC\n")

    def _paint_background_and_borders(
        self, page: "Page", rectangle: typing.Tuple[int, int, int, int]
    ) -> None:
        x: int = rectangle[0]
        y: int = rectangle[1]
        w: int = rectangle[2]
        h: int = rectangle[3]

        # IF there are no borders AND no background
        # THEN do nothing
        if (
            self.__border_width_bottom
            == self.__border_width_left
            == self.__border_width_right
            == self.__border_width_top
            == 0
            and self.__background_color is None
        ):
            return

        # leading newline (if needed)
        LayoutElement._append_newline_to_content_stream(page)

        # store the graphics state
        LayoutElement._append_to_content_stream(page=page, bytes_or_string="q\n")

        # IF the background color is specified
        # THEN write the operator to set the background color
        if self.__background_color is not None:
            rgb_background_color: RGBColor = self.__background_color.to_rgb_color()
            LayoutElement._append_to_content_stream(
                page=page,
                bytes_or_string=f"{round(rgb_background_color.get_red() / 255, 7)} "
                f"{round(rgb_background_color.get_green() / 255, 7)} "
                f"{round(rgb_background_color.get_blue() / 255, 7)} rg\n",
            )

        # IF the border color is specified
        # THEN write the operator to set the border color
        if self.__border_color is not None:
            rgb_border_color: RGBColor = self.__border_color.to_rgb_color()
            LayoutElement._append_to_content_stream(
                page=page,
                bytes_or_string=f"{round(rgb_border_color.get_red() / 255, 7)} "
                f"{round(rgb_border_color.get_green() / 255, 7)} "
                f"{round(rgb_border_color.get_blue() / 255, 7)} RG\n",
            )

        # set dash pattern
        # fmt: off
        LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{self.__border_dash_pattern} {self.__border_dash_phase} d\n")
        # fmt: on

        # IF all the border widths are the same
        # THEN draw a rectangle
        if (
            self.__border_width_bottom
            == self.__border_width_left
            == self.__border_width_right
            == self.__border_width_top
        ):
            LayoutElement._append_to_content_stream(
                page=page, bytes_or_string=f"{self.__border_width_bottom} w\n"
            )
            LayoutElement._append_to_content_stream(
                page=page, bytes_or_string=f"{x} {y} {w} {h} re\n"
            )
            if self.__background_color is not None and self.__border_color is not None:
                LayoutElement._append_to_content_stream(
                    page=page, bytes_or_string="B\n"
                )
            elif self.__background_color is not None:
                LayoutElement._append_to_content_stream(
                    page=page, bytes_or_string="f\n"
                )
            elif self.__border_color is not None:
                LayoutElement._append_to_content_stream(
                    page=page, bytes_or_string="S\n"
                )

        # IF the border widths are different
        # THEN we need to construct a path
        else:
            # background
            if self.__background_color is not None:
                # fmt: off
                LayoutElement._append_to_content_stream(page=page, bytes_or_string="0 w\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{x} {y} {w} {h} re\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string="f\n")
                # fmt: on
            # bottom
            if self.__border_color is not None and self.__border_width_bottom > 0:
                # fmt: off
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{self.__border_width_bottom} w\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{x} {y} m {x+w} {y} l S\n")
                # fmt: on
            # left
            if self.__border_color is not None and self.__border_width_left > 0:
                # fmt: off
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{self.__border_width_left} w\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{x} {y} m {x} {y+h} l S\n")
                # fmt: on
            # right
            if self.__border_color is not None and self.__border_width_right > 0:
                # fmt: off
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{self.__border_width_right} w\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{x+w} {y} m {x+w} {y+h} l S\n")
                # fmt: on
            # top
            if self.__border_color is not None and self.__border_width_top > 0:
                # fmt: off
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{self.__border_width_top} w\n")
                LayoutElement._append_to_content_stream(page=page, bytes_or_string=f"{x} {y+h} m {x+w} {y+h} l S\n")
                # fmt: on

        # restore the graphics state
        LayoutElement._append_to_content_stream(page=page, bytes_or_string="Q\n")

        return

    #
    # PUBLIC
    #

    def get_background_color(self) -> typing.Optional[Color]:
        """
        Return the background color of this LayoutElement.

        This function returns the background color of this LayoutElement, or None if no color is set.

        :return: The background color of this LayoutElement, or None if no color is set.
        """
        return self.__background_color

    def get_border_color(self) -> typing.Optional[Color]:
        """
        Get the border color of the layout element.

        This method returns the color used for the border of the layout element.
        If no border color has been set, it returns None.

        :return: An optional Color object representing the border color, or None if no color is set.
        """
        return self.__border_color

    def get_border_dash_pattern(self) -> typing.List[int]:
        """
        Get the dash pattern for the border of the layout element.

        This method returns a list of integers that define the dash pattern of the border.
        The dash pattern is represented as a sequence of lengths, where even-indexed values
        represent the lengths of the dashes and odd-indexed values represent the lengths of the gaps
        between the dashes. If no dash pattern has been set, the default pattern will be returned.

        :return: A list of integers representing the dash pattern for the border.
        """
        return self.__border_dash_pattern

    def get_border_dash_phase(self) -> int:
        """
        Get the dash phase of the border dash pattern.

        This method retrieves the phase offset for the dash pattern of the border. The phase
        specifies the starting point of the dash pattern, allowing for adjustments in the positioning
        of the dashes and gaps. If no dash phase has been set, it will return the default value.

        :return: An integer representing the dash phase for the border dash pattern.
        """
        return self.__border_dash_phase

    def get_border_width_bottom(self) -> int:
        """
        Get the width of the bottom border of the layout element.

        This method returns the width of the border at the bottom of the layout element.
        The width is specified in units relevant to the document's layout.

        :return: An integer representing the width of the bottom border in document units.
        """
        return self.__border_width_bottom

    def get_border_width_left(self) -> int:
        """
        Get the width of the left border of the layout element.

        This method retrieves the width of the border on the left side of the layout element.
        The width is measured in units relevant to the document's layout.

        :return: An integer representing the width of the left border in document units.
        """
        return self.__border_width_left

    def get_border_width_right(self) -> int:
        """
        Get the width of the right border of the layout element.

        This method returns the width of the border on the right side of the layout element.
        The width is specified in units that correspond to the document's layout.

        :return: An integer representing the width of the right border in document units.
        """
        return self.__border_width_right

    def get_border_width_top(self) -> int:
        """
        Get the width of the top border of the layout element.

        This method retrieves the width of the border at the top of the layout element.
        The width is measured in units that are relevant to the document's layout.

        :return: An integer representing the width of the top border in document units.
        """
        return self.__border_width_top

    def get_horizontal_alignment(self) -> HorizontalAlignment:
        """
        Return the horizontal alignment of this LayoutElement.

        This function returns the horizontal alignment setting for this LayoutElement.

        :return: The horizontal alignment of this LayoutElement.
        """
        return self.__horizontal_alignment

    def get_margin_bottom(self) -> int:
        """
        Return the bottom margin of this LayoutElement.

        This function returns the value of the bottom margin for this LayoutElement.

        :return: The bottom margin of this LayoutElement as an integer.
        """
        return self.__margin_bottom

    def get_margin_left(self) -> int:
        """
        Return the left margin of this LayoutElement.

        This function returns the value of the left margin for this LayoutElement.

        :return: The left margin of this LayoutElement as an integer.
        """
        return self.__margin_left

    def get_margin_right(self) -> int:
        """
        Return the right margin of this LayoutElement.

        This function returns the value of the right margin for this LayoutElement.

        :return: The right margin of this LayoutElement as an integer.
        """
        return self.__margin_right

    def get_margin_top(self) -> int:
        """
        Return the top margin of this LayoutElement.

        This function returns the value of the top margin for this LayoutElement.

        :return: The top margin of this LayoutElement as an integer.
        """
        return self.__margin_top

    def get_padding_bottom(self) -> int:
        """
        Return the bottom padding of this LayoutElement.

        This function returns the value of the bottom padding for this LayoutElement.

        :return: The bottom padding of this LayoutElement as an integer.
        """
        return self.__padding_bottom

    def get_padding_left(self) -> int:
        """
        Return the left padding of this LayoutElement.

        This function returns the value of the left padding for this LayoutElement.

        :return: The left padding of this LayoutElement as an integer.
        """
        return self.__padding_left

    def get_padding_right(self) -> int:
        """
        Return the right padding of this LayoutElement.

        This function returns the value of the right padding for this LayoutElement.

        :return: The right padding of this LayoutElement as an integer.
        """
        return self.__padding_right

    def get_padding_top(self) -> int:
        """
        Return the top padding of this LayoutElement.

        This function returns the value of the top padding for this LayoutElement.

        :return: The top padding of this LayoutElement as an integer.
        """
        return self.__padding_top

    def get_previous_paint_box(
        self,
    ) -> typing.Optional[typing.Tuple[int, int, int, int]]:
        """
        Get the bounding box of the previously painted element.

        This method returns the last recorded paint box of the element, which
        represents its position and dimensions on the PDF page.

        :return: A tuple (x, y, width, height) representing the last painted box,
                 or None if the element has not been painted yet.
        """
        return self.__previous_paint_box

    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        return 0, 0

    def get_vertical_alignment(self) -> VerticalAlignment:
        """
        Return the vertical alignment of this LayoutElement.

        This function returns the vertical alignment setting for this LayoutElement.

        :return: The vertical alignment of this LayoutElement.
        """
        return self.__vertical_alignment

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (x, y, width, height).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        return
