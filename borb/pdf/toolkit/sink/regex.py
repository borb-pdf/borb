#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A sink class that captures text matching a regular expression from the PDF content pipeline.

The Regex class sits at the end of the PDF processing pipeline, serving as a sink to
detect and collect text fragments whose content matches a given regular expression.
As the page content is processed, it evaluates text rendering events against the
configured pattern and records the bounding boxes of all matching occurrences.

This class does not alter the content stream but rather listens for text-related events,
aggregates matches across the page, and exposes their positional information for
downstream processing, analysis, or extraction workflows.
"""

import re
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.page_size import PageSize
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.text_event import TextEvent

# define a Rectangle
RectangleType = typing.Tuple[float, float, float, float]


class Regex(Sink):
    """
    A sink class that captures text matching a regular expression from the PDF content pipeline.

    The Regex class sits at the end of the PDF processing pipeline, serving as a sink to
    detect and collect text fragments whose content matches a given regular expression.
    As the page content is processed, it evaluates text rendering events against the
    configured pattern and records the bounding boxes of all matching occurrences.

    This class does not alter the content stream but rather listens for text-related events,
    aggregates matches across the page, and exposes their positional information for
    downstream processing, analysis, or extraction workflows.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, pattern: typing.Union[str, re.Pattern]):
        """
        Initialize the Regex filter.

        This constructor sets up the necessary structures for extracting and storing
        text content from each page of a PDF. It prepares the filter to capture
        text-related events during the PDF processing pipeline, allowing for text
        extraction based on the processed content streams.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[TextEvent]] = {}  # type: ignore[annotation-unchecked]
        self.__pattern = re.compile(pattern) if isinstance(pattern, str) else pattern
        self.__text_per_page: typing.Dict[int, str] = {}  # type: ignore[annotation-unchecked]
        self.__rectangles_per_page: typing.Dict[int, typing.List[RectangleType]] = {}

    #
    # PRIVATE
    #

    @staticmethod
    def __indo_european_reading_order(e: TextEvent) -> int:
        y_upside_down: int = int(PageSize.A4_PORTRAIT[1] - e.get_y())
        return int(y_upside_down * PageSize.A4_PORTRAIT[1] + e.get_x())

    @staticmethod
    def __split_event_into_rectangles(e: TextEvent) -> typing.List[RectangleType]:
        out: typing.List[RectangleType] = []
        x: float = e.get_x()
        y: float = e.get_y()
        w: float = e.get_width()
        h: float = e.get_height()
        for c in e.get_text():
            cw: float = e.get_font().get_width(text=c)
            out += [(x, y, cw, h)]
            # move to the next x
            x += cw

        # return
        return out

    #
    # PUBLIC
    #

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        return self.__rectangles_per_page

    def process(self, event: Event):
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        if not isinstance(event, TextEvent):
            return

        if len(event.get_text().strip()) == 0:
            return

        # append TextEvent
        page_nr: int = event.get_page_nr()
        self.__events_per_page[page_nr] = self.__events_per_page.get(page_nr, []) + [
            event
        ]

        # sort
        self.__events_per_page[page_nr] = sorted(
            self.__events_per_page[page_nr],
            key=Regex.__indo_european_reading_order,
        )

        # split the TextEvent into RectangleType objects
        # and keep those in sync with the characters
        # this is important to match the regex indices to the RectangleType objects
        char_rectangles: typing.List[typing.Optional[RectangleType]] = []
        text: str = ""
        for evt in self.__events_per_page[page_nr]:

            # IF we do not yet have any text (and thus rectangles)
            # THEN simply add the new text (and rectangles)
            rs: typing.List[RectangleType] = Regex.__split_event_into_rectangles(evt)
            if len(char_rectangles) == 0:
                char_rectangles += rs
                text += evt.get_text()
                continue

            # IF our previous character was a space or newline
            # THEN  we do not attempt to add in another space or newline
            #       we do not compare x-gap or y-gap
            if char_rectangles[-1] is None:
                char_rectangles += rs
                text += evt.get_text()
                continue

            # IF the y-gap is too large
            # THEN add a newline (and None to the char_rectangles)
            next_y: float = rs[0][1]  # typing: ignore[index]
            next_height: float = rs[0][3]  # typing: ignore[index]
            prev_y: float = char_rectangles[-1][1]  # typing: ignore[index]
            if abs(prev_y - next_y) > next_height // 2:
                char_rectangles += [None]
                text += "\n"
                char_rectangles += rs
                text += evt.get_text()
                continue

            # IF the x-gap is too large
            # THEN add a space (and None to the char_rectangles)
            next_left: float = rs[0][0]  # typing: ignore[index]
            next_width: float = rs[0][2]  # typing: ignore[index]
            prev_right: float = (
                char_rectangles[-1][0] + char_rectangles[-1][2]
            )  # typing: ignore[index]
            if abs(prev_right - next_left) > (0.250 * next_width / len(evt.get_text())):
                char_rectangles += [None]
                text += " "
                char_rectangles += rs
                text += evt.get_text()
                continue

            # default (append)
            char_rectangles += rs
            text += evt.get_text()

        # now apply the regex
        self.__rectangles_per_page[page_nr] = []
        for match in self.__pattern.finditer(text):

            # find its matching rectangles
            match_rectangles: typing.List[RectangleType] = []
            for r in char_rectangles[match.start() : match.end()]:

                # IF the rectangle is None
                # THEN skip
                if r is None:
                    continue

                # IF we don't have anything to merge with (yet)
                # THEN simply copy the (char) rectangle
                if len(match_rectangles) == 0:
                    match_rectangles += [r]
                    continue

                # IF the y-gap is too large
                # THEN don't merge rectangles
                next_y: float = r[1]  # type: ignore [no-redef]
                next_height: float = r[3]  # type: ignore [no-redef]
                prev_y: float = match_rectangles[-1][1]  # type: ignore [no-redef]
                if abs(prev_y - next_y) > next_height // 2:
                    match_rectangles += [r]
                    continue

                # default, merge
                next_right: float = r[0] + r[2]
                match_rectangles[-1] = (
                    match_rectangles[-1][0],
                    match_rectangles[-1][1],
                    (next_right - match_rectangles[-1][0]),
                    match_rectangles[-1][3],
                )

            # append
            self.__rectangles_per_page[page_nr] += match_rectangles
