import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.image_to_scanned_document.image_to_document_scanner import ImageToPdfScanner
from src.utils.exception_handler import ExceptionHandler
from PIL import Image, ImageTk
import threading

class ImageToPdfForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.exception_handler = ExceptionHandler()

        self.configure(style='Form.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(7, weight=1)

        self.title_label = ttk.Label(
            self,
            text="Konverzija slike u skenirani PDF dokument",
            style="FormTitle.TLabel",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.image_label = ttk.Label(self, text="Odaberite sliku za konverziju:", style="Form.TLabel")
        self.image_label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        self.image_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.image_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.image_path_entry.insert(0, "Putanja do slike")

        self.browse_image_button = ttk.Button(
            self,
            text="Odaberi sliku",
            style="Form.TButton",
            command=self.browse_image,
        )
        self.browse_image_button.grid(row=2, column=1, sticky="ew", padx=(5, 0))

        self.output_label = ttk.Label(self, text="Odaberite izlaznu putanju:", style="Form.TLabel")
        self.output_label.grid(row=3, column=0, columnspan=2, pady=(5, 5))

        self.output_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.output_path_entry.grid(row=4, column=0, sticky="ew", padx=(0, 5))
        self.output_path_entry.insert(0, "Putanja za spremanje")

        self.browse_output_button = ttk.Button(
            self,
            text="Odaberi izlaznu putanju",
            style="Form.TButton",
            command=self.browse_output,
        )
        self.browse_output_button.grid(row=4, column=1, sticky="ew", padx=(5, 0))

        self.image_display_label = ttk.Label(self)
        self.image_display_label.grid(row=5, column=0, columnspan=2, pady=(10, 10))
        self.image_display_label.grid_remove()  # Hide the image label initially

        self.convert_button = ttk.Button(
            self,
            text="Konvertiraj",
            style="Form.TButton",
            command=self.start_conversion_thread,
        )
        self.convert_button.grid(row=6, column=0, columnspan=2, pady=(20, 10))

        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=7, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Hidden initially

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)
            self.display_image(file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((150, 150))  # Resize to fit within the window
        photo = ImageTk.PhotoImage(image)

        self.image_display_label.config(image=photo)
        self.image_display_label.image = photo

        self.image_display_label.grid()

    def start_conversion_thread(self):
        input_image_path = self.image_path_entry.get()
        output_pdf_path = self.output_path_entry.get()

        if not input_image_path or not os.path.isfile(input_image_path):
            messagebox.showwarning("Pogreška", "Molim odaberite valjanu sliku!")
            return

        if not output_pdf_path or output_pdf_path == "Putanja za spremanje":
            messagebox.showwarning("Pogreška", "Molim odaberite odredište za PDF datoteku!")
            return

        output_directory = os.path.dirname(output_pdf_path)
        if not os.path.isdir(output_directory):
            messagebox.showwarning("Pogreška", "Odabrana izlazna putanja ne postoji!")
            return

        self.convert_button.config(state=tk.DISABLED)
        self.progressbar.grid()
        self.progressbar.start()

        threading.Thread(target=self.convert_image_to_pdf, args=(input_image_path, output_pdf_path)).start()

    def convert_image_to_pdf(self, input_image_path, output_pdf_path):
        scanner = ImageToPdfScanner(input_image_path, output_pdf_path)

        try:
            scanner.process_and_save()
            self.after(0, lambda: messagebox.showinfo("Uspjeh", f"PDF uspješno spremljen u {output_pdf_path}"))
        except Exception as e:
            self.exception_handler.log_exception(e)
            self.after(0, lambda: self.exception_handler.show_user_message(
                "Dogodila se pogreška. Za više detalja pogledajte log datoteku."))

        self.after(0, lambda: self.convert_button.config(state=tk.NORMAL))
        self.after(0, lambda: self.progressbar.grid_remove())
