import unittest

from borb.pdf import (
    Paragraph,
    X11Color,
    Page,
    Document,
    PDF,
    LayoutElement,
    Chunk,
    Standard14Fonts,
    HeterogeneousParagraph,
    HomogeneousParagraph,
    ProgressBar,
    ProgressSquare,
    TextArea,
    DropDownList,
    CountryDropDownList,
    GenderDropDownList,
    Button,
    JavascriptButton,
    OrderedList,
)


class TestRoundedBorders(unittest.TestCase):

    @staticmethod
    def __create_pdf_with_single_element(e: LayoutElement) -> Document:
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # set layout properties
        e._LayoutElement__border_color = X11Color.DARK_GRAY  # type: ignore[attr-defined]
        e._LayoutElement__background_color = X11Color.LIGHT_GRAY.lighter().lighter()  # type: ignore[attr-defined]
        try:
            e._LayoutElement__font_color = X11Color.DARK_GRAY  # type: ignore[attr-defined]
        except:
            pass
        e._LayoutElement__border_radius_top_left = 15  # type: ignore[attr-defined]
        e._LayoutElement__border_radius_top_right = 15  # type: ignore[attr-defined]
        e._LayoutElement__border_radius_bottom_right = 0  # type: ignore[attr-defined]
        e._LayoutElement__border_radius_bottom_left = 15  # type: ignore[attr-defined]
        e._LayoutElement__border_width_top = 1  # type: ignore[attr-defined]
        e._LayoutElement__border_width_right = 1  # type: ignore[attr-defined]
        e._LayoutElement__border_width_bottom = 1  # type: ignore[attr-defined]
        e._LayoutElement__border_width_left = 1  # type: ignore[attr-defined]
        e._LayoutElement__padding_top = 5  # type: ignore[attr-defined]
        e._LayoutElement__padding_right = 5  # type: ignore[attr-defined]
        e._LayoutElement__padding_bottom = 5  # type: ignore[attr-defined]
        e._LayoutElement__padding_left = 5  # type: ignore[attr-defined]

        # paint
        e.paint(available_space=(x, y, w, h), page=p)

        # return
        return d

    def test_button_rounded_corners(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            Button(
                text="Lorem",
            )
        )
        PDF.write(what=doc, where_to="assets/test_button_rounded_corners.pdf")

    def test_country_dropdown_list_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            CountryDropDownList(
                padding_top=5,
                padding_bottom=5,
                padding_right=5,
                padding_left=5,
            )
        )
        PDF.write(
            what=doc, where_to="assets/test_country_dropdown_list_rounded_borders.pdf"
        )

    def test_dropdown_list_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            DropDownList(
                options=["Lorem", "Ipsum", "Dolor", "Sit", "Amet"],
                padding_top=5,
                padding_bottom=5,
                padding_right=5,
                padding_left=5,
            )
        )
        PDF.write(what=doc, where_to="assets/test_dropdown_list_rounded_borders.pdf")

    def test_gender_dropdown_list_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            GenderDropDownList(
                padding_top=5,
                padding_bottom=5,
                padding_right=5,
                padding_left=5,
            )
        )
        PDF.write(
            what=doc, where_to="assets/test_gender_dropdown_list_rounded_borders.pdf"
        )

    def test_heterogeneous_paragraph_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            HeterogeneousParagraph(
                chunks=[
                    Chunk(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                    ),
                    Chunk("Ut enim", font=Standard14Fonts.get("Helvetica-Bold")),
                    Chunk(
                        "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                    ),
                ],
                text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
            )
        )
        PDF.write(
            what=doc, where_to="assets/test_heterogeneous_paragraph_rounded_borders.pdf"
        )

    def test_homogeneous_paragraph_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            HomogeneousParagraph(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                "Ut enim"
                "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            )
        )
        PDF.write(
            what=doc, where_to="assets/test_homogeneous_paragraph_rounded_borders.pdf"
        )

    def test_javascript_button_rounded_corners(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            JavascriptButton(
                text="Lorem",
                javascript="alert('Hello World!')",
            )
        )
        PDF.write(
            what=doc, where_to="assets/test_javascript_button_rounded_corners.pdf"
        )

    def test_ordered_list_rounded_corners(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            OrderedList()
            .append_layout_element(Chunk(text="Lorem"))
            .append_layout_element(Chunk(text="Ipsum"))
            .append_layout_element(Chunk(text="Dolor"))
        )
        PDF.write(what=doc, where_to="assets/test_ordered_list_rounded_corners.pdf")

    def test_paragraph_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            Paragraph(
                text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            )
        )
        PDF.write(what=doc, where_to="assets/test_paragraph_rounded_borders.pdf")

    def test_progress_bar_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            ProgressBar(value=65, max_value=100, size=(100, 15))
        )
        PDF.write(what=doc, where_to="assets/test_progress_bar_rounded_borders.pdf")

    def test_progress_square_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            ProgressSquare(value=65, max_value=100, width=100)
        )
        PDF.write(what=doc, where_to="assets/test_progress_square_rounded_borders.pdf")

    def test_text_area_rounded_borders(self):
        doc = TestRoundedBorders.__create_pdf_with_single_element(
            TextArea(
                padding_top=5,
                padding_bottom=5,
                padding_right=5,
                padding_left=5,
            )
        )
        PDF.write(what=doc, where_to="assets/test_text_area_rounded_borders.pdf")
