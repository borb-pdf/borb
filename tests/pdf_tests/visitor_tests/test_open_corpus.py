import pathlib
import sys
import time
import typing
import unittest

from borb.pdf import PDF, Document


class TestOpenCorpus(unittest.TestCase):

    # Path to the directory containing a collection of PDF documents used for testing.
    #
    # Users must adjust this path to match the location of the PDF corpus on their system
    # to run the tests successfully. A large collection of PDF documents is available
    # on the author's GitHub repository, which can be cloned or downloaded to use as the
    # test corpus.
    #
    # Ensure that the directory specified by this path exists and contains the necessary
    # PDF files before running the tests.
    CORPUS_DIRECTORY: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus/pdf"
    )

    #@unittest.skip
    def test_open_corpus(self):
        positive: typing.List[pathlib.Path] = []
        positive_timing: typing.List[float] = []
        negative: typing.List[pathlib.Path] = []
        negative_timing: typing.List[float] = []
        reasons_for_failure: typing.Dict[str, int] = {}
        M: typing.List[pathlib.Path] = [
            x
            for x in TestOpenCorpus.CORPUS_DIRECTORY.iterdir()
            if x.name.endswith(".pdf")
        ]
        M = sorted(M, key=lambda x: x.name)
        N: int = len(M)
        for i, pdf_file in enumerate(M):
            if not pdf_file.name.endswith(".pdf"):
                continue

            # KNOWN ERRORS
            # fmt: off
            if pdf_file.name in ["0605.pdf"]:
                continue
            # fmt: on

            # debug
            print(
                f"count: {i}, total: {N}, count-as-%: {round(i / N, 2)}, pos: {len(positive)}, pos-as-%:{round(len(positive) / i, 2) if i != 0 else 0}, now-reading: {pdf_file.name}"
            )

            # try opening
            before: float = time.time()
            try:
                doc: Document = PDF.read(where_from=pdf_file)
                doc.get_page(0)
                positive_timing += [time.time() - before]
                positive += [pdf_file]
            except Exception as e:
                print(f"Unable to read {pdf_file}")
                reasons_for_failure[str(e)] = reasons_for_failure.get(str(e), 0) + 1
                negative_timing += [time.time() - before]
                negative += [pdf_file]

        # debug
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

        # print all reasons
        if len(reasons_for_failure) > 0:
            print("\treasons:")
            for k, v in reasons_for_failure.items():
                print(f"\t\t- {k}: {round(v/sum(reasons_for_failure.values()), 2)}")

        # print all negative
        if len(negative) > 0:
            print("\tfiles:")
            for pdf_file in negative:
                print(f"\t\t- {pdf_file}")

    # @unittest.skip
    def test_open_single_file_from_corpus(self):
        d = PDF.read(where_from=TestOpenCorpus.CORPUS_DIRECTORY / "0000.pdf")
        d.get_page(0)
