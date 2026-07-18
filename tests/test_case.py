import pathlib
import unittest


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
