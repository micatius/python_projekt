from PIL import Image, ImageEnhance
import pytesseract
from src.config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image(image: Image) -> Image:
    image = image.convert('L')  # Pretvorite sliku u crno-bijelu
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Poboljšajte kontrast
    return image


