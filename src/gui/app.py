import tkinter as tk
from tkinter import ttk
from src.config import set_global_styles
from src.gui.components.image_to_pdf_form import ImageToPdfForm
from src.gui.components.text_summarization_form import TextSummarizationForm
from src.gui.components.to_text_converter_form import TextConverterForm
from src.gui.components.pdf_mover_form import PdfMoverForm
from src.gui.components.pdf_renamer_form import PdfRenamerForm


def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text_extractor_icon = None
        self.image_to_pdf_icon = None
        self.pdf_mover_icon = None
        self.pdf_renamer_icon = None
        self.translator_icon = None
        self.summarizer_icon = None
        self.current_theme = 'light'

        self.title("File Management Tools")
        self.geometry("800x600")
        self.configure(bg="#F7F7F7")

        self.resizable(width=False, height=False)
        self.minsize(800, 600)

        self.iconphoto(False, tk.PhotoImage(file="../../resources/icons/main_icon.png"))

        self.style = ttk.Style(self)
        self.set_global_styles()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self, style='MainFrame.TFrame', padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        self.title_label = ttk.Label(
            self.main_frame,
            text="File Management Tools",
            font=('Arial', 24, 'bold'),
            anchor="center",
            style="Title.TLabel",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.create_buttons()
        self.create_image_toggle()

    def set_global_styles(self):
        set_global_styles(self.style, self.current_theme)

    def create_buttons(self):
        self.pdf_renamer_icon = tk.PhotoImage(file="../../resources/icons/pdf_renamer.png").subsample(6, 6)
        self.pdf_mover_icon = tk.PhotoImage(file="../../resources/icons/pdf_mover.png").subsample(5, 5)
        self.image_to_pdf_icon = tk.PhotoImage(file="../../resources/icons/image_scanner.png").subsample(6, 6)
        self.text_extractor_icon = tk.PhotoImage(file="../../resources/icons/text_extraction.png").subsample(6, 6)
        self.summarizer_icon = tk.PhotoImage(file="../../resources/icons/summary.png").subsample(6, 6)

        self.main_frame.grid_columnconfigure(0, weight=1, uniform="col")
        self.main_frame.grid_columnconfigure(1, weight=1, uniform="col")

        pdf_renamer_button = ttk.Button(
            self.main_frame,
            text="PDF Renamer",
            command=self.open_pdf_renamer,
            style='Elevated.TButton',
            image=self.pdf_renamer_icon,
            compound=tk.BOTTOM
        )
        pdf_renamer_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))

        pdf_mover_button = ttk.Button(
            self.main_frame,
            text="PDF Mover",
            command=self.open_pdf_mover,
            style='Elevated.TButton',
            image=self.pdf_mover_icon,
            compound=tk.BOTTOM
        )
        pdf_mover_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=(5, 5))

        image_to_pdf_button = ttk.Button(
            self.main_frame,
            text="Image to PDF",
            command=self.open_image_to_pdf,
            style='Elevated.TButton',
            image=self.image_to_pdf_icon,
            compound=tk.BOTTOM
        )
        image_to_pdf_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 5))

        text_extractor_button = ttk.Button(
            self.main_frame,
            text="Text Extractor",
            command=self.open_pdf_converter,
            style='Elevated.TButton',
            image=self.text_extractor_icon,
            compound=tk.BOTTOM
        )
        text_extractor_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=(5, 5))

        summarizer_button = ttk.Button(
            self.main_frame,
            text="Text Summarizer",
            command=self.open_text_summarization,
            style='Elevated.TButton',
            image=self.summarizer_icon,
            compound=tk.BOTTOM
        )
        summarizer_button.grid(row=3, column=1, sticky="nsew", padx=10, pady=(5, 5))

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)


    def create_image_toggle(self):

        self.image_on = tk.PhotoImage(file="../../resources/icons/light_mode.png").subsample(20, 20)
        self.image_off = tk.PhotoImage(file="../../resources/icons/night_mode.png").subsample(20, 20)


        self.toggle_label = tk.Label(self, image=self.image_off, bg="#F7F7F7", cursor="hand2")
        self.toggle_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)


        self.toggle_label.bind("<Button-1>", self.toggle_theme)

    def toggle_theme(self, event=None):

        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'


        new_image = self.image_on if self.current_theme == 'dark' else self.image_off
        self.toggle_label.configure(image=new_image)


        new_bg = "#2B3A42" if self.current_theme == 'dark' else "#F7F7F7"
        self.configure(bg=new_bg)
        self.toggle_label.configure(bg=new_bg)


        self.set_global_styles()
        self.update_theme()

    def update_theme(self):
        self.configure(bg=self.style.lookup('MainFrame.TFrame', 'background'))

    def open_pdf_renamer(self):
        self.open_new_window(PdfRenamerForm, "PDF Renamer")

    def open_pdf_mover(self):
        self.open_new_window(PdfMoverForm, "PDF Mover")

    def open_pdf_converter(self):
        self.open_new_window(TextConverterForm, "PDF Converter")

    def open_image_to_pdf(self):
        self.open_new_window(ImageToPdfForm, "Image to PDF")

    def open_text_summarization(self):
        self.open_new_window(TextSummarizationForm, "Text Summarization")

    def open_new_window(self, form_class, title):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_window.geometry("700x500")
        new_window.configure(bg="#F7F7F7")

        new_window.resizable(width=False, height=False)

        new_window.iconphoto(False, tk.PhotoImage(file="../../resources/icons/main_icon.png"))
        self.center_window(new_window)

        padded_frame = ttk.Frame(new_window, style='Form.TFrame')
        padded_frame.pack(fill=tk.BOTH, expand=True)

        form_class(padded_frame).pack(fill=tk.BOTH, expand=True)

        new_window.grab_set()
        new_window.focus_set()
        new_window.transient(self)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()

        position_left = main_window_x + (main_window_width // 2) - (width // 2)
        position_top = main_window_y + (main_window_height // 2) - (height // 2)

        window.geometry(f'{width}x{height}+{position_left}+{position_top}')


if __name__ == "__main__":
    main()
