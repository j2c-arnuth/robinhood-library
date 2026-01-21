#!/usr/bin/env python3
"""
Get file size and token estimate for a PDF file.

Token estimation uses word count × 1.3 as an approximation.

Usage:
    python pdf_stats.py <input.pdf> [--pages N] [--json]

Examples:
    python pdf_stats.py document.pdf
    python pdf_stats.py document.pdf --pages 3
    python pdf_stats.py document.pdf --json
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def get_pdf_stats(input_path: str, num_pages: int = None) -> dict:
    """
    Get file size and token estimate for a PDF file.

    Args:
        input_path: Path to the input PDF file
        num_pages: Number of pages to analyze for token estimate (None = all pages)

    Returns:
        Dictionary with file_size_bytes, file_size_human, word_count, token_estimate

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input is not a PDF file
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() != '.pdf':
        raise ValueError(f"Input must be a PDF file, got: {input_path.suffix}")

    # Get file size
    file_size_bytes = os.path.getsize(input_path)

    # Human-readable size
    if file_size_bytes < 1024:
        file_size_human = f"{file_size_bytes} B"
    elif file_size_bytes < 1024 * 1024:
        file_size_human = f"{file_size_bytes / 1024:.1f} KB"
    else:
        file_size_human = f"{file_size_bytes / (1024 * 1024):.1f} MB"

    # Extract text and count words
    with open(input_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)

        pages_to_read = total_pages if num_pages is None else min(num_pages, total_pages)

        text = ""
        for i in range(pages_to_read):
            text += reader.pages[i].extract_text() or ""

    word_count = len(text.split())
    token_estimate = int(word_count * 1.3)

    return {
        "file_size_bytes": file_size_bytes,
        "file_size_human": file_size_human,
        "total_pages": total_pages,
        "pages_analyzed": pages_to_read,
        "word_count": word_count,
        "token_estimate": token_estimate
    }


def main():
    parser = argparse.ArgumentParser(
        description='Get file size and token estimate for a PDF file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('--pages', '-p', type=int, default=None,
                        help='Number of pages to analyze (default: all pages)')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output as JSON')

    args = parser.parse_args()

    try:
        stats = get_pdf_stats(args.input, args.pages)

        if args.json:
            print(json.dumps(stats))
        else:
            print(f"File size: {stats['file_size_human']} ({stats['file_size_bytes']} bytes)")
            print(f"Total pages: {stats['total_pages']}")
            print(f"Pages analyzed: {stats['pages_analyzed']}")
            print(f"Word count: {stats['word_count']:,}")
            print(f"Token estimate: {stats['token_estimate']:,}")

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
