# config.py
import os

# Putanja do instalacije Tesseract OCR-a
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#Ovdje su definirani razni stilovi kako bi aplikacija bolje izgledala
def set_global_styles(style, theme='light'):
    if theme == 'light':
        background = "#F4F6F9"
        foreground = "#000000"
        form_background = "#FFFFFF"
        button_bg = "#4b80b8"
        button_active = "#2a7d8f"
        button_pressed = "#1b6a6d"
        entry_bg = "#f8f8f8"
        entry_fg = "#333"
        list_bg = "#f8f8f8"
        list_fg = "#333"
        progress_bg = "#3B6B9D"
        progress_trough = "#F4F6F9"
    else:
        background = "#2B3A42"
        foreground = "#F4F6F9"
        form_background = "#3A4750"
        button_bg = "#6A994E"
        button_active = "#5A8641"
        button_pressed = "#4D6F36"
        entry_bg = "#49565C"
        entry_fg = "#333"
        list_bg = "#3A4750"
        list_fg = "#F4F6F9"
        progress_bg = "#6A994E"
        progress_trough = "#3A4750"


    style.theme_use('clam')

    style.configure('MainFrame.TFrame', background=background)
    style.configure('Title.TLabel', background=background, foreground=foreground, font=('Arial', 26, 'bold'))


    style.configure('Form.TFrame', background=form_background, padding=20)
    style.configure('FormTitle.TLabel', background=form_background, foreground=button_bg, font=('Arial', 18, 'bold'))


    style.configure(
        'Elevated.TButton',
        font=('Arial', 14, 'bold'),
        padding=12,
        relief='raised',
        borderwidth=3,
        background=button_bg,
        foreground=foreground
    )
    style.map(
        'Elevated.TButton',
        background=[('active', button_active), ('pressed', button_pressed)],
        relief=[('pressed', 'sunken')]
    )
    style.configure('Form.TButton',
                    font=('Arial', 12, 'bold'),
                    background=button_bg,
                    foreground=foreground,
                    padding=10,
                    relief="flat")

    style.map('Form.TButton',
              background=[('active', button_active), ('pressed', button_pressed)])


    style.configure('Custom.TEntry',
                    font=("Arial", 16),
                    padding=(12, 14),
                    foreground=entry_fg,
                    background=entry_bg,
                    borderwidth=2,
                    relief="sunken")


    style.configure('Custom.TListbox',
                    font=("Arial", 14),
                    foreground=list_fg,
                    background=list_bg,
                    padding=10,
                    borderwidth=2)


    style.configure("TProgressbar",
                    thickness=20,
                    background=progress_bg,
                    troughcolor=progress_trough)


    style.configure('Form.TLabel',
                    foreground=foreground,
                    background=form_background,
                    font=('Arial', 12, 'bold'))
