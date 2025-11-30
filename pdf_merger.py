#!/usr/bin/env python3
"""
PDF Scans Merger - A Tkinter GUI application for merging scanned PDF files.

This application merges two PDF files where:
- First file contains odd pages (1, 3, 5, ...)
- Second file contains even pages in reverse order (6, 4, 2 or 4, 2)

The result is a merged PDF with pages in correct order (1, 2, 3, 4, 5, 6, ...).
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import os


class PDFMergerApp:
    """Tkinter GUI application for merging scanned PDF files."""
    
    def __init__(self, root):
        """Initialize the PDF Merger application.
        
        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("PDF Scans Merger")
        self.root.geometry("600x300")
        self.root.resizable(True, True)
        
        # File paths
        self.odd_pages_file = tk.StringVar()
        self.even_pages_file = tk.StringVar()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="PDF Scans Merger", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Merge scanned PDFs: File 1 (odd pages: 1,3,5...) + File 2 (even pages reversed: 6,4,2...)",
            wraplength=550
        )
        desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Odd pages file selection
        ttk.Label(main_frame, text="Odd Pages File (1,3,5...):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.odd_pages_file, width=50).grid(
            row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Browse", command=self._browse_odd_file).grid(
            row=2, column=2, pady=5
        )
        
        # Even pages file selection
        ttk.Label(main_frame, text="Even Pages File (6,4,2...):").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.even_pages_file, width=50).grid(
            row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Browse", command=self._browse_even_file).grid(
            row=3, column=2, pady=5
        )
        
        # Merge button
        merge_btn = ttk.Button(
            main_frame, 
            text="Merge PDFs", 
            command=self._merge_pdfs
        )
        merge_btn.grid(row=4, column=0, columnspan=3, pady=30)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=5, column=0, columnspan=3)
    
    def _browse_odd_file(self):
        """Open file dialog to select the odd pages PDF file."""
        filename = filedialog.askopenfilename(
            title="Select PDF with Odd Pages (1,3,5...)",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.odd_pages_file.set(filename)
    
    def _browse_even_file(self):
        """Open file dialog to select the even pages PDF file."""
        filename = filedialog.askopenfilename(
            title="Select PDF with Even Pages (reversed: 6,4,2...)",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.even_pages_file.set(filename)
    
    def _merge_pdfs(self):
        """Merge the selected PDF files."""
        odd_file = self.odd_pages_file.get()
        even_file = self.even_pages_file.get()
        
        # Validate inputs
        if not odd_file or not even_file:
            messagebox.showerror("Error", "Please select both PDF files.")
            return
        
        if not os.path.exists(odd_file):
            messagebox.showerror("Error", f"Odd pages file not found: {odd_file}")
            return
        
        if not os.path.exists(even_file):
            messagebox.showerror("Error", f"Even pages file not found: {even_file}")
            return
        
        # Ask for output file location
        output_file = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged_output.pdf"
        )
        
        if not output_file:
            return
        
        try:
            self._perform_merge(odd_file, even_file, output_file)
            self.status_label.config(text=f"Successfully merged to: {output_file}", foreground="green")
            messagebox.showinfo("Success", f"PDFs merged successfully!\n\nSaved to: {output_file}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")
    
    def _perform_merge(self, odd_file, even_file, output_file):
        """Perform the actual PDF merge operation.
        
        Args:
            odd_file: Path to PDF containing odd pages (1,3,5...).
            even_file: Path to PDF containing even pages in reverse order (6,4,2...).
            output_file: Path for the merged output PDF.
        """
        # Read both PDF files
        odd_reader = PdfReader(odd_file)
        even_reader = PdfReader(even_file)
        
        # Get pages from each file
        odd_pages = list(odd_reader.pages)  # Pages 1, 3, 5, ... (0-indexed: 0, 1, 2, ...)
        even_pages = list(even_reader.pages)  # Pages in reverse: 6, 4, 2 (0-indexed: 0, 1, 2, ...)
        
        # Reverse the even pages to get correct order (2, 4, 6, ...)
        even_pages_corrected = list(reversed(even_pages))
        
        # Create the merged PDF
        writer = PdfWriter()
        
        # Interleave odd and even pages
        # odd_pages[0] = page 1, even_pages_corrected[0] = page 2
        # odd_pages[1] = page 3, even_pages_corrected[1] = page 4
        # etc.
        
        max_pages = max(len(odd_pages), len(even_pages_corrected))
        
        for i in range(max_pages):
            # Add odd page (1, 3, 5, ...)
            if i < len(odd_pages):
                writer.add_page(odd_pages[i])
            
            # Add even page (2, 4, 6, ...)
            if i < len(even_pages_corrected):
                writer.add_page(even_pages_corrected[i])
        
        # Write the merged PDF to output file
        with open(output_file, 'wb') as output:
            writer.write(output)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
