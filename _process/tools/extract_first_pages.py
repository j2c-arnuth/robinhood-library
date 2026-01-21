#!/usr/bin/env python3
"""
Extract the first N pages from a PDF file.

Usage:
    python extract_first_pages.py <input.pdf> [--pages N] [--output-dir DIR]

Examples:
    python extract_first_pages.py document.pdf
    python extract_first_pages.py document.pdf --pages 5
    python extract_first_pages.py document.pdf --output-dir /path/to/output
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def extract_first_pages(input_path: str, output_dir: str, num_pages: int = 3) -> str:
    """
    Extract the first N pages from a PDF file.

    Args:
        input_path: Path to the input PDF file
        output_dir: Directory to save the output file
        num_pages: Number of pages to extract (default: 3)

    Returns:
        Path to the output file

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input is not a PDF file
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() != '.pdf':
        raise ValueError(f"Input must be a PDF file, got: {input_path.suffix}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / input_path.name

    with open(input_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        writer = PyPDF2.PdfWriter()

        pages_to_extract = min(num_pages, len(reader.pages))

        for i in range(pages_to_extract):
            writer.add_page(reader.pages[i])

        with open(output_path, 'wb') as out:
            writer.write(out)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Extract the first N pages from a PDF file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('--pages', '-p', type=int, default=3,
                        help='Number of pages to extract (default: 3)')
    parser.add_argument('--output-dir', '-o', default='tmp',
                        help='Output directory (default: tmp)')

    args = parser.parse_args()

    try:
        output_path = extract_first_pages(args.input, args.output_dir, args.pages)
        print(f"Extracted {args.pages} pages to: {output_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
