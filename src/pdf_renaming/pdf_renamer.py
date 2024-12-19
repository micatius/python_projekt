import os
from src.preprocessing import extract_text_from_pdf
from src.utils import find_name_surname_date
from src.utils.exception_handler import ExceptionHandler


class PdfRenamer:
    def __init__(self, folder_path, pdf_files):
        self.folder_path = folder_path
        self.pdf_files = pdf_files
        self.exception_handler = ExceptionHandler()

    def rename_pdf(self, pdf_path, name_surname, date):
        try:

            new_filename = f"{name_surname} - Karton {date}.pdf"
            new_filepath = os.path.join(os.path.dirname(pdf_path), new_filename)
            os.rename(pdf_path, new_filepath)
            return True

        except Exception as e:
            self.exception_handler.log_exception(f"Pogreška u preimenovanju {pdf_path}: {e}")
            return False

    def process_pdf(self, pdf_path):
        try:

            text = extract_text_from_pdf(pdf_path, 1)

            name_surname_date = find_name_surname_date(text)

            if name_surname_date and name_surname_date[0] and name_surname_date[1]:
                name_surname, date = name_surname_date
                return self.rename_pdf(pdf_path, name_surname, date)
            else:

                self.exception_handler.log_exception(f"Nije moguće pronaći potrebne informacije u  {pdf_path}.")
                return False

        except Exception as e:
            self.exception_handler.log_exception(f"Pogreška u procesuiranju {pdf_path}: {e}")
            return False

    def process_pdfs(self):
        total_success = 0
        total_error = 0

        for pdf_file in self.pdf_files:
            result = self.process_pdf(pdf_file)

            if result:
                total_success += 1

            else:
                total_error += 1

        return total_success, total_error
