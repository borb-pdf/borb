#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A paragraph that dynamically truncates its content to fit within layout constraints.

This class extends :class:`HeterogeneousParagraph` to support automatic truncation
when text exceeds a specified width and/or height. The truncation process uses a
binary search strategy to determine the maximum number of chunks that fit within
the available layout space, ensuring the paragraph never overflows its container.

When truncation occurs, a designated truncation chunk (defaulting to an ellipsis,
i.e., ``"..."``) is appended at the cutoff point. The rest of the paragraph is
omitted from rendering. This makes the component suitable for dynamic or
data-driven layouts where available space may vary, such as in table cells,
labels, or UI overlays.

Layout constraints may be provided explicitly via ``max_width`` and ``max_height``,
or inherited from the rendering context’s available space. All standard paragraph
styling parameters—alignment, padding, margins, and line spacing—are preserved.
"""

import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph


class SelfTruncatingHeterogeneousParagraph(HeterogeneousParagraph):
    """
    A paragraph that dynamically truncates its content to fit within layout constraints.

    This class extends :class:`HeterogeneousParagraph` to support automatic truncation
    when text exceeds a specified width and/or height. The truncation process uses a
    binary search strategy to determine the maximum number of chunks that fit within
    the available layout space, ensuring the paragraph never overflows its container.

    When truncation occurs, a designated truncation chunk (defaulting to an ellipsis,
    i.e., ``"..."``) is appended at the cutoff point. The rest of the paragraph is
    omitted from rendering. This makes the component suitable for dynamic or
    data-driven layouts where available space may vary, such as in table cells,
    labels, or UI overlays.

    Layout constraints may be provided explicitly via ``max_width`` and ``max_height``,
    or inherited from the rendering context’s available space. All standard paragraph
    styling parameters—alignment, padding, margins, and line spacing—are preserved.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        chunks: typing.List[Chunk],
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.Optional[typing.List[int]] = None,
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        fixed_leading: typing.Optional[int] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        max_height: typing.Optional[int] = None,
        max_width: typing.Optional[int] = None,
        multiplied_leading: typing.Optional[float] = 1.2,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        preserve_whitespaces: bool = False,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        truncation_chunk: typing.Optional[Chunk] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a self-truncating heterogeneous paragraph.

        The paragraph automatically truncates its content based on available
        layout space, appending a truncation chunk (defaulting to "...") when
        content exceeds the specified constraints.

        :param chunks: The list of text chunks in the paragraph.
        :param background_color: The background color of the paragraph.
        :param border_color: The color of the paragraph border.
        :param border_dash_pattern: The dash pattern for the border, if any.
        :param border_dash_phase: The phase offset for the border dash pattern.
        :param border_width_bottom: The width of the bottom border.
        :param border_width_left: The width of the left border.
        :param border_width_right: The width of the right border.
        :param border_width_top: The width of the top border.
        :param fixed_leading: The fixed leading (line spacing).
        :param horizontal_alignment: The horizontal alignment of the paragraph.
        :param margin_bottom: The bottom margin.
        :param margin_left: The left margin.
        :param margin_right: The right margin.
        :param margin_top: The top margin.
        :param max_height: The maximum allowed height before truncation.
        :param max_width: The maximum allowed width before truncation.
        :param multiplied_leading: The multiplier for line spacing.
        :param padding_bottom: The bottom padding.
        :param padding_left: The left padding.
        :param padding_right: The right padding.
        :param padding_top: The top padding.
        :param preserve_whitespaces: Whether to preserve leading/trailing whitespaces.
        :param text_alignment: The text alignment mode.
        :param truncation_chunk: The chunk appended when truncation occurs.
        :param vertical_alignment: The vertical alignment of the paragraph.
        """
        super().__init__(
            chunks=chunks,
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            fixed_leading=fixed_leading,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            multiplied_leading=multiplied_leading,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            preserve_whitespaces=preserve_whitespaces,
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
        )
        self.__max_width: typing.Optional[int] = max_width
        self.__max_height: typing.Optional[int] = max_height
        self.__truncation_chunk: Chunk = truncation_chunk or Chunk("...")
        self.__truncation_index: int = len(self._HeterogeneousParagraph__chunks)  # type: ignore[attr-defined]

    #
    # PRIVATE
    #

    def __get_lines(  # type: ignore[override]
        self,
        available_space: typing.Tuple[int, int],
        preserve_whitespaces: bool = False,
    ) -> typing.List[typing.List[Chunk]]:

        current_line_width: int = 0
        lines: typing.List[typing.List[Chunk]] = [[]]

        # IF we have truncated the text
        # THEN append the truncation chunk
        chunks_to_render = self._HeterogeneousParagraph__chunks  # type: ignore[attr-defined]
        if self.__truncation_index != len(self._HeterogeneousParagraph__chunks) - 1:  # type: ignore[attr-defined]
            chunks_to_render = self._HeterogeneousParagraph__chunks[  # type: ignore[attr-defined]
                : self.__truncation_index
            ] + [
                self.__truncation_chunk
            ]

        # convert these chunks to lines
        for c in chunks_to_render:
            w, h = c.get_size(available_space=available_space)

            # IF the chunk fits on the line
            # THEN append the chunk to the line
            # THEN update the current_line_width
            if current_line_width + w <= available_space[0]:
                current_line_width += w
                lines[-1] += [c]
                continue

            # start a new line
            lines += [[c]]
            current_line_width = w

        # remove leading/trailing spaces
        if not preserve_whitespaces:
            for i in range(0, len(lines)):
                # remove leading space
                while len(lines[i]) > 0 and lines[i][0].get_text().isspace():
                    lines[i].pop(0)
                # remove trailing space
                while len(lines[i]) > 0 and lines[i][-1].get_text().isspace():
                    lines[i].pop(-1)

        # return
        return lines

    #
    # PUBLIC
    #

    @functools.cache
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
        # monkey-patching
        self._HeterogeneousParagraph__get_lines = self.__get_lines

        # uncached super method
        uncached_super_get_size = super().get_size.__wrapped__

        # perform binary search
        chunks = self._HeterogeneousParagraph__chunks  # type: ignore[attr-defined]
        n = len(chunks)
        low, high = 0, n
        best_fit = 0  # full text fits by default
        while low < high:
            mid = (low + high) // 2
            self.__truncation_index = mid

            w, h = uncached_super_get_size(
                self,
                available_space=(
                    (
                        available_space[0]
                        if self.__max_width is None
                        else min(self.__max_width, available_space[0])
                    ),
                    (
                        available_space[1]
                        if self.__max_height is None
                        else min(self.__max_height, available_space[1])
                    ),
                ),
            )

            fits = (self.__max_height is None or h < self.__max_height) and (
                self.__max_width is None or w < self.__max_width
            )

            if fits:
                best_fit = mid
                low = mid + 1  # try a longer version
            else:
                high = mid  # try shorter version

        # calculate the width and height
        # the super call to get_size will use the modified get_lines
        # which should work perfectly
        self.__truncation_index = best_fit
        return super().get_size(available_space=available_space)
