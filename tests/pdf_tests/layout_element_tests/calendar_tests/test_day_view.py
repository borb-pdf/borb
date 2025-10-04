import datetime
import unittest

from borb.pdf import HexColor
from borb.pdf.document import Document
from borb.pdf.layout_element.calendar.day_view import DayView
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestDayView(unittest.TestCase):

    def test_day_view(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        (
            DayView(
                font_size=8,
                lane_width=100,
            )
            .push_event(
                color=HexColor("FFB703"),
                from_hour=datetime.datetime(year=2025, month=10, day=2, hour=9),
                until_hour=datetime.datetime(
                    year=2025, month=10, day=2, hour=9, minute=30
                ),
                title="Lorem",
                description="ipsum dolor sit amet, consectetur adipiscing elit",
            )
            .push_event(
                color=HexColor("219EBC"),
                from_hour=datetime.datetime(year=2025, month=10, day=2, hour=10),
                until_hour=datetime.datetime(year=2025, month=10, day=2, hour=12),
                title="Ipsum",
                description="Dolor sit amet, consectetur adipiscing elit",
            )
            .push_event(
                from_hour=datetime.datetime(year=2025, month=10, day=2, hour=9),
                until_hour=datetime.datetime(year=2025, month=10, day=2, hour=10),
                title="Sit",
                description="Amet, consectetur adipiscing elit",
            )
            .paint(
                available_space=(x, y, w, h),
                page=p,
            )
        )

        PDF.write(what=d, where_to="assets/test_day_view.pdf")
