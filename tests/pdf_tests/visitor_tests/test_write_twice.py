import copy
import unittest

from borb.pdf import (
    Document,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    Page,
    PDF,
    LineArt,
    Image,
    LayoutElement,
    SquareAnnotation,
    TextAnnotation,
    TableUtil, Heading, Table, HexColor, FixedColumnWidthTable,
)


class TestWriteTwice(unittest.TestCase):

    def test_write_twice_with_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        d2 = copy.deepcopy(d1)
        PDF.write(what=d1, where_to="assets/test_write_twice_with_copy_a.pdf")
        PDF.write(what=d2, where_to="assets/test_write_twice_with_copy_b.pdf")

    def test_write_read_write_without_copy(self):

        # write
        d1: Document = Document()
        p: Page = Page()
        d1.append_page(p)
        l: PageLayout = SingleColumnLayout(p)
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))
        l.append_layout_element(LineArt.rectangle())
        l.append_layout_element(TextAnnotation(contents="Lorem ipsum"))
        l.append_layout_element(
            Image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm0Wq_2sTfpM9NisExXWpwhvxr5bPO2IUPfg&s",
                size=(100, 100),
            )
        )
        l.append_layout_element(
            TableUtil.from_2d_data(
                [["Lorem", "Ipsum"], [1, 2], [3, 4]]
            ).set_padding_on_all_cells(5, 5, 5, 5)
        )
        PDF.write(what=d1, where_to="assets/test_write_read_write_without_copy_a.pdf")

        # read
        d1 = PDF.read(
            where_from="assets/test_write_read_write_without_copy_a.pdf"
        )

        # write
        PDF.write(what=d1, where_to="assets/test_write_read_write_without_copy_b.pdf")

    def test_write_twice_without_copy(self):

        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(32)))

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_a.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_b.pdf")

    def test_write_twice_without_copy_002(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(LineArt.rectangle())

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_002_a.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_002_b.pdf")

    def test_write_twice_without_copy_003(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(
            Image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm0Wq_2sTfpM9NisExXWpwhvxr5bPO2IUPfg&s",
                size=(100, 100),
            )
        )

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_003_a.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_003_b.pdf")

    def test_write_twice_without_copy_004(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(TextAnnotation(contents="Lorem ipsum"))

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_004_a.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_004_b.pdf")

    def test_write_twice_without_copy_005(self):
        d1: Document = Document()

        p: Page = Page()
        d1.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        l.append_layout_element(
            TableUtil.from_2d_data(
                [["Lorem", "Ipsum"], [1, 2], [3, 4]]
            ).set_padding_on_all_cells(5, 5, 5, 5)
        )

        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_005_a.pdf")
        PDF.write(what=d1, where_to="assets/test_write_twice_without_copy_005_b.pdf")
