import pathlib
import unittest

from borb.pdf import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.annotation.sound_annotation import SoundAnnotation
from borb.pdf.page import Page
from tests.test_case import TestCase


@unittest.skipIf(True, "ffmpeg is not installed")
class TestSoundAnnotation(TestCase):

    def test_sound_annotation(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        SoundAnnotation(
            path_to_audio_file=pathlib.Path(
                "/usr/share/sounds/gnome/default/alerts/click.ogg"
            ),
            size=(100, 100),
            background_color=X11Color.YELLOW_MUNSELL,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        TestCase.write(what=d, where_to="test_sound_annotation.pdf")
