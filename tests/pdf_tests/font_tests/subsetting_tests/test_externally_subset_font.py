import pathlib
import unittest

from fontTools import subset  # type: ignore[import-not-found,import-untyped]

from borb.pdf import (
    Document,
    Page,
    Font,
    TrueTypeFont,
    SingleColumnLayout,
    PageLayout,
    Paragraph,
    PDF,
)
from borb.pdf.primitives import name, stream


class TestExternallySubsetFonts(unittest.TestCase):

    def _create_subset_font(self):

        # Create options object
        options = subset.Options()
        options.retain_gids = True
        options.notdef_glyph = True
        options.notdef_outline = True
        options.recalc_bounds = True
        options.recalc_timestamp = False
        options.canonical_order = True

        # Example: keep only ASCII characters
        options.text = "Hello World!"

        # Load font
        # fmt: off
        font_file_in: pathlib.Path = pathlib.Path(__file__).parent / "BitcountGridDouble-Regular.ttf"
        font = subset.load_font(font_file_in, options)
        # fmt: on

        # Create subsetter
        subsetter = subset.Subsetter(options)

        # Populate subsetter with desired glyphs
        subsetter.populate(text=options.text)

        # Subset the font
        subsetter.subset(font)

        # Save output
        # fmt: off
        font_file_out: pathlib.Path = pathlib.Path(__file__).parent / "BitcountGridDouble-Regular-subset.ttf"
        subset.save_font(font, font_file_out, options)
        # fmt: on

    def _cmap(self) -> stream:
        cmap_str: str = ""
        cmap_str += "/CIDInit /ProcSet findresource begin\n"
        cmap_str += "12 dict begin\n"
        cmap_str += "begincmap\n"
        cmap_str += "/CIDSystemInfo\n"
        cmap_str += "<< /Registry (Adobe)\n"
        cmap_str += "/Ordering (UCS)\n"
        cmap_str += "/Supplement 0\n"
        cmap_str += ">> def\n"
        cmap_str += "/CMapName /Adobe-Identity-UCS def\n"
        cmap_str += "/CMapType 2 def\n"
        cmap_str += "1 begincodespacerange\n"
        cmap_str += "<00> <FF>\n"
        cmap_str += "endcodespacerange\n"
        cmap_str += "9 beginbfchar\n"
        cmap_str += "<20> <0020>  % space\n"
        cmap_str += "<21> <0021>  % !\n"
        cmap_str += "<48> <0048>  % H\n"
        cmap_str += "<57> <0057>  % W\n"
        cmap_str += "<64> <0064>  % d\n"
        cmap_str += "<65> <0065>  % e\n"
        cmap_str += "<6C> <006C>  % l\n"
        cmap_str += "<6F> <006F>  % o\n"
        cmap_str += "<72> <0072>  % r\n"
        cmap_str += "endbfchar\n"
        cmap_str += "endcmap\n"
        cmap_str += "CMapName currentdict /CMap defineresource pop\n"
        cmap_str += "end\n"
        cmap_str += "end"

        # convert to stream object
        import zlib

        bts: bytes = (cmap_str).encode("latin1")
        to_unicode_stream = stream()
        to_unicode_stream[name("Bytes")] = zlib.compress(bts, 9)
        to_unicode_stream[name("DecodedBytes")] = bts
        to_unicode_stream[name("Filter")] = name("FlateDecode")
        to_unicode_stream[name("Length")] = len(to_unicode_stream[name("Bytes")])

        # return
        from borb.pdf.font.cmap import CMap

        return CMap(to_unicode_stream)

    def test_externally_subset_fonts(self):

        # create subset font
        self._create_subset_font()

        # new Document
        doc = Document()

        # new Page
        page = Page()
        doc.append_page(page)

        # new Font
        # fmt: off
        font_file_in: pathlib.Path = pathlib.Path(__file__).parent / "BitcountGridDouble-Regular-subset.ttf"
        subset_font: Font = TrueTypeFont._TrueTypeFont__type_0_font_from_file(font_file_in)
        # fmt: on

        # new Paragraph
        layout: PageLayout = SingleColumnLayout(page)
        layout.append_layout_element(Paragraph(text="Hello World!", font=subset_font))

        # store
        PDF.write(what=doc, where_to="assets/test_externally_subset_fonts.pdf")
