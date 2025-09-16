import unittest

from borb.pdf import Document, PageLayout, SingleColumnLayout, UnorderedList, Paragraph, Page, PDF


class TestOrderedListMultilineParagraph(unittest.TestCase):

    def test_ordered_list_multiline_paragraph(self):

        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        layout.append_layout_element(UnorderedList()
                                     .append_layout_element(Paragraph("This is a list item with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus."))
                                     .append_layout_element(Paragraph("Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus. Donec sit amet nisl. Aliquam semper ipsum sit amet velit."))
                                     .append_layout_element(Paragraph("Suspendisse id sem consectetuer libero luctus adipiscing."))
                                     )

        PDF.write(what=doc, where_to="assets/test_ordered_list_multiline_paragraph.pdf")