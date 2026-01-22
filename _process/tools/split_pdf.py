#!/usr/bin/env python3
"""
Split a PDF file into single-page PDF files.

Usage:
    python split_pdf.py <input.pdf> [--output-dir DIR]

Examples:
    python split_pdf.py document.pdf
    python split_pdf.py document.pdf --output-dir /path/to/output
"""

import argparse
import sys
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


def split_pdf(input_path: str, output_dir: str) -> list[str]:
    """
    Split a PDF file into single-page PDF files.

    Args:
        input_path: Path to the input PDF file
        output_dir: Directory to save the output files

    Returns:
        List of paths to the output files

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

    output_files = []
    stem = input_path.stem

    with open(input_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)

        for i in range(total_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])

            page_num = i + 1
            output_path = output_dir / f"{stem}-page-{page_num:04d}.pdf"

            with open(output_path, 'wb') as out:
                writer.write(out)

            output_files.append(str(output_path))

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description='Split a PDF file into single-page PDF files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('--output-dir', '-o', default='tmp/pages',
                        help='Output directory (default: tmp/pages)')

    args = parser.parse_args()

    try:
        output_files = split_pdf(args.input, args.output_dir)
        print(f"Split into {len(output_files)} pages:")
        print(f"  Directory: {args.output_dir}")
        print(f"  Files: {Path(output_files[0]).name} to {Path(output_files[-1]).name}")
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
