import argparse
import json
import time
import typing

import tqdm # type: ignore[import-not-found, import-untyped]

from borb.pdf import PDF

TEXT: str = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Pellentesque sagittis dignissim fermentum. 
Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
In aliquet, ipsum in tincidunt lacinia, leo elit faucibus ipsum, et volutpat justo odio id orci. 
Mauris finibus non justo et elementum. 
Nullam consequat vehicula maximus. 
Integer in quam id urna elementum dictum fringilla et orci. 
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
Sed at ante eu turpis dignissim rutrum.
"""


def median(xs: typing.List[float]) -> float:
    sorted_xs: typing.List[float] = sorted(xs)
    middle: int = len(sorted_xs) // 2
    if len(sorted_xs) % 2 == 1:
        return sorted_xs[middle]
    else:
        return (sorted_xs[middle - 1] + sorted_xs[middle]) / 2


def main():

    # process command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    # do the work
    layout_times = []
    import_times = []
    write_times = []
    for _ in tqdm.tqdm(range(100), desc="Benchmarking"):

        # importing
        delta: float = time.time()
        from borb.pdf import Document
        from borb.pdf import Page
        from borb.pdf import SingleColumnLayout
        from borb.pdf import Paragraph

        delta = time.time() - delta
        import_times.append(delta)

        # adding text
        delta = time.time()
        doc: Document = Document()
        page: Page = Page()
        doc.append_page(page)
        layout: SingleColumnLayout = SingleColumnLayout(page)
        for _ in range(64):
            layout.append_layout_element(Paragraph(TEXT))
        delta = time.time() - delta
        layout_times.append(delta)

        # persisting
        delta = time.time()
        PDF.write(what=doc, where_to="output.pdf")
        delta = time.time() - delta
        write_times.append(delta)

    with open(args.output, "w", encoding="utf-8") as output:
        json.dump(
            {
                "import": {
                    "min": min(import_times),
                    "max": max(import_times),
                    "avg": sum(import_times) / len(import_times),
                    "median": median(import_times),
                },
                "layout": {
                    "min": min(layout_times),
                    "max": max(layout_times),
                    "avg": sum(layout_times) / len(layout_times),
                    "median": median(layout_times),
                },
                "write": {
                    "min": min(write_times),
                    "max": max(write_times),
                    "avg": sum(write_times) / len(write_times),
                    "median": median(write_times),
                },
            },
            output,
            indent=4,
        )


if __name__ == "__main__":
    main()
