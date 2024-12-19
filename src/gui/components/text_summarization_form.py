import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.preprocessing.text_extraction import extract_text_from_pdf, convert_image_to_txt
from src.text_summarization.text_summarization import summarize_text
from src.utils.exception_handler import ExceptionHandler
import threading
from src.text_summarization.language_mapping import LANGUAGE_CODE_MAPPING


class TextSummarizationForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.exception_handler = ExceptionHandler()
        self.configure(style='Form.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(10, weight=1)


        self.title_label = ttk.Label(
            self,
            text="Generiranje sažetka teksta",
            style="FormTitle.TLabel",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))


        self.label = ttk.Label(
            self,
            text="Odaberite tekstualnu datoteku za generiranje sažetka:",
            style="Form.TLabel",
        )
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do tekstualne (.txt) datoteke:")

        self.browse_button = ttk.Button(
            self,
            text="Odaberite .txt datoteku",
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

        # languages = sorted(LANGUAGE_CODE_MAPPING.keys())

        # Source Language
        # source_language_label = ttk.Label(self, text="Izvorni jezik:", style="Form.TLabel")
        # source_language_label.grid(row=6, column=0, pady=(10, 5), sticky="e")
        #
        # self.source_language_combobox = ttk.Combobox(self, values=languages, state="readonly")
        # self.source_language_combobox.grid(row=6, column=1, padx=(10, 0), pady=(10, 5), sticky="ew")
        # self.source_language_combobox.current(6)
        #
        # # Target Language
        # target_language_label = ttk.Label(self, text="Jezik sažetka:", style="Form.TLabel")
        # target_language_label.grid(row=7, column=0, pady=(0, 25), sticky="e")
        #
        # self.target_language_combobox = ttk.Combobox(self, values=languages, state="readonly")
        # self.target_language_combobox.grid(row=7, column=1, pady=(0, 25), padx=(10, 0), sticky="ew")
        # self.target_language_combobox.current(6)

        self.summarize_button = ttk.Button(
            self,
            text="Sažmi tekst",
            style="Form.TButton",
            command=self.start_text_summarization,
        )
        self.summarize_button.grid(row=5, column=0, columnspan=2, pady=(20, 10))


        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=8, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Initially hidden


    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Odaberite tekstualnu datoteku",
            filetypes=[("Text files", "*.txt")],
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


    def start_text_summarization(self):
        input_txt_path = self.folder_path_entry.get()
        output_txt_path = self.output_path_entry.get()
        # source_language = self.source_language_combobox.get()
        # target_language = self.target_language_combobox.get()

        if not input_txt_path or not os.path.isfile(input_txt_path):
            messagebox.showwarning("Pogreška", "Molim odaberite valjanu tekstualnu datoteku!")
            return

        if not output_txt_path or output_txt_path == "Putanja za spremanje teksta":
            messagebox.showwarning("Pogreška", "Molim odaberite odredište za tekstualnu datoteku!")
            return

        output_directory = os.path.dirname(output_txt_path)
        if not os.path.isdir(output_directory):
            messagebox.showwarning("Pogreška", "Odabrana izlazna putanja ne postoji!")
            return

        # source_language_code = LANGUAGE_CODE_MAPPING.get(source_language, None)
        # target_language_code = LANGUAGE_CODE_MAPPING.get(target_language, None)

        self.summarize_button.config(state=tk.DISABLED)
        self.progressbar.grid()
        self.progressbar.start()

        threading.Thread(target=self.run_summarization, args=(input_txt_path, output_txt_path)).start()

    def run_summarization(self, input_txt_path, output_txt_path):
        try:
            text_summary = summarize_text(input_txt_path)
            with open(output_txt_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text_summary)

            messagebox.showinfo("Uspjeh", f"Tekst je uspješno sažet: {output_txt_path}")
        except IndexError as ie:
            self.exception_handler.log_exception(ie)
            messagebox.showerror("Greška",
                                 "Došlo je do greške prilikom sažimanja teksta. Nepodržan jezik.\nPogledajte log za detalje.")
        except Exception as e:
            self.exception_handler.log_exception(e)
            messagebox.showerror("Greška",
                                 "Došlo je do greške prilikom sažimanja teksta. Pogledajte log za detalje.")
        finally:
            self.summarize_button.config(state=tk.NORMAL)
            self.progressbar.stop()
            self.progressbar.grid_remove()

