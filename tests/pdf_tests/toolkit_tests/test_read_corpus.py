import pathlib
import re
import time
import typing
import unittest

from borb.pdf import PDF, Document
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_text import GetText
from borb.pdf.toolkit.source.operator.source import Source


class TestReadCorpus(unittest.TestCase):

    # Path to the directory containing a collection of PDF documents used for testing.
    #
    # Users must adjust this path to match the location of the PDF corpus on their system
    # to run the tests successfully. A large collection of PDF documents is available
    # on the author's GitHub repository, which can be cloned or downloaded to use as the
    # test corpus.
    #
    # Ensure that the directory specified by this path exists and contains the necessary
    # PDF files before running the tests.
    FIRST_PAGE_PDF_DIR: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus/first-page-pdf"
    )
    FIRST_PAGE_TXT_DIR: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus/first-page-txt"
    )

    # @unittest.skip
    def test_read_corpus(self):
        positive: typing.List[pathlib.Path] = []
        positive_timing: typing.List[float] = []
        negative: typing.List[pathlib.Path] = []
        negative_timing: typing.List[float] = []
        error_buckets: typing.Dict[int, int] = {x: 0 for x in range(0, 110, 10)}
        all_pdf_files = [
            x
            for x in TestReadCorpus.FIRST_PAGE_PDF_DIR.iterdir()
            if x.name.endswith(".pdf")
        ]
        all_pdf_files = sorted(all_pdf_files, key=lambda x: x.name)
        all_pdf_files = all_pdf_files[0:100]
        N: int = len(all_pdf_files)
        for i, pdf_file in enumerate(all_pdf_files):

            # known errors
            if pdf_file.name in [
                "0025.pdf",
                "0028.pdf",
                "0046.pdf",
                "0051.pdf",
                "0389.pdf",
                "0398.pdf",
            ]:
                continue

            # try opening
            before: float = time.time()
            try:
                d: Document = PDF.read(where_from=pdf_file)
                positive_timing += [time.time() - before]
                positive += [pdf_file]

                # debug
                print(
                    f"count: {i}, total: {N}, count-as-%: {round(i / N, 2)}, pos: {len(positive)}, pos-as-%:{round(len(positive) / i, 2) if i != 0 else 0}, now-reading: {pdf_file.name}"
                )

                # get text
                txt0: str = (
                    Pipeline([Source(), GetText()]).process(d.get_page(0)).get(0, "")
                )
                txt1: str = ""
                with open(
                    TestReadCorpus.FIRST_PAGE_TXT_DIR
                    / (pdf_file.name.replace(".pdf", ".txt"))
                ) as fh:
                    txt1 = fh.read()

                # process text
                txt0_trimmed = re.sub("[^a-zA-Z0-9]+", "", txt0)
                txt1_trimmed = re.sub("[^a-zA-Z0-9]+", "", txt1)

                # process text
                l0 = len(txt0_trimmed)
                l1 = len(txt1_trimmed)

                # update errors
                error: int = 0
                if max(l0, l1) > 0:
                    error = abs(l0 - l1) / max(l0, l1)
                    error = int(error * 100)
                    error_down = error - (error % 10)
                    error_up = min(error_down + 10, 100)
                    if abs(error - error_down) < abs(error - error_up):
                        error = error_down
                    else:
                        error = error_up
                error_buckets[error] += 1

            except Exception as e:
                negative_timing += [time.time() - before]
                negative += [pdf_file]

        # debug
        # fmt: off
        n: int = sum(error_buckets.values())
        if n != 0:
            print("ERROR:")
            for k,v in error_buckets.items():
                print(f"\t{k}: {round(v/n, 2)*100}")
            print('\n')
        # fmt: on

        # fmt: off
        n: int = len(positive) + len(negative)
        print("POSITIVE:")
        print(f"\tcount: {len(positive)}")
        print(f"\t    %: {round(len(positive)/n, 2)}")
        print(f"\t  duration (avg): {round(sum(positive_timing) / len(positive_timing), 2)}")
        print(f"\t           (max): {round(max(positive_timing), 2)}")
        print(f"\t           (min): {round(min(positive_timing), 2)}")
        # fmt: on

        # fmt: off
        print("NEGATIVE:")
        print(f"\tcount: {len(negative)}")
        print(f"\t    %: {round(len(negative)/n, 2)}")
        print(f"\t  duration (avg): {round(sum(negative_timing) / len(negative_timing), 2)}")
        print(f"\t           (max): {round(max(negative_timing), 2)}")
        print(f"\t           (min): {round(min(negative_timing), 2)}")
        # fmt: on

        # print all negative
        if len(negative) > 0:
            print("\tfiles:")
            for pdf_file in negative:
                print(f"\t\t- {pdf_file}")

    @unittest.skipIf(True, "Only used for debugging")
    def test_read_single_pdf(self):

        d: Document = PDF.read(where_from="/home/joris-schellekens/Downloads/68192.pdf")
        print(d.get_number_of_pages())
        print(d.get_page(0))
