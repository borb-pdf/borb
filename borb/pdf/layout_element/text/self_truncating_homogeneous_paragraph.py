#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A paragraph composed of a single, stylistically uniform text chunk that truncates automatically.

This class behaves like :class:`SelfTruncatingHeterogeneousParagraph` but is optimized
for text with a single consistent style — font, size, color, and spacing. It wraps the
text into one :class:`Chunk` internally, applying the same font and rendering parameters
across the entire paragraph.

The paragraph automatically truncates its content to fit within specified layout
constraints, appending a truncation marker (defaulting to an ellipsis, i.e., ``"..."``)
when necessary. It preserves all layout behavior from its heterogeneous counterpart,
including margins, padding, alignment, and line spacing, while simplifying text setup
for common use cases where mixed styling is not required.

This makes the component ideal for static text fields, UI labels, or table cells
where space is limited but text should remain stylistically consistent.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.self_truncating_heterogeneous_paragraph import (
    SelfTruncatingHeterogeneousParagraph,
)


class SelfTruncatingHomogeneousParagraph(SelfTruncatingHeterogeneousParagraph):
    """
    A paragraph composed of a single, stylistically uniform text chunk that truncates automatically.

    This class behaves like :class:`SelfTruncatingHeterogeneousParagraph` but is optimized
    for text with a single consistent style — font, size, color, and spacing. It wraps the
    text into one :class:`Chunk` internally, applying the same font and rendering parameters
    across the entire paragraph.

    The paragraph automatically truncates its content to fit within specified layout
    constraints, appending a truncation marker (defaulting to an ellipsis, i.e., ``"..."``)
    when necessary. It preserves all layout behavior from its heterogeneous counterpart,
    including margins, padding, alignment, and line spacing, while simplifying text setup
    for common use cases where mixed styling is not required.

    This makes the component ideal for static text fields, UI labels, or table cells
    where space is limited but text should remain stylistically consistent.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.Optional[typing.List[int]] = None,
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        character_spacing: float = 0,
        fixed_leading: typing.Optional[int] = None,
        font: typing.Optional[typing.Union[Font, str]] = None,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
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
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        truncation_chunk: typing.Optional[Chunk] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        word_spacing: float = 0,
    ):
        """
        Initialize a self-truncating homogeneous paragraph.

        This constructor creates a paragraph consisting of a single :class:`Chunk`
        with uniform text styling. The paragraph automatically truncates its content
        when it exceeds the available layout space or the specified ``max_width`` and
        ``max_height`` constraints. When truncation occurs, a truncation chunk
        (defaulting to an ellipsis rendered with the same style) is appended.

        :param text: The text content of the paragraph.
        :param background_color: The background color of the paragraph.
        :param border_color: The color of the paragraph border.
        :param border_dash_pattern: The dash pattern for the border, if any.
        :param border_dash_phase: The phase offset for the border dash pattern.
        :param border_width_bottom: The width of the bottom border.
        :param border_width_left: The width of the left border.
        :param border_width_right: The width of the right border.
        :param border_width_top: The width of the top border.
        :param character_spacing: Additional spacing between individual characters.
        :param fixed_leading: The fixed leading (line spacing) between lines.
        :param font: The font to use for rendering the text.
        :param font_color: The color of the text.
        :param font_size: The size of the font in points.
        :param horizontal_alignment: The horizontal alignment of the paragraph.
        :param margin_bottom: The bottom margin.
        :param margin_left: The left margin.
        :param margin_right: The right margin.
        :param margin_top: The top margin.
        :param max_height: The maximum allowed height before truncation.
        :param max_width: The maximum allowed width before truncation.
        :param multiplied_leading: The multiplier for line spacing relative to font size.
        :param padding_bottom: The bottom padding.
        :param padding_left: The left padding.
        :param padding_right: The right padding.
        :param padding_top: The top padding.
        :param text_alignment: The text alignment mode.
        :param truncation_chunk: The chunk appended when truncation occurs.
        :param vertical_alignment: The vertical alignment of the paragraph.
        :param word_spacing: Additional spacing between words.
        """
        super().__init__(
            chunks=[
                Chunk(
                    text=text,
                    character_spacing=character_spacing,
                    font=font,
                    font_color=font_color,
                    font_size=font_size,
                    word_spacing=word_spacing,
                )
            ],
            background_color=background_color,
            fixed_leading=fixed_leading,
            multiplied_leading=multiplied_leading,
            text_alignment=text_alignment,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            max_height=max_height,
            max_width=max_width,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            truncation_chunk=truncation_chunk
            or Chunk(
                "...",
                character_spacing=character_spacing,
                font=font,
                font_color=font_color,
                font_size=font_size,
                word_spacing=word_spacing,
            ),
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
