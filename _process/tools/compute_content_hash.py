#!/usr/bin/env python3
"""
Compute a content hash from the first N pages of a PDF file.

The hash is computed from the extracted text content, making it useful
for detecting duplicate documents regardless of filename or metadata differences.

Usage:
    python compute_content_hash.py <input.pdf> [--pages N]

Examples:
    python compute_content_hash.py document.pdf
    python compute_content_hash.py document.pdf --pages 5
"""

import argparse
import hashlib
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def compute_content_hash(input_path: str, num_pages: int = 3) -> str:
    """
    Compute SHA256 hash of text extracted from the first N pages of a PDF.

    Args:
        input_path: Path to the input PDF file
        num_pages: Number of pages to extract text from (default: 3)

    Returns:
        SHA256 hash as hexadecimal string

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input is not a PDF file
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() != '.pdf':
        raise ValueError(f"Input must be a PDF file, got: {input_path.suffix}")

    with open(input_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        pages_to_read = min(num_pages, len(reader.pages))

        for i in range(pages_to_read):
            text += reader.pages[i].extract_text() or ""

    return hashlib.sha256(text.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='Compute content hash from the first N pages of a PDF.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('--pages', '-p', type=int, default=3,
                        help='Number of pages to extract text from (default: 3)')

    args = parser.parse_args()

    try:
        content_hash = compute_content_hash(args.input, args.pages)
        print(content_hash)
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
