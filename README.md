# Robinhood Library

A document library about Robinhood Markets, Inc. (NASDAQ: HOOD).

## Purpose

This library supports the development of a Data and AI strategy and business plan for the CMU Heinz Chief Data & AI Officer (CDAIO) Certificate program capstone deliverable.

## Repository Structure

```
robinhood-library/
├── _process/                    # Processing infrastructure
│   ├── input-buffer/            # Incoming documents to be processed
│   ├── tmp/                     # Temporary files during processing
│   └── tools/                   # Processing scripts
├── library/                     # Organized document library
│   ├── index.json               # Document catalog with metadata
│   ├── earnings/                # Earnings materials
│   ├── esg/                     # ESG reports
│   ├── governance/              # Governance documents
│   ├── investor-relations/      # Investor presentations and transcripts
│   ├── operating-data/          # Monthly operating data
│   ├── press-releases/          # Press releases and M&A announcements
│   └── sec-filings/             # SEC filings (10-K, 10-Q, etc.)
└── README.md
```

## Tools

Located in `_process/tools/`:

| Tool | Purpose | Usage |
|------|---------|-------|
| `extract_first_pages.py` | Extract first N pages from PDF | `python3 _process/tools/extract_first_pages.py <input.pdf> [-p N] [-o DIR]` |
| `compute_content_hash.py` | Compute SHA256 hash for duplicate detection | `python3 _process/tools/compute_content_hash.py <input.pdf> [-p N]` |
| `pdf_stats.py` | Get file size and token estimate | `python3 _process/tools/pdf_stats.py <input.pdf> [-p N] [--json]` |

## Git Strategy

This repository uses a single-branch strategy. All commits are made directly to the `main` branch.
