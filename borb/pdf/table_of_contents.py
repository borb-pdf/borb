#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a table of contents within a PDF document.

The `TableOfContents` class is responsible for generating and rendering
a table of contents on a dedicated page. It collects and organizes
headings defined throughout the document and presents them in a hierarchical
list structure. Each entry is displayed according to its level, with
configurable visual properties such as indentation, numbering, and alignment.

This ensures that the table of contents provides a clear and structured
overview of the document's content, improving readability and organization.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hex_color import HexColor
from borb.pdf.document import Document
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout


class TableOfContents(Page):
    """
    Represents a table of contents within a PDF document.

    The `TableOfContents` class is responsible for generating and rendering
    a table of contents on a dedicated page. It collects and organizes
    headings defined throughout the document and presents them in a hierarchical
    list structure. Each entry is displayed according to its level, with
    configurable visual properties such as indentation, numbering, and alignment.

    This ensures that the table of contents provides a clear and structured
    overview of the document's content, improving readability and organization.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        height_in_points: int = 842,
        table_of_contents_font_color: typing.Optional[Color] = None,
        table_of_contents_font: typing.Optional[Font] = None,
        table_of_contents_font_size: int = 17,
        table_of_contents_title: str = "Contents",
        width_in_points: int = 595,
    ):
        """
        Initialize a new TableOfContents object with specified dimensions.

        The `TableOfContents` class represents a dedicated page in a PDF document
        that lists the document's headings in a structured, hierarchical format.
        This constructor allows the creation of the table of contents page with
        customizable dimensions, typically matching standard page sizes such as
        A4 or letter.

        :param height_in_points:    The height of the page in points. Default is 842 points (A4 height).
        :param width_in_points:     The width of the page in points. Default is 595 points (A4 width).
        """
        # fmt: off
        super().__init__(height_in_points, width_in_points)
        self.__end_page_index: typing.Optional[int] = None
        self.__entries: typing.List[typing.Tuple[int, int, str]] = []
        self.__persistent_document: typing.Optional[Document] = None
        self.__start_page_index: typing.Optional[int] = None
        self.__table_of_contents_font_color: Color = table_of_contents_font_color or HexColor("2F5496")
        self.__table_of_contents_font: Font = table_of_contents_font or Standard14Fonts.get("Helvetica") # type: ignore[assignment]
        self.__table_of_contents_font_size: int = table_of_contents_font_size
        self.__table_of_contents_title: str = table_of_contents_title
        # fmt: on

    #
    # PRIVATE
    #

    def __append_entry(
        self, outline_level: int, page_number: int, text: str
    ) -> "TableOfContents":

        # append entry
        self.__entries += [(outline_level, page_number, text)]

        # store a reference to the Document
        if self.__persistent_document is None:
            self.__persistent_document = self.get_document()

        # calculate new page range
        from borb.pdf import Table

        W, H = self.get_size()
        entries_per_page: typing.List[Table] = []

        number_as_list = [1]
        for i in range(0, len(self.__entries)):

            if len(entries_per_page) == 0:
                entries_per_page += [
                    self.__create_initial_table(
                        include_title=True,
                        level=self.__entries[i][0],
                        number=number_as_list,
                        page_nr=self.__entries[i][1],
                        text=self.__entries[i][2],
                    )
                ]
                continue

            existing_table = entries_per_page[-1]

            # update numbers_as_list
            if self.__entries[i][0] == self.__entries[i - 1][0]:
                number_as_list[-1] += 1
            elif self.__entries[i][0] > self.__entries[i - 1][0]:
                number_as_list += [1]
            elif self.__entries[i][0] < self.__entries[i - 1][0]:
                number_as_list = number_as_list[:-1]
                number_as_list[-1] += 1

            # add the new data
            existing_table = self.__update_table(
                level=self.__entries[i][0],
                number=number_as_list,
                page_nr=self.__entries[i][1],
                table=existing_table,
                text=self.__entries[i][2],
            )

            # IF the table is now too big to fit on a page
            # THEN undo
            if existing_table.get_size((W, H))[1] > H * 0.8:

                # UNDO
                existing_table = self.__undo_update_table(existing_table)

                # create a new Table
                entries_per_page += [
                    self.__create_initial_table(
                        include_title=False,
                        level=self.__entries[i][0],
                        number=number_as_list,
                        page_nr=self.__entries[i][1],
                        text=self.__entries[i][2],
                    )
                ]

        # determine how many pages we now need
        new_nof_pages_needed: int = len(entries_per_page)

        # initial setup of self.__start_page_index and self.__end_page_index
        assert self.__persistent_document is not None
        if self.__start_page_index is None:
            self.__start_page_index = min(
                [
                    x
                    for x, y in [
                        (i, self.__persistent_document.get_page(i))
                        for i in range(
                            0, self.__persistent_document.get_number_of_pages()
                        )
                    ]
                    if isinstance(y, TableOfContents)
                ]
            )
            self.__end_page_index = self.__start_page_index + new_nof_pages_needed - 1

        # remove old page(s)
        assert self.__end_page_index is not None
        assert self.__start_page_index is not None
        old_nof_pages_needed: int = self.__end_page_index - self.__start_page_index + 1
        for i in range(0, old_nof_pages_needed):
            self.__persistent_document.pop_page(self.__start_page_index)

        # previously we (the TOC) took up old_nof_pages_needed
        # we now to take up new_nof_pages_needed
        # shift everything, if needed
        if new_nof_pages_needed > old_nof_pages_needed:
            self.__end_page_index = self.__start_page_index + new_nof_pages_needed - 1
            self.__shift_outlines(
                document=self.__persistent_document,
                delta=new_nof_pages_needed - old_nof_pages_needed,
            )

        # perform rendering
        for i in range(0, new_nof_pages_needed):

            # create Page
            toc_page: Page = TableOfContents()
            toc_page.__start_page_index = self.__start_page_index  # type: ignore[attr-defined]
            toc_page.__end_page_index = self.__end_page_index  # type: ignore[attr-defined]
            toc_page.__entries = self.__entries  # type: ignore[attr-defined]
            toc_page.__persistent_document = self.__persistent_document  # type: ignore[attr-defined]

            # set PageLayout
            layout_for_toc_page: PageLayout = SingleColumnLayout(toc_page)

            # append Table
            layout_for_toc_page.append_layout_element(entries_per_page[0])
            entries_per_page = entries_per_page[1:]

            # insert Page
            self.__persistent_document.insert_page(
                page=toc_page, index=self.__start_page_index + i
            )

        # return
        return self

    def __create_initial_table(
        self,
        include_title: bool,
        level: int,
        number: typing.List[int],
        page_nr: int,
        text: str,
    ) -> Table:
        t: typing.Optional[Table] = None
        if include_title:
            t = FixedColumnWidthTable(
                number_of_rows=2, number_of_columns=3, column_widths=[10, 80, 10]
            )
            t.append_layout_element(
                Table.TableCell(
                    Paragraph(
                        text=self.__table_of_contents_title,
                        padding_bottom=20,
                        font_size=self.__table_of_contents_font_size,
                        font_color=self.__table_of_contents_font_color,
                    ),
                    column_span=3,
                    row_span=1,
                )
            )
        else:
            t = FixedColumnWidthTable(
                number_of_rows=1, number_of_columns=3, column_widths=[10, 80, 10]
            )

        # convert (list of) number(s) to legible text
        number_as_str: str = ".".join([str(x) for x in number])

        # append new data
        t.append_layout_element(Paragraph(f"{number_as_str}"))
        t.append_layout_element(
            Paragraph(
                text,
                padding_left=int(12 * 0.250 * 3 * level),
            )
        )
        t.append_layout_element(
            Paragraph(
                f"{page_nr}",
                text_alignment=LayoutElement.TextAlignment.RIGHT,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )

        # set global properties
        t.no_borders()
        t.set_padding_on_all_cells(
            padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
        )
        # return
        return t

    def __shift_outlines(self, document: Document, delta: int) -> None:
        if delta == 0:
            return
        # TODO
        pass

    def __undo_update_table(self, table: Table) -> Table:

        # decrease number of rows
        table._Table__number_of_rows -= 1  # type: ignore[attr-defined]

        # find elements to be removed
        to_remove = table._Table__inner_layout_elements[-3:]  # type: ignore[attr-defined]

        # remove the elements
        table._Table__inner_layout_elements = table._Table__inner_layout_elements[:-3]  # type: ignore[attr-defined]

        # remove the mapping
        for e in to_remove:
            table._Table__inner_layout_element_to_table_coordinates.remove(e)  # type: ignore[attr-defined]

        # return
        return table

    def __update_table(
        self,
        level: int,
        number: typing.List[int],
        page_nr: int,
        table: Table,
        text: str,
    ) -> Table:

        # dangerous
        # fmt: off
        table._Table__number_of_rows += 1                                                                           # type: ignore[attr-defined]
        table._Table__available_table_coordinates += [(table._Table__number_of_rows - 1, i) for i in range(0, 3)]   # type: ignore[attr-defined]
        # fmt: on

        # convert (list of) number(s) to legible text
        number_as_str: str = ".".join([str(x) for x in number])

        # append new data
        table.append_layout_element(Paragraph(f"{number_as_str}"))
        table.append_layout_element(
            Paragraph(
                text,
                padding_left=int(12 * 0.250 * 3 * level),
            )
        )
        table.append_layout_element(
            Paragraph(
                f"{page_nr}",
                text_alignment=LayoutElement.TextAlignment.RIGHT,
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
            )
        )

        # set global properties
        table.no_borders()
        table.set_padding_on_all_cells(
            padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
        )

        # return
        return table

    #
    # PUBLIC
    #
