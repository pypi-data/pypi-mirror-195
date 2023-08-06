import pytesseract
import cv2

class NormalCaptcha:

    def __init__(self, path: str, image: str):
        if path is None or image in [None, '']:
            raise ValueError('Os Valores devem ser preenchidos')

        pytesseract.pytesseract.tesseract_cmd = path
        self.img = image

    def processa(self):
        imagem = cv2.imread(self.img)
        texto = pytesseract.image_to_string(imagem)
        return texto
