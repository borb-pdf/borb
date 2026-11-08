import random

from borb.pdf import Document, Page, SingleColumnLayout, Paragraph, Lipsum, PDF
from tests.test_case import TestCase
import cProfile


class TestProfile(TestCase):

    def test_profile_paragraph(self):

        random.seed(0)
        txt: str = Lipsum.generate_lorem_ipsum(500)

        # start profiler
        profiler = cProfile.Profile()
        profiler.enable()

        # borb code
        doc: Document = Document()
        page: Page = Page()
        doc.append_page(page)
        layout: SingleColumnLayout = SingleColumnLayout(page)
        for _ in range(1000):
            layout.append_layout_element(Paragraph(txt))

        # stop profiling
        profiler.disable()
        profiler.dump_stats(self.get_assets_dir() / "test_profile_paragraph.prof")

        # write
        self.write(what=doc, where_to="test_profile_paragraph.pdf")
