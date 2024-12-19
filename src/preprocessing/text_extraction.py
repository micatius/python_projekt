import concurrent
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from src.config import TESSERACT_CMD
from src.preprocessing.image_processing import preprocess_image

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image, languages='hrv+fra+deu'):
    image = preprocess_image(image)
    return pytesseract.image_to_string(image, lang=languages)

def extract_text_from_pdf(pdf_path, max_pages=3, languages='hrv+fra+deu'):
    pages = convert_from_path(pdf_path, first_page=1, last_page=max_pages)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        texts = executor.map(lambda page: extract_text_from_image(page, languages), pages)
    return ''.join(texts)


def convert_image_to_txt(image_path: str, languages='hrv+fra+deu') -> str:
    extracted_text = ""
    img = Image.open(image_path)
    extracted_text = extract_text_from_image(img, languages=languages)
    return extracted_text



