#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A layout element that represents a single day in a calendar view.

This class renders a vertical timeline from a start hour to an end hour,
divided into 30-minute slots. Events can be pushed into the view and will
be displayed at their scheduled times. The DayView supports styling via
background color, borders, padding, and font size.
"""

import collections
import datetime
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hex_color import HexColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.layout_element.text.self_truncating_heterogeneous_paragraph import (
    SelfTruncatingHeterogeneousParagraph,
)
from borb.pdf.page import Page

DayViewEventType = collections.namedtuple(
    "DayViewEventType", ["color", "description", "from_hour", "title", "until_hour"]
)


class DayView(LayoutElement):
    """
    A layout element that represents a single day in a calendar view.

    This class renders a vertical timeline from a start hour to an end hour,
    divided into 30-minute slots. Events can be pushed into the view and will
    be displayed at their scheduled times. The DayView supports styling via
    background color, borders, padding, and font size.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.Optional[typing.List[int]] = None,
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_size: int = 12,
        from_hour: typing.Optional[datetime.datetime] = None,
        gutter_width: int = 6,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        item_height: int = 32,
        lane_width: int = 64,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        until_hour: typing.Optional[datetime.datetime] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a DayView layout element representing a single day in a calendar.

        The DayView renders a vertical timeline from `from_hour` to `until_hour`,
        divided into 30-minute slots, with optional styling such as background color,
        borders, padding, and font size. This constructor also allows configuration
        of the visual layout of event lanes and spacing.

        :param background_color: Background color of the DayView.
        :param border_color: Color of the borders around the DayView.
        :param border_dash_pattern: Optional dash pattern for borders.
        :param border_dash_phase: Phase offset for dashed borders.
        :param border_width_bottom: Width of the bottom border.
        :param border_width_left: Width of the left border.
        :param border_width_right: Width of the right border.
        :param border_width_top: Width of the top border.
        :param font_size: Base font size for text in the DayView.
        :param from_hour: The starting hour of the day view. Defaults to 9:00 AM today.
        :param gutter_width: Width of the gutter separating time and event columns.
        :param horizontal_alignment: Horizontal alignment of the DayView in the layout.
        :param item_height: Height of each time slot row.
        :param lane_width: Width of each event lane column.
        :param margin_bottom: Bottom margin of the DayView.
        :param margin_left: Left margin of the DayView.
        :param margin_right: Right margin of the DayView.
        :param margin_top: Top margin of the DayView.
        :param padding_bottom: Bottom padding inside the DayView.
        :param padding_left: Left padding inside the DayView.
        :param padding_right: Right padding inside the DayView.
        :param padding_top: Top padding inside the DayView.
        :param until_hour: The ending hour of the day view. Defaults to 5:00 PM today.
        :param vertical_alignment: Vertical alignment of the DayView in the layout.
        """
        # calculate from_hour
        now: datetime.datetime = datetime.datetime.now()
        self.__from_hour = from_hour or datetime.datetime(
            year=now.year, month=now.month, day=now.day, hour=9, minute=0, second=0
        )

        # calculate until_hour
        self.__until_hour = until_hour or datetime.datetime(
            year=now.year, month=now.month, day=now.day, hour=18, minute=0, second=0
        )
        assert self.__until_hour.year == self.__from_hour.year
        assert self.__until_hour.month == self.__from_hour.month
        assert self.__until_hour.day == self.__from_hour.day
        assert self.__until_hour > self.__from_hour

        # store events
        self.__events: typing.List[DayViewEventType] = []
        self.__grid: typing.List[typing.List[int]] = []

        # call to super
        self.__font_size: int = font_size
        self.__gutter_width: int = gutter_width
        self.__item_height: int = item_height
        self.__lane_width: int = lane_width
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        # calculate number_of_lines
        number_of_lines: int = len(self.__grid)

        # calculate width
        w: int = 0
        w += max(
            [
                Paragraph(
                    text=f"{i:02d}:00",
                    font_size=self.__font_size,
                    padding_right=self.__font_size // 2,
                    padding_left=self.__font_size // 2,
                    padding_top=self.__font_size // 2,
                    padding_bottom=self.__font_size // 2,
                ).get_size(available_space=(2**64, 2**64))[0]
                for i in range(self.__from_hour.hour, self.__until_hour.hour + 1)
            ]
        )
        w += number_of_lines * self.__lane_width

        # calculate height
        # fmt: off
        h: int = ((self.__until_hour - self.__from_hour).seconds // 1800) * self.__item_height
        # fmt: on

        # return
        return w, h

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (x, y, width, height).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        # determine width/height
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # paint background and border(s)
        self._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # calculate the width of the hour label(s)
        hour_label_width: int = max(
            [
                Paragraph(
                    text=f"{i:02d}:00",
                    font_size=self.__font_size,
                    padding_right=self.__font_size // 2,
                    padding_left=self.__font_size // 2,
                    padding_top=self.__font_size // 2,
                    padding_bottom=self.__font_size // 2,
                ).get_size(available_space=(2**64, 2**64))[0]
                for i in range(self.__from_hour.hour, self.__until_hour.hour + 1)
            ]
        )

        # render the (second) background
        Shape(
            coordinates=[  # type: ignore[arg-type]
                (0, 0),
                (0, h),
                (w - hour_label_width, h),
                (w - hour_label_width, 0),
                (0, 0),
            ],
            stroke_color=None,
            fill_color=HexColor("#E0E0E0"),
        ).paint(
            available_space=(
                background_x + hour_label_width,
                background_y,
                w - hour_label_width,
                h,
            ),
            page=page,
        )

        # render lines for the hours
        # fmt: off
        number_of_half_hours: int = (self.__until_hour - self.__from_hour).seconds // 1800
        for i in range(0, number_of_half_hours + 1):
            Shape(
                coordinates=[(0, 0), (w, 0)],   # type: ignore[arg-type]
                fill_color=None,
                stroke_color=X11Color.LIGHT_GRAY,
                dash_pattern=[] if i % 2 == 0 else [3, 3],
            ).paint(
                available_space=(
                    background_x,
                    background_y + i * self.__item_height,
                    w,
                    0,
                ),
                page=page,
            )
        # fmt: on

        # render the labels for the hours
        top: int = background_y + h
        number_of_hours: int = number_of_half_hours // 2
        for i in range(0, number_of_hours):
            Paragraph(
                f"{self.__from_hour.hour+i:02d}:00",
                horizontal_alignment=LayoutElement.HorizontalAlignment.RIGHT,
                text_alignment=LayoutElement.TextAlignment.RIGHT,
                font_size=self.__font_size,
                padding_right=self.__font_size // 2,
                padding_left=self.__font_size // 2,
                padding_top=self.__font_size // 2,
                padding_bottom=self.__font_size // 2,
            ).paint(
                available_space=(
                    background_x,
                    top - self.__item_height - i * self.__item_height * 2,
                    hour_label_width,
                    self.__item_height,
                ),
                page=page,
            )

        # render events
        for lane_index, lane in enumerate(self.__grid):

            lane_x: int = (
                background_x + hour_label_width + self.__lane_width * lane_index
            )

            # loop over everything in the swimlane
            i: int = 0  # type: ignore[no-redef]
            while i < len(lane):

                # IF the swimlane does not contain anything at the given time
                # THEN continue with the next half hour
                if lane[i] == -1:
                    i += 1
                    continue

                event: DayViewEventType = self.__events[lane[i]]
                event_top: int = background_y + h - i * self.__item_height
                event_bottom: int = (
                    event_top
                    - ((event.until_hour - event.from_hour).seconds // 1800)
                    * self.__item_height
                )
                event_height: int = event_top - event_bottom

                # draw background
                Shape(
                    coordinates=[  # type: ignore[arg-type]
                        (0, 0),
                        (0, event_height),
                        (self.__lane_width, event_height),
                        (self.__lane_width, 0),
                        (0, 0),
                    ],
                    stroke_color=None,
                    fill_color=event.color,
                ).paint(
                    available_space=(
                        lane_x,
                        event_bottom,
                        self.__lane_width,
                        event_height,
                    ),
                    page=page,
                )

                # draw gutter
                Shape(
                    coordinates=[  # type: ignore[arg-type]
                        (0, 0),
                        (0, event_height),
                        (self.__lane_width // 10, event_height),
                        (self.__lane_width // 10, 0),
                        (0, 0),
                    ],
                    stroke_color=None,
                    fill_color=event.color.darker().darker(),
                ).paint(
                    available_space=(
                        lane_x,
                        event_bottom,
                        self.__lane_width // 10,
                        event_height,
                    ),
                    page=page,
                )

                # draw paragraph
                SelfTruncatingHeterogeneousParagraph(
                    chunks=[
                        Chunk(
                            event.title,
                            font_size=self.__font_size,
                            font="Helvetica-Bold",
                        ),
                        Chunk(": ", font_size=self.__font_size),
                        Chunk(
                            event.description,
                            font_size=self.__font_size,
                        ),
                    ],
                    padding_left=self.__font_size // 2,
                    padding_right=self.__font_size // 2,
                    padding_top=self.__font_size // 2,
                    padding_bottom=self.__font_size // 2,
                    max_height=event_height,
                ).paint(
                    available_space=(
                        lane_x + self.__lane_width // 10,
                        event_bottom,
                        self.__lane_width - self.__lane_width // 10,
                        event_height,
                    ),
                    page=page,
                )

                # skip to the next event (or empty slot) in the lane
                i = max([x for x in range(0, len(lane)) if lane[x] == lane[i]]) + 1

    def push_event(
        self,
        from_hour: datetime.datetime,
        until_hour: datetime.datetime,
        color: Color = X11Color.SLATE_GRAY,
        description: str = "",
        title: str = "",
    ) -> "DayView":
        """
        Add an event to the current DayView.

        The event will be displayed between the specified start and end times.
        Both from_hour and until_hour must fall within the DayView’s configured
        range and align to 30-minute intervals. If an event overlaps an existing one,
        a ValueError may be raised depending on implementation.

        :param from_hour: The start time of the event.
        :param until_hour: The end time of the event.
        :param color: The background color used to display the event. Defaults to X11Color.SLATE_GRAY.
        :param description: An optional longer description of the event. Defaults to an empty string.
        :param title: A short title or label to display for the event. Defaults to an empty string.
        :returns: The current DayView instance, allowing method chaining.
        :raises ValueError: If the event times are invalid (e.g., outside the view range,
                            not aligned to 30-minute slots, or overlapping another event).
        """
        # append event
        self.__events += [
            DayViewEventType(
                color=color,
                description=description,
                from_hour=from_hour,
                title=title,
                until_hour=until_hour,
            )
        ]

        # calculate a grid
        # fmt: off
        number_of_half_hours: int = (self.__until_hour - self.__from_hour).seconds // 1800
        self.__grid = [[-1 for _ in range(0, number_of_half_hours)]]
        for i, e in enumerate(self.__events):
            from_index: int = (e.from_hour - self.__from_hour).seconds // 1800
            to_index: int = (e.until_hour - self.__from_hour).seconds // 1800
            lane_with_free_slots: typing.Optional[int] = next(iter([i for i in range(0, len(self.__grid)) if all([x == -1 for x in self.__grid[i][from_index:to_index]])]), None)
            if lane_with_free_slots is None:
                self.__grid += [[-1 for _ in range(0, number_of_half_hours)]]
                lane_with_free_slots = -1
            for j in range(from_index, to_index):
                self.__grid[lane_with_free_slots][j] = i
        # fmt: on

        # return
        return self
