import collections
import pathlib
import re
import typing
import sys

WarningType = collections.namedtuple(
    "WarningType",
    field_names=[
        "file",
        "function",
        "line_number",
        "text",
    ],
)


class CheckSomethingTemplate:

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        root: pathlib.Path,
        known_exceptions: typing.List[typing.Union[pathlib.Path, str]],
    ):
        self.__root: pathlib.Path = root
        self.__warnings: typing.List[WarningType] = []
        self.__number_of_files_checked: int = 0
        self.__known_exceptions: typing.List[pathlib.Path] = known_exceptions

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_number_of_files_checked(self) -> int:
        return self.__number_of_files_checked

    def get_warnings(self) -> typing.List[WarningType]:
        return self.__warnings

    def perform_check_on_directory(self) -> None:
        stk_todo = [self.__root]
        stk_done = []
        while len(stk_todo) > 0:
            f = stk_todo.pop(0)
            if f.is_dir():

                # IF we have reached the /.github directory
                # THEN do not delve into it
                if f.name == ".github":
                    continue

                # IF we have reached the /.venv directory
                # THEN do not delve into it
                if f.name == ".venv":
                    continue

                # IF we have reached the /tests directory
                # THEN do not delve into it
                if f.name == "tests":
                    continue
                stk_todo += [subdir for subdir in f.iterdir()]
            else:
                if f.name.endswith(".py"):
                    stk_done += [f]

        # filter out known_exceptions
        # fmt: off
        known_exceptions_01 = [x for x in self.__known_exceptions if isinstance(x, pathlib.Path)]
        known_exceptions_02 = [re.compile(x) for x in self.__known_exceptions if isinstance(x, str)]
        stk_done = [x for x in stk_done if x not in known_exceptions_01]
        stk_done = [x for x in stk_done if not any([y.match(x.name) is not None for y in known_exceptions_02])]
        # fmt: on

        # perform_check_on_file for each item in stk_done
        stk_done.sort(key=lambda x: x.name)
        for f in stk_done:
            self.perform_check_on_file(f)

    def perform_check_on_file(self, file: pathlib.Path) -> None:
        self.__number_of_files_checked += 1
        lines: typing.List[str] = []
        try:
            with open(file, "r") as fh:
                lines = fh.readlines()
        except:
            return
        if len(lines) > 512:
            self.__warnings += [
                WarningType(
                    file=file,
                    function=None,
                    line_number=513,
                    text=f"{len(lines)} > 512",
                )
            ]


if __name__ == "__main__":
    checker = CheckSomethingTemplate(
        root=pathlib.Path(sys.argv[1]),
        known_exceptions=[
            "a4_portrait.py",
            "a4_portrait_invoice.py",
            "adobe_glyph_list.py",
            "avatar.py",
            "conformance_checks.py",
            "dict_visitor.py",
            "emoji.py",
            "layout_element.py",
            "line_art.py",
            "map.py",
            "pantone_color.py",
            "shape.py",
            "slideshow.py",
            "smart_art.py",
            "source.py",
            "table.py",
            "week_view.py",
        ],
    )
    checker.perform_check_on_directory()
    warnings: typing.List[WarningType] = checker.get_warnings()

    # IF everything passed
    # THEN display pass text
    if len(warnings) == 0:
        print(
            f"Finished checking {checker.get_number_of_files_checked()} file(s), everything OK"
        )

    # IF there are warnings
    # THEN display them
    if len(warnings) > 0:
        print(
            f"Finished checking {checker.get_number_of_files_checked()} file(s), found {len(warnings)} warnings:"
        )
        for w in warnings:
            if (
                w.file is not None
                and w.function is not None
                and w.line_number is not None
                and w.text is not None
            ):
                print(f"{w.file}:{w.function}:{w.line_number} {w.text}")
                continue
            if w.file is not None and w.line_number is not None and w.text is not None:
                print(f"{w.file}:{w.line_number} {w.text}")
                continue
            if w.file is not None and w.text is not None:
                print(f"{w.file} {w.text}")
                continue
            if w.file is not None:
                print(f"{w.file}")
                continue

        sys.exit(1)
