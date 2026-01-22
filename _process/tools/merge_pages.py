#!/usr/bin/env python3
"""
Merge specific pages from single-page PDFs into a new PDF file.

Usage:
    python merge_pages.py <output.pdf> <page1.pdf> <page2.pdf> ...
    python merge_pages.py <output.pdf> --pages-dir DIR --range START-END

Examples:
    python merge_pages.py section.pdf page-0001.pdf page-0002.pdf page-0003.pdf
    python merge_pages.py section.pdf --pages-dir tmp/pages --range 1-5
    python merge_pages.py section.pdf --pages-dir tmp/pages --range 10-25
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def merge_pages(output_path: str, page_files: list[str]) -> str:
    """
    Merge multiple single-page PDF files into one PDF.

    Args:
        output_path: Path for the output PDF file
        page_files: List of paths to single-page PDF files

    Returns:
        Path to the output file

    Raises:
        FileNotFoundError: If any input file doesn't exist
        ValueError: If no page files provided
    """
    if not page_files:
        raise ValueError("No page files provided")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = PyPDF2.PdfWriter()

    for page_file in page_files:
        page_path = Path(page_file)
        if not page_path.exists():
            raise FileNotFoundError(f"Page file not found: {page_path}")

        with open(page_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            writer.add_page(reader.pages[0])

    with open(output_path, 'wb') as out:
        writer.write(out)

    return str(output_path)


def get_pages_from_dir(pages_dir: str, start: int, end: int, stem_pattern: str = None) -> list[str]:
    """
    Get list of page files from a directory for a given range.

    Args:
        pages_dir: Directory containing single-page PDFs
        start: Start page number (1-indexed)
        end: End page number (1-indexed, inclusive)
        stem_pattern: Optional pattern to match file stems (e.g., "10-K-2022")

    Returns:
        List of page file paths in order
    """
    pages_dir = Path(pages_dir)
    if not pages_dir.exists():
        raise FileNotFoundError(f"Pages directory not found: {pages_dir}")

    page_files = []
    for page_num in range(start, end + 1):
        if stem_pattern:
            pattern = f"{stem_pattern}-page-{page_num:04d}.pdf"
        else:
            pattern = f"*-page-{page_num:04d}.pdf"

        matches = list(pages_dir.glob(pattern))
        if not matches:
            raise FileNotFoundError(f"Page file not found for page {page_num} with pattern {pattern}")
        page_files.append(str(matches[0]))

    return page_files


def parse_range(range_str: str) -> tuple[int, int]:
    """Parse a range string like '1-5' into (start, end) tuple."""
    match = re.match(r'^(\d+)-(\d+)$', range_str)
    if not match:
        raise ValueError(f"Invalid range format: {range_str}. Expected format: START-END (e.g., 1-5)")
    return int(match.group(1)), int(match.group(2))


def main():
    parser = argparse.ArgumentParser(
        description='Merge specific pages from single-page PDFs into a new PDF file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('output', help='Path for the output PDF file')
    parser.add_argument('pages', nargs='*', help='Paths to single-page PDF files')
    parser.add_argument('--pages-dir', '-d',
                        help='Directory containing single-page PDFs')
    parser.add_argument('--range', '-r', dest='page_range',
                        help='Page range to merge (e.g., 1-5)')
    parser.add_argument('--stem', '-s',
                        help='File stem pattern to match (e.g., "10-K-2022")')

    args = parser.parse_args()

    try:
        if args.pages_dir and args.page_range:
            start, end = parse_range(args.page_range)
            page_files = get_pages_from_dir(args.pages_dir, start, end, args.stem)
        elif args.pages:
            page_files = args.pages
        else:
            parser.error("Provide either page files or --pages-dir with --range")

        output_path = merge_pages(args.output, page_files)
        print(f"Merged {len(page_files)} pages into: {output_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDFs: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
