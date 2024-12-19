import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.preprocessing.text_extraction import extract_text_from_pdf, convert_image_to_txt
from src.utils.exception_handler import ExceptionHandler
import threading


class TextConverterForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.exception_handler = ExceptionHandler()
        self.configure(style='Form.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)


        self.title_label = ttk.Label(
            self,
            text="Ekstrakcija teksta iz slike ili PDF-a",
            style="FormTitle.TLabel",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))


        self.label = ttk.Label(
            self,
            text="Odaberite sliku ili PDF za ekstrakciju teksta:",
            style="Form.TLabel",
        )
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do slike ili PDF-a")

        self.browse_button = ttk.Button(
            self,
            text="Odaberi sliku ili PDF",
            style="Form.TButton",
            command=self.browse_file,
        )
        self.browse_button.grid(row=2, column=1, sticky="ew")


        self.output_label = ttk.Label(
            self,
            text="Odaberite izlaznu putanju za tekst:",
            style="Form.TLabel",
        )
        self.output_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        self.output_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.output_path_entry.grid(row=4, column=0, sticky="ew", padx=(0, 10))
        self.output_path_entry.insert(0, "Putanja za spremanje teksta")

        self.browse_output_button = ttk.Button(
            self,
            text="Odaberi izlaznu putanju",
            style="Form.TButton",
            command=self.browse_output,
        )
        self.browse_output_button.grid(row=4, column=1, sticky="ew")

        self.extract_button = ttk.Button(
            self,
            text="Ekstrahiraj tekst",
            style="Form.TButton",
            command=self.start_text_extraction_thread,
        )
        self.extract_button.grid(row=5, column=0, columnspan=2, pady=(20, 10))


        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=6, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Initially hidden


    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Odaberite sliku ili PDF",
            filetypes=[("Image and PDF files", "*.jpg;*.jpeg;*.png;*.bmp;*.pdf")],
        )
        if file_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
        )
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)

    def start_text_extraction_thread(self):
        input_file_path = self.folder_path_entry.get()
        output_txt_path = self.output_path_entry.get()


        if not input_file_path or not os.path.isfile(input_file_path):
            messagebox.showwarning("Pogreška", "Molim odaberite valjanu sliku ili PDF!")
            return

        if not output_txt_path or output_txt_path == "Putanja za spremanje teksta":
            messagebox.showwarning("Pogreška", "Molim odaberite odredište za tekst datoteku!")
            return

        output_directory = os.path.dirname(output_txt_path)
        if not os.path.isdir(output_directory):
            messagebox.showwarning("Pogreška", "Odabrana izlazna putanja ne postoji!")
            return


        self.extract_button.config(state=tk.DISABLED)
        self.progressbar.grid()
        self.progressbar.start()

        threading.Thread(target=self.extract_and_save_text, args=(input_file_path, output_txt_path)).start()

    def extract_and_save_text(self, input_file_path, output_txt_path):
        try:

            if input_file_path.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(input_file_path)
            else:
                extracted_text = convert_image_to_txt(input_file_path)


            with open(output_txt_path, 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)


            self.after(0, lambda: messagebox.showinfo("Uspjeh", f"Tekst je uspješno ekstrahiran: {output_txt_path}"))
        except Exception as e:
            self.exception_handler.log_exception(e)
            self.after(0, lambda: messagebox.showerror("Greška", "Došlo je do greške prilikom ekstrakcije teksta. Pogledajte log za detalje."))


        self.after(0, lambda: self.extract_button.config(state=tk.NORMAL))
        self.after(0, lambda: self.progressbar.stop())
        self.after(0, lambda: self.progressbar.grid_remove())
