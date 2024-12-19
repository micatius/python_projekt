
import os
import logging
from tkinter import messagebox


class ExceptionHandler:
    def __init__(self, log_dir="../../logs", log_file="errors.log"):
        self.log_dir = log_dir
        self.log_file = log_file
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, log_file)
        logging.basicConfig(
            filename=log_path,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            encoding='utf-8'
        )

    def log_exception(self, exception):
        logging.error(str(exception))

    def show_user_message(self, message):
        messagebox.showerror("Error", message)

   