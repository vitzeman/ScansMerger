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
        self.root.geometry("600x600")
        self.root.resizable(True, True)

        # File paths
        self.odd_pages_file = tk.StringVar()
        self.even_pages_file = tk.StringVar()

        self._create_widgets()

    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame with padding
        current_row = 0
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=current_row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title label
        title_label = ttk.Label(
            main_frame, text="Slučování skenů - PDF", font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=current_row, column=0, columnspan=4, pady=(0, 20))
        current_row += 1
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Sloučení skenovaných PDF: PDF 1 (liché stránky: 1,3,5...) + PDF 2 (sudé stránky v obráceném pořadí: 6,4,2...)",
            # wraplength=550,
        )
        desc_label.grid(row=current_row, column=0, columnspan=4, pady=(0, 15))
        current_row += 1

        # Odd pages file selection
        ttk.Label(main_frame, text="PDF s lichými stránkami (1,3,5...):").grid(
            row=current_row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.odd_pages_file, width=50).grid(
            row=current_row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Procházet", command=self._browse_odd_file).grid(
            row=current_row, column=2, pady=5
        )
        self.rotate_odd = tk.BooleanVar()
        ttk.Checkbutton(
            main_frame,
            text="Otočit stránky",
            variable=self.rotate_odd,
        ).grid(row=current_row, column=3, padx=10, pady=5)
        current_row += 1

        # Even pages file selection
        ttk.Label(main_frame, text="PDF se sudými stránkami (6,4,2...):").grid(
            row=current_row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.even_pages_file, width=50).grid(
            row=current_row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Procházet", command=self._browse_even_file).grid(
            row=current_row, column=2, pady=5
        )
        self.rotate_even = tk.BooleanVar()
        ttk.Checkbutton(
            main_frame,
            text="Otočit stránky",
            variable=self.rotate_even,
        ).grid(row=current_row, column=3, padx=10, pady=5)
        current_row += 1
        # Merge button
        merge_btn = ttk.Button(main_frame, text="Sloučit PDF", command=self._zip_pdfs)
        merge_btn.grid(row=current_row, column=0, columnspan=4, pady=30)

        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1
        # Append pages to the previous file

        desc_label = ttk.Label(
            main_frame,
            text="Přidání stránek druhého PDF na konec prvního PDF",
            wraplength=550,
        )
        desc_label.grid(row=current_row, column=0, columnspan=4, pady=(0, 15))
        current_row += 1
        # Odd pages file selection
        ttk.Label(main_frame, text="První PDF").grid(
            row=current_row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.odd_pages_file, width=50).grid(
            row=current_row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Procházet", command=self._browse_first_file).grid(
            row=current_row, column=2, pady=5
        )
        self.rotate_first = tk.BooleanVar()
        ttk.Checkbutton(
            main_frame,
            text="Otočit stránky",
            variable= self.rotate_first

        ).grid(row=current_row, column=3, padx=10, pady=5)
        current_row += 1
        # Even pages file selection
        ttk.Label(main_frame, text="Druhé PDF").grid(
            row=current_row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.even_pages_file, width=50).grid(
            row=current_row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E)
        )
        ttk.Button(main_frame, text="Procházet", command=self._browse_second_file).grid(
            row=current_row, column=2, pady=5
        )
        self.rotate_second = tk.BooleanVar()
        ttk.Checkbutton(
            main_frame,
            text="Otočit stránky",
            variable=self.rotate_second,
        ).grid(row=current_row, column=3, padx=10, pady=5)
        current_row += 1
        # Merge button
        merge_btn = ttk.Button(
            main_frame, text="Sečíst PDFka", command=self._append_pdfs
        )
        merge_btn.grid(row=current_row, column=0, columnspan=4, pady=30)
        current_row += 1
        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=current_row, column=0, columnspan=3)
        current_row += 1

    def _browse_first_file(self):
        """Open file dialog to select the first PDF file."""
        filename = filedialog.askopenfilename(
            title="Vyberte první PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if filename:
            self.odd_pages_file.set(filename)

    def _browse_second_file(self):
        """Open file dialog to select the second PDF file."""
        filename = filedialog.askopenfilename(
            title="Vyberte druhé PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if filename:
            self.even_pages_file.set(filename)

    def _browse_odd_file(self):
        """Open file dialog to select the odd pages PDF file."""
        filename = filedialog.askopenfilename(
            title="Vyberte PDF s lichými stránkami (1,3,5...)",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if filename:
            self.odd_pages_file.set(filename)

    def _browse_even_file(self):
        """Open file dialog to select the even pages PDF file."""
        filename = filedialog.askopenfilename(
            title="Vyberte PDF se sudými stránkami (6,4,2...)",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if filename:
            self.even_pages_file.set(filename)

    def _zip_pdfs(self):
        """Merge the selected PDF files."""
        odd_file = self.odd_pages_file.get()
        even_file = self.even_pages_file.get()

        # Validate inputs
        if not odd_file or not even_file:
            messagebox.showerror("Chyba", "Prosím vyberte oba PDF soubory.")
            return

        if not os.path.exists(odd_file):
            messagebox.showerror(
                "Chyba", f"Soubor s lichými stránkami nenalezen: {odd_file}"
            )
            return

        if not os.path.exists(even_file):
            messagebox.showerror(
                "Chyba", f"Soubor se sudými stránkami nenalezen: {even_file}"
            )
            return

        # Ask for output file location
        output_file = filedialog.asksaveasfilename(
            title="Uložit sloučené PDF jako",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged_output.pdf",
        )

        if not output_file:
            return

        try:
            self._perform_zip_merge(odd_file, even_file, output_file)
            self.status_label.config(
                text=f"Úspěšně sloučeno do: {output_file}", foreground="green"
            )
            messagebox.showinfo(
                "Úspěch",
                f"PDF soubory byly úspěšně sloučeny!\n\nUloženo do: {output_file}",
            )
        except Exception as e:
            self.status_label.config(text=f"Chyba: {str(e)}", foreground="red")
            messagebox.showerror(
                "Chyba", f"Nepodařilo se sloučit PDF soubory:\n{str(e)}"
            )

    def _perform_zip_merge(self, odd_file, even_file, output_file):
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
        odd_pages = list(
            odd_reader.pages
        )  # Pages 1, 3, 5, ... (0-indexed: 0, 1, 2, ...)
        if self.rotate_odd.get():
            odd_pages = [page.rotate(180) for page in odd_pages]
        even_pages = list(
            even_reader.pages
        )  # Pages in reverse: 6, 4, 2 (0-indexed: 0, 1, 2, ...)
        if self.rotate_even.get():
            even_pages = [page.rotate(180) for page in even_pages]

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
        with open(output_file, "wb") as output:
            writer.write(output)

    def _perform_append(self, first_file, second_file, output_file):
        """Append the second PDF to the end of the first PDF.

        Args:
            first_file: Path to the first PDF file.
            second_file: Path to the second PDF file.
            output_file: Path for the appended output PDF.
        """
        # Read both PDF files
        first_reader = PdfReader(first_file)
        second_reader = PdfReader(second_file)

        # Create the appended PDF
        writer = PdfWriter()

        # Add pages from the first PDF
        for page in first_reader.pages:
            if self.rotate_first.get():
                writer.add_page(page.rotate(180))
            else:
                writer.add_page(page)

        # Add pages from the second PDF
        for page in second_reader.pages:
            if self.rotate_second.get():
                writer.add_page(page.rotate(180))
            else:
                writer.add_page(page)

        # Write the appended PDF to output file
        with open(output_file, "wb") as output:
            writer.write(output)

    def _append_pdfs(self):
        """Append the second PDF to the end of the first PDF."""
        first_file = self.odd_pages_file.get()
        second_file = self.even_pages_file.get()

        # Validate inputs
        if not first_file or not second_file:
            messagebox.showerror("Chyba", "Prosím vyberte oba PDF soubory.")
            return

        if not os.path.exists(first_file):
            messagebox.showerror("Chyba", f"První PDF soubor nenalezen: {first_file}")
            return

        if not os.path.exists(second_file):
            messagebox.showerror("Chyba", f"Druhý PDF soubor nenalezen: {second_file}")
            return

        # Ask for output file location
        output_file = filedialog.asksaveasfilename(
            title="Uložit výsledné PDF jako",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="appended_output.pdf",
        )

        if not output_file:
            return

        try:
            self._perform_append(first_file, second_file, output_file)
            self.status_label.config(
                text=f"Úspěšně přidáno do: {output_file}", foreground="green"
            )
            messagebox.showinfo(
                "Úspěch",
                f"Stránky byly úspěšně přidány!\n\nUloženo do: {output_file}",
            )
        except Exception as e:
            self.status_label.config(text=f"Chyba: {str(e)}", foreground="red")
            messagebox.showerror("Chyba", f"Nepodařilo se přidat stránky:\n{str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
