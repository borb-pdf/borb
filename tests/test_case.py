import pathlib
import typing
import unittest

from borb.pdf import Document, PDF
from tests.pdf_tests.visual_assert import VisualAssert


class TestCase(unittest.TestCase):

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def get_assets_dir() -> pathlib.Path:
        return TestCase.get_project_dir() / "tests" / "assets"

    @staticmethod
    def get_ground_truth_dir() -> pathlib.Path:
        return TestCase.get_project_dir() / "tests" / "ground_truth"

    @staticmethod
    def get_project_dir() -> pathlib.Path:
        me: pathlib.Path = pathlib.Path(__file__).resolve().parent
        while True:
            if (me / ".git").is_dir():
                return me
            if me.parent == me:
                break  # reached filesystem root
            me = me.parent
        raise FileNotFoundError(
            "Could not find project root (.git directory not found)"
        )

    @staticmethod
    def get_tests_dir() -> pathlib.Path:
        return TestCase.get_project_dir() / "tests"

    @staticmethod
    def write(
        what: Document,
        where_to: typing.Union[pathlib.Path, str, typing.BinaryIO],
    ) -> None:

        # canonize
        if isinstance(where_to, str):
            where_to = pathlib.Path(where_to)
        where_to = TestCase.get_assets_dir() / where_to.name

        # write
        PDF.write(what=what, where_to=where_to)

        # IF we are writing to a stream
        # THEN we can't really compare to the ground truth
        if isinstance(where_to, typing.BinaryIO):
            return

        # determine the ground-truth name
        stem: typing.Optional[str] = None
        if isinstance(where_to, pathlib.Path):
            stem = where_to.stem
        if isinstance(where_to, str):
            stem = pathlib.Path(where_to).stem
        assert stem is not None

        # compare
        VisualAssert.assert_equals(
            TestCase.get_ground_truth_dir() / f"{stem}.png",
            TestCase.get_assets_dir() / f"{stem}.pdf",
        )
