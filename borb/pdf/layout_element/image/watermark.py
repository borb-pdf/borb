#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a watermark to be applied to PDF documents, inheriting from the Image class.

This class is designed to handle the addition of watermarks (typically semi-transparent images or text) to PDF files.
It extends the functionality of the `Image` class, allowing for customization of watermark properties such as opacity,
size, and position.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class Watermark(LayoutElement):
    """
    Represents a watermark to be applied to PDF documents, inheriting from the Image class.

    This class is designed to handle the addition of watermarks (typically semi-transparent images or text) to PDF files.
    It extends the functionality of the `Image` class, allowing for customization of watermark properties such as opacity,
    size, and position.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        angle_in_degrees: int = 45,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.Optional[typing.List[int]] = None,
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_color: Color = X11Color.RED,
        font_size: int = 24,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        transparency: float = 0.6,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a full-page watermark to be applied on the PDF.

        This constructor sets up the watermark text, its appearance, and its positioning
        across the entire page. You can customize the angle, font size, colors, margins,
        padding, and transparency to achieve the desired visual effect. The watermark
        will overlay the content of the PDF, making it suitable for branding or marking
        documents as confidential.

        :param text:                   The text to display as the watermark.
        :param angle_in_degrees:      The angle at which the watermark text is displayed (default is 45).
        :param background_color:       Optional background color for the watermark.
        :param border_color:           Optional border color for the watermark.
        :param border_dash_pattern:    Dash pattern used for the border lines of the watermark.
        :param border_dash_phase:      Phase offset for the dash pattern in the borders.
        :param border_width_bottom:    Width of the bottom border of the watermark.
        :param border_width_left:      Width of the left border of the watermark.
        :param border_width_right:     Width of the right border of the watermark.
        :param border_width_top:       Width of the top border of the watermark.
        :param font_color:             Color of the watermark text (default is RED).
        :param font_size:              Size of the watermark text (default is 24).
        :param horizontal_alignment:    Horizontal alignment of the watermark (default is LEFT).
        :param margin_bottom:          Space between the watermark and the element below it.
        :param margin_left:            Space between the watermark and the left page margin.
        :param margin_right:           Space between the watermark and the right page margin.
        :param margin_top:             Space between the watermark and the element above it.
        :param padding_bottom:         Padding inside the watermark at the bottom.
        :param padding_left:           Padding inside the watermark on the left side.
        :param padding_right:          Padding inside the watermark on the right side.
        :param padding_top:            Padding inside the watermark at the top.
        :param transparency:           Transparency level of the watermark (default is 0.6).
        :param vertical_alignment:      Vertical alignment of the watermark (default is TOP).
        """
        self.__angle_in_degrees: int = angle_in_degrees
        self.__font_color: Color = font_color
        self.__font_size: int = font_size
        self.__text: str = text
        self.__transparency: float = transparency

        # call super
        super().__init__()

    #
    # PRIVATE
    #

    @staticmethod
    def __get_pil_image(
        text: str,
        angle_in_degrees: int = 0,
        font_color: Color = X11Color.BLACK,
        font_size: int = 20,
        height: int = 100,
        transparency: float = 0.6,
        width: int = 100,
    ):
        from PIL import Image, ImageDraw, ImageFont  # type: ignore[import-not-found]

        # Create a fully transparent image (RGBA)
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Prepare drawing context
        draw = ImageDraw.Draw(img)

        # Load a font (fallback-safe)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", size=font_size)
        except IOError:
            font = ImageFont.load_default()

        # Measure text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Center the text
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw black text (fully opaque)
        rgb_font_color: RGBColor = font_color.to_rgb_color()
        draw.text(
            (x, y),
            text,
            fill=(
                rgb_font_color.get_red(),
                rgb_font_color.get_green(),
                rgb_font_color.get_blue(),
                255 - int(255 * transparency),
            ),
            font=font,
        )

        # Rotate around center, preserve alpha
        if angle_in_degrees != 0:
            img = img.rotate(
                angle=angle_in_degrees,
                resample=Image.BICUBIC,
                expand=False,
                center=(width // 2, height // 2),
            )

        # return
        return img

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
        return 0, 0

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
        # useful constant(s)
        x: int = page.get_size()[0] // 10
        y: int = page.get_size()[1] // 10
        w: int = page.get_size()[0] - 2 * (page.get_size()[0] // 10)
        h: int = page.get_size()[1] - 2 * (page.get_size()[1] // 10)

        # generate the image to draw
        from borb.pdf.layout_element.image.image import Image

        img_to_draw = Image(
            bytes_path_pil_image_or_url=self.__get_pil_image(
                text=self.__text,
                angle_in_degrees=self.__angle_in_degrees,
                font_color=self.__font_color,
                font_size=self.__font_size,
                height=min(w, h),
                width=min(w, h),
            ),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            size=(min(w, h), min(w, h)),
        )

        # draw
        img_to_draw.paint(
            available_space=(x, y, w, h),
            page=page,
        )

        # hack
        self._LayoutElement__previous_paint_box = (0, 0, 0, 0)
