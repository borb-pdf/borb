from borb.pdf import (
    UsageStatistics,
    Document,
    SingleColumnLayout,
    PageLayout,
    Page,
    Paragraph,
)
from tests.test_case import TestCase


class TestUsageStatistics(TestCase):

    def test_usage_statistics(self):
        UsageStatistics.event(
            what="PDF.test",
            number_of_pages=1,
            number_of_documents=1,
        )

    def test_usage_statistics_implicitly(self):
        doc: Document = Document()

        page: Page = Page()
        doc.append_page(page)

        layout: PageLayout = SingleColumnLayout(page)

        layout.append_layout_element(Paragraph("Lorem Ipsum Dolor Sit Amet"))

        TestCase.write(what=doc, where_to="test_usage_statistics_implicitly.pdf")
