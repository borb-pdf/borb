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

from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.page import Page
from borb.pdf.document import Document


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
    def __init__(self, height_in_points: int = 842, width_in_points: int = 595):
        super().__init__(height_in_points, width_in_points)
        self.__entries: typing.List[typing.Tuple[int, int, str]] = []
        self._start_page_index: typing.Optional[int] = None
        self._end_page_index: typing.Optional[int] = None
        self._persistent_document: typing.Optional[Document] = None

    #
    # PRIVATE
    #

    def __append_entry(
        self, outline_level: int, page_number: int, text: str
    ) -> "TableOfContents":

        # append entry
        print("")
        print(f"entry added to TOC")
        self.__entries += [(outline_level, page_number, text)]

        # store a reference to the Document
        if self._persistent_document is None:
            print(f"setting self._persistent_document to {self.get_document()}")
            self._persistent_document = self.get_document()

        # calculate new page range
        from borb.pdf import Table
        from borb.pdf import FixedColumnWidthTable

        W, H = self.get_size()
        entries_per_page: typing.List[Table] = []

        for entry in self.__entries:

            level: str = f"{entry[0]}"
            page_nr: str = f"pg. {entry[1]}"
            text: str = entry[2]

            if len(entries_per_page) == 0:
                entries_per_page += [
                    FixedColumnWidthTable(
                        number_of_rows=1, number_of_columns=3, column_widths=[5, 85, 10]
                    )
                    .append_layout_element(Paragraph(level))
                    .append_layout_element(Paragraph(text))
                    .append_layout_element(
                        Paragraph(
                            page_nr,
                            text_alignment=LayoutElement.TextAlignment.RIGHT,
                            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                        )
                    )
                    .set_padding_on_all_cells(
                        padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
                    )
                ]
                continue

            existing_table = entries_per_page[-1]

            # add the new data
            existing_table._Table__number_of_rows = (
                existing_table._Table__number_of_rows + 1
            )
            existing_table._Table__available_table_coordinates += [
                (existing_table._Table__number_of_rows - 1, i) for i in range(0, 3)
            ]
            existing_table.append_layout_element(Paragraph(level))
            existing_table.append_layout_element(Paragraph(text))
            existing_table.append_layout_element(
                Paragraph(
                    page_nr,
                    text_alignment=LayoutElement.TextAlignment.RIGHT,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                )
            )
            existing_table.set_padding_on_all_cells(
                padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
            )

            # IF the table is now too big to fit on a page
            # THEN undo
            if existing_table.get_size((W, H))[1] > H * 0.8:

                # decrease number of rows
                existing_table._Table__number_of_rows = (
                    existing_table._Table__number_of_rows - 1
                )

                # find elements to be removed
                to_remove = existing_table._Table__inner_layout_elements[-3:]

                # remove the elements
                existing_table._Table__inner_layout_elements = (
                    existing_table._Table__inner_layout_elements[:-3]
                )

                # remove the mapping
                for e in to_remove:
                    existing_table._Table__inner_layout_element_to_table_coordinates.remove(
                        e
                    )

                # create a new Table
                entries_per_page += [
                    FixedColumnWidthTable(
                        number_of_rows=1, number_of_columns=3, column_widths=[5, 85, 10]
                    )
                    .append_layout_element(Paragraph(level))
                    .append_layout_element(Paragraph(text))
                    .append_layout_element(
                        Paragraph(
                            page_nr,
                            text_alignment=LayoutElement.TextAlignment.RIGHT,
                            horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                        )
                    )
                    .set_padding_on_all_cells(
                        padding_bottom=3, padding_left=3, padding_right=3, padding_top=3
                    )
                ]

        # determine how many pages we now need
        new_nof_pages_needed: int = len(entries_per_page)
        print(f"TOC requires {new_nof_pages_needed} page(s)")

        # initial setup of self._start_page_index and self_end_page_index
        if self._start_page_index is None:
            self._start_page_index = min(
                [
                    x
                    for x, y in [
                        (i, doc.get_page(i))
                        for i in range(
                            0, self._persistent_document.get_number_of_pages()
                        )
                    ]
                    if isinstance(y, TableOfContents)
                ]
            )
            self._end_page_index = self._start_page_index + new_nof_pages_needed - 1
            print(
                f"TOC starts at {self._start_page_index}, ends at page {self._end_page_index}"
            )

        # remove old page(s)
        old_nof_pages_needed: int = self._end_page_index - self._start_page_index + 1
        for i in range(0, old_nof_pages_needed):
            print(f"removing old TOC at page {self._start_page_index}")
            self._persistent_document.pop_page(self._start_page_index)

        # previously we (the TOC) took up old_nof_pages_needed
        # we now to take up new_nof_pages_needed
        # shift everything, if needed
        if new_nof_pages_needed > old_nof_pages_needed:
            self._end_page_index = self._start_page_index + new_nof_pages_needed - 1
            TableOfContents.__shift_outlines(
                document=self._persisent_document,
                delta=new_nof_pages_needed - old_nof_pages_needed,
            )

        # perform rendering
        print(f"rendering new TOC")
        for i in range(0, new_nof_pages_needed):

            # create Page
            toc_page: Page = TableOfContents()
            toc_page._start_page_index = self._start_page_index
            toc_page._end_page_index = self._end_page_index
            toc_page.__entries = self.__entries
            toc_page._persistent_document = self._persistent_document

            # set PageLayout
            layout_for_toc_page: PageLayout = SingleColumnLayout(toc_page)

            # append Table
            layout_for_toc_page.append_layout_element(entries_per_page[0])
            entries_per_page = entries_per_page[1:]

            # insert Page
            self._persistent_document.insert_page(
                page=toc_page, index=self._start_page_index + i
            )

        # return
        return self

    @staticmethod
    def __shift_outlines(document: Document, delta: int) -> None:
        if delta == 0:
            return
        pass

    #
    # PUBLIC
    #
