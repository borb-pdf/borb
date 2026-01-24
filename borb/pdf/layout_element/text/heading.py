#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a heading element in a PDF document.

The `Heading` class is designed to create and manage heading elements
within a PDF document. It not only defines the visual properties of the
heading (such as size and style) but also ensures that the heading entries
are correctly set in the PDF outline data structure. This functionality
is crucial for enabling PDF reading software to display the headings
in a structured and navigable manner, improving document accessibility.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.table_of_contents import TableOfContents


class Heading(Paragraph):
    """
    Represents a heading element in a PDF document.

    The `Heading` class is designed to create and manage heading elements
    within a PDF document. It not only defines the visual properties of the
    heading (such as size and style) but also ensures that the heading entries
    are correctly set in the PDF outline data structure. This functionality
    is crucial for enabling PDF reading software to display the headings
    in a structured and navigable manner, improving document accessibility.
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
        fixed_leading: typing.Optional[int] = None,
        font: typing.Optional[Font] = None,
        font_color: typing.Optional[Color] = None,
        font_size: typing.Optional[int] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        multiplied_leading: typing.Optional[float] = 1.2,
        outline_level: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a Heading object for a PDF document.

        The `Heading` class represents a heading element in the PDF document, combining the functionality of a
        `Paragraph` with special behavior for updating the PDF's internal structure to support a navigable
        document outline (Table of Contents) in PDF viewers. Headings are used to structure the document and
        enable hierarchical navigation.

        This constructor allows for the configuration of the heading's text, visual styling, alignment, and its
        contribution to the document outline. The `level` parameter defines the hierarchy of the heading, where
        smaller numbers (e.g., 1) represent higher levels in the hierarchy (like H1, H2, etc.).

        :param text:                   The text content of the heading.
        :param outline_level:          The level of the heading in the document hierarchy (default is 0).
        :param font:                   The font to use for the heading text (default is None, to be determined by outline_level).
        :param font_size:              The size of the font for the heading (default is None, to be determined by outline_level).
        :param font_color:             The color of the heading text (default is None, to be determined by outline_level).
        :param background_color:       The background color behind the heading (optional).
        :param border_color:           The color of the heading's border (optional).
        :param border_dash_pattern:    The dash pattern for the heading's border (default is solid).
        :param border_dash_phase:      The phase of the dash pattern for the border (default is 0).
        :param border_width_bottom:    The width of the bottom border (default is 0).
        :param border_width_left:      The width of the left border (default is 0).
        :param border_width_right:     The width of the right border (default is 0).
        :param border_width_top:       The width of the top border (default is 0).
        :param horizontal_alignment:   The horizontal alignment of the heading text (default is left-aligned).
        :param margin_bottom:          The margin below the heading (default is 10).
        :param margin_left:            The margin to the left of the heading (default is 0).
        :param margin_right:           The margin to the right of the heading (default is 0).
        :param margin_top:             The margin above the heading (default is 10).
        :param padding_bottom:         The padding below the heading text (default is 0).
        :param padding_left:           The padding to the left of the heading text (default is 0).
        :param padding_right:          The padding to the right of the heading text (default is 0).
        :param padding_top:            The padding above the heading text (default is 0).
        :param vertical_alignment:     The vertical alignment of the heading text (default is top-aligned).
        """
        super().__init__(
            text=text,
            font_color=font_color
            or Heading.__get_font_color_for_outline_level(outline_level=outline_level),
            font_size=font_size
            or Heading.__get_font_size_for_outline_level(outline_level=outline_level),
            font=font
            or Heading.__get_font_for_outline_level(outline_level=outline_level),
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
            padding_bottom=padding_bottom
            or Heading.__get_padding_for_outline_level(
                outline_level=outline_level, font_size=font_size
            ),
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top
            or Heading.__get_padding_for_outline_level(
                outline_level=outline_level, font_size=font_size
            ),
            vertical_alignment=vertical_alignment,
        )
        self.__outline_level: int = outline_level
        self.__text: str = text

    #
    # PRIVATE
    #

    @staticmethod
    def __get_children_of_outlines_dictionary(x):
        if "First" not in x:
            return []
        y = [x["First"]]
        while "Next" in y[-1]:
            y += [y[-1]["Next"]]
        return y

    @staticmethod
    def __get_font_color_for_outline_level(
        outline_level: int = 0,
    ):
        from borb.pdf import HexColor

        return {
            0: HexColor("#4472C4"),
            1: HexColor("#4472C4"),
            2: HexColor("#1F3763"),
            3: HexColor("#2F5496"),
            4: HexColor("#2F5496"),
            5: HexColor("#1F3763"),
        }.get(outline_level, X11Color.BLACK)

    @staticmethod
    def __get_font_for_outline_level(outline_level: int = 0):
        from borb.pdf import Standard14Fonts

        return {
            0: Standard14Fonts.get("Helvetica-Bold"),
            1: Standard14Fonts.get("Helvetica"),
            2: Standard14Fonts.get("Helvetica"),
            3: Standard14Fonts.get("Helvetica"),
            4: Standard14Fonts.get("Helvetica-Italic"),
            5: Standard14Fonts.get("Helvetica"),
        }.get(outline_level, Standard14Fonts.get("Helvetica"))

    @staticmethod
    def __get_font_size_for_outline_level(outline_level: int = 0):
        return {
            0: 17,
            1: 14,
            2: 13,
            3: 12,
            4: 12,
            5: 12,
        }.get(outline_level, 12)

    @staticmethod
    def __get_padding_for_outline_level(
        font_size: typing.Optional[int] = None,
        outline_level: int = 0,
    ) -> int:
        if font_size is None:
            font_size = Heading.__get_font_size_for_outline_level(
                outline_level=outline_level
            )
        return int(
            {
                0: 0.335,
                1: 0.553,
                2: 0.855,
                3: 1.333,
                4: 2.012,
                5: 3.477,
            }.get(outline_level, 1.2)
            * font_size
        )

    #
    # PUBLIC
    #

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
        super().paint(available_space=available_space, page=page)

        # get underlying Document
        from borb.pdf.document import Document

        doc: typing.Optional[Document] = page.get_document()
        assert doc is not None

        # get page number
        page_nr = next(
            iter(
                [
                    i
                    for i in range(0, doc.get_number_of_pages())
                    if doc.get_page(i) == page
                ]
            )
        )

        # IF outlines dictionary does not exist (yet)
        # THEN create it
        from borb.pdf.primitives import name

        if "Trailer" not in doc:
            doc[name("Trailer")] = {}
        if "Root" not in doc["Trailer"]:
            doc["Trailer"][name("Root")] = {}
        if "Outlines" not in doc["Trailer"]["Root"]:
            doc["Trailer"]["Root"][name("Outlines")] = {
                name("Type"): name("Outlines"),
                name("Count"): 0,
            }

        # create the outlines dictionary
        new_outlines_dictionary: typing.Dict[name, typing.Any] = {
            name("Dest"): [page_nr, name("Fit")],
            name("Title"): self.__text,
        }

        # IF the outlines dictionary is empty
        # THEN add this outline as the only entry
        outlines_dictionary = doc["Trailer"]["Root"]["Outlines"]
        if "First" not in outlines_dictionary or "Last" not in outlines_dictionary:
            outlines_dictionary[name("First")] = new_outlines_dictionary
            outlines_dictionary[name("Last")] = new_outlines_dictionary
            outlines_dictionary[name("Count")] = 1
            new_outlines_dictionary[name("Parent")] = outlines_dictionary

            # update TOC(s)
            tocs = [
                x
                for x in [doc.get_page(i) for i in range(0, doc.get_number_of_pages())]
                if isinstance(x, TableOfContents)
            ]
            if len(tocs) > 0:
                tocs[0]._TableOfContents__append_entry(  # type: ignore[attr-defined]
                    self.__outline_level, page_nr, self.__text
                )

            # return
            return

        # IF there are multiple entries
        # THEN we need to determine the correct parent

        # now we walk over the entire outlines dictionary tree
        done: typing.List[typing.Tuple[int, typing.Dict]] = []
        todo: typing.List[typing.Tuple[int, typing.Dict]] = [(-1, outlines_dictionary)]
        while len(todo) > 0:
            x: typing.Tuple[int, typing.Dict] = todo[0]
            todo.pop(0)
            done += [x]
            for y in Heading.__get_children_of_outlines_dictionary(x[1]):
                todo += [(x[0] + 1, y)]

        # find the parent outlines dictionary level
        # fmt: off
        parent_outlines_dictionary_level = max([x[0] for x in done if x[0] < self.__outline_level])
        # fmt: on

        # find the last parent outlines dictionary to match that level
        # fmt: off
        parent_outlines_dictionary = [x[1] for x in done if x[0] == parent_outlines_dictionary_level][-1]
        # fmt: on

        # update /Parent
        new_outlines_dictionary[name("Parent")] = parent_outlines_dictionary

        # update /Next /Last
        if "Last" in parent_outlines_dictionary:
            sibling_outlines_dictionary = parent_outlines_dictionary["Last"]
            sibling_outlines_dictionary[name("Next")] = new_outlines_dictionary
            parent_outlines_dictionary["Last"] = new_outlines_dictionary
        else:
            parent_outlines_dictionary[name("First")] = new_outlines_dictionary
            parent_outlines_dictionary[name("Last")] = new_outlines_dictionary

        # update /Count
        outlines_dictionary_to_update = parent_outlines_dictionary
        while outlines_dictionary_to_update:
            # fmt: off
            outlines_dictionary_to_update[name("Count")] = outlines_dictionary_to_update.get(name("Count"), 0) + 1
            outlines_dictionary_to_update = outlines_dictionary_to_update.get(name("Parent"), None)     # type: ignore[assignment]
            # fmt: on

        # update TOC(s)
        tocs = [
            x
            for x in [doc.get_page(i) for i in range(0, doc.get_number_of_pages())]
            if isinstance(x, TableOfContents)
        ]
        if len(tocs) > 0:
            tocs[0]._TableOfContents__append_entry(  # type: ignore[attr-defined]
                self.__outline_level, page_nr, self.__text
            )
