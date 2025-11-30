# ScansMerger

A simple Python GUI application to merge scanned PDF files.

## Description

This application merges two PDF files from a scanner where:
- **First file** contains odd pages (1, 3, 5, ...)
- **Second file** contains even pages in reverse order (6, 4, 2, ...)

The result is a properly ordered merged PDF (1, 2, 3, 4, 5, 6, ...).

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- PyPDF2

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/vitzeman/ScansMerger.git
   cd ScansMerger
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python pdf_merger.py
```

1. Click "Browse" to select the PDF file with odd pages (1, 3, 5, ...)
2. Click "Browse" to select the PDF file with even pages in reverse order (6, 4, 2, ...)
3. Click "Merge PDFs" and choose where to save the merged output
4. The application will create a properly ordered PDF file

## How It Works

When scanning a double-sided document on a single-sided scanner:
1. First scan all odd pages (front sides) → Creates file with pages 1, 3, 5, ...
2. Flip the stack and scan all even pages (back sides) → Creates file with pages in reverse order (last even page first)

This application automatically handles the page ordering to produce a correctly merged document.
