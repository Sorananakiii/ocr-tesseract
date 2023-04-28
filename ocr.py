import pytesseract, cv2
from PIL import Image
import numpy as np
import argparse


# init tesseract engine on your computer
tessing = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tessing

def ocr(image_path, lang='tha+eng', save_file=False):
    im = np.asarray(Image.open(image_path))
    # binarization
    _, thresh = cv2.threshold(im, 220, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, lang=lang)

    # save text into txt file 
    if save_file:
        txt_path = image_path.replace('.png', '.txt').replace('.jpg', '.txt')
        with open(txt_path, 'w', encoding="utf-8") as f:
            f.write(text)
        print(f'Save txt file : {str(txt_path)}')
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OCR engine for image to text')
    parser.add_argument("-p", "--path", help="input image path", type=str)
    parser.add_argument("-s", "--save_file", 
                        help="save output into txt file", 
                        nargs='?', const=True, default=False)

    args = parser.parse_args()
    text = ocr(args.path, save_file=args.save_file)
    print(text)