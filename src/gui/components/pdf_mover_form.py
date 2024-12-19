import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.pdf_moving.pdf_mover import PdfMover
import threading
from concurrent import futures              #Potreban import iako se nigdje u kod izravno ne koristi - bez njega ne radi, ali ne znam zašto



class PdfMoverForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='Form.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)


        self.title_label = ttk.Label(
            self,
            text="Premještanje PDF datotekama",
            style="FormTitle.TLabel",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))


        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:", style="Form.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        self.browse_button = ttk.Button(
            self,
            text="Odaberi direktorij",
            command=self.browse_folder,
            style="Form.TButton",
        )
        self.browse_button.grid(row=2, column=1, sticky="ew")


        self.destination_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.destination_path_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        self.destination_path_entry.insert(0, "Putanja do odredišne mape")

        self.destination_button = ttk.Button(
            self,
            text="Odaberi odredišnu mapu",
            command=self.select_destination_folder,
            style="Form.TButton",
        )
        self.destination_button.grid(row=3, column=1, sticky="ew", pady=(5, 10))


        self.listbox_frame = ttk.Frame(self, style="Form.TFrame")
        self.listbox_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.file_listbox = tk.Listbox(
            self.listbox_frame,
            selectmode=tk.MULTIPLE,
            height=10,
            bg="#f9f9f9",
            bd=0,
            highlightthickness=1,
            font=("Arial", 10),
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)

        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        self.move_button = ttk.Button(
            self,
            text="Premjesti PDF",
            command=self.start_move_pdfs_thread,
            style="Form.TButton",
        )
        self.move_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 10))


        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=6, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Initially hide the progress bar

    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite direktorij s PDF datotekama")
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        self.file_listbox.delete(0, tk.END)
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        self.pdf_files = [os.path.join(folder_path, f) for f in pdf_files]
        for pdf_file in pdf_files:
            self.file_listbox.insert(tk.END, pdf_file)

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite odredišnu mapu")
        if folder_path:
            self.destination_folder = folder_path
            self.destination_path_entry.delete(0, tk.END)
            self.destination_path_entry.insert(0, folder_path)
            messagebox.showinfo("Odabrana mapa", f"Odabrana odredišna mapa: {self.destination_folder}")

    def start_move_pdfs_thread(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za premještanje.")
            return

        self.move_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.move_selected_pdfs)
        thread.start()

    def move_selected_pdfs(self):
        if not hasattr(self, 'destination_folder') or not self.destination_folder:
            self.after(0, lambda: messagebox.showwarning("Upozorenje", "Niste odabrali odredišnu mapu."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Re-enable button
            return

        if not self.pdf_files:
            self.after(0, lambda: messagebox.showwarning("Upozorenje", "Niste učitali PDF datoteke."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Re-enable button
            return

        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.after(0, lambda: messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za premještanje."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Re-enable button
            return

        pdf_files_to_move = [self.pdf_files[index] for index in selected_indices]
        pdf_mover = PdfMover(self.destination_folder)

        success_count = 0
        failure_count = 0

        self.after(0, lambda: self.progressbar.grid())
        self.after(0, lambda: self.progressbar.start())

        for pdf_path in pdf_files_to_move:
            result = pdf_mover.process_and_move_pdf(pdf_path)
            if result:
                success_count += 1
            else:
                failure_count += 1

        self.after(0, lambda: self.progressbar.stop())
        self.after(0, lambda: self.progressbar.grid_remove())
        self.after(0, lambda: self.move_button.config(state=tk.NORMAL))

        if success_count == 0:
            self.after(0, lambda: messagebox.showerror("Greška", "Nijedan PDF nije uspješno premješten. Za više informacija pogledaj log."))
        elif success_count > 0 and failure_count > 0:
            self.after(0, lambda: messagebox.showinfo(
                "Uspjeh",
                f"Premještanje završeno.\n"
                f"Uspješno premješteno: {success_count}\n"
                f"Neuspješno premješteno: {failure_count}. Za više informacija pogledaj log."
            ))

        else:
            self.after(0, lambda: messagebox.showinfo(
                "Uspjeh",
                f"Premještanje završeno.\n"
                f"Uspješno premješteno: {success_count}"))


        self.after(0, lambda: self.load_pdf_files(self.folder_path_entry.get()))
