from borb.pdf.layout_element.shape.line_art import LineArt
from tests.test_case import TestCase


class TestLineArtRectangularMazeSize(TestCase):

    def test_line_rectangular_maze_size(self):
        w, h = LineArt.rectangular_maze().get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
