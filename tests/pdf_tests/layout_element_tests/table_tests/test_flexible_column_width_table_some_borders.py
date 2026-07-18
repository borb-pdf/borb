import unittest

from borb.pdf import Table
from borb.pdf.document import Document
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestFlexibleColumnWidthTableSomeBorders(unittest.TestCase):

    def test_flexible_column_width_table_some_borders(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    border_radius_top_left=10,
                    border_width_left=1,
                    border_width_top=0,
                )
            )
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    border_radius_top_right=10,
                    border_width_top=1,
                    border_width_right=0,
                )
            )
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    border_radius_bottom_left=10,
                    border_width_left=0,
                    border_width_bottom=1,
                )
            )
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    border_radius_bottom_right=10,
                    border_width_bottom=0,
                    border_width_left=1,
                )
            )
        ).set_padding_on_all_cells(
            padding_bottom=5, padding_left=5, padding_right=5, padding_top=5
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(
            what=d,
            where_to="assets/test_flexible_column_width_table_some_borders.pdf",
        )
