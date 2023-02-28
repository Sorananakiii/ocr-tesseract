import os, cv2, glob, random, time, io, requests
import re, math, base64, yaml, json
import pandas as pd, numpy as np

import pytesseract, fitz
from PIL import Image, ImageFilter
from skimage.color import rgb2gray
from skimage import measure
from urllib.parse import urlparse
from functools import cmp_to_key



def read_image(path, resize=False, new_size=(256, 256)):
    """
    function: read image file from local/resizing
        <arg> path: local file path
              resize: True/False
              new_size: (w, h)
    """
    org = cv2.imread(path)
    if resize :
        org = cv2.resize(org, new_size, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
    return org, gray


def check_is_local(url):
    """
    function: check local file or url name
        <arg> url: url or local path
    """
    url_parsed = urlparse(url)
    if url_parsed.scheme in ('file', ''): # Possibly a local file
        if os.path.exists(url_parsed.path):
            return True, "local"
        else:
            return False, "local"
    return False, "url"


def pdf2image(pdf_input, scale=(1.0, 1.0), png_name=None):
    """
    function: convert pdf to png by separate each page (1 page 1 image)
        <arg> pdf_input: url or local path
              scale: (x scale, y scale)
              png_name: if None not save png, but use image to process only
    """
    zoom_x, zoom_y = scale
    mat = fitz.Matrix(zoom_x, zoom_y)  
    
    is_local, pth_form = check_is_local(pdf_input)
    if is_local and pth_form == "local":
        doc = fitz.open(pdf_input)  # open document_
    elif (not is_local) and pth_form == "url":
        request = requests.get(pdf_input)
        filestream = io.BytesIO(request.content)
        doc = fitz.open(stream=filestream, filetype="pdf")
    else:
        print("[INFO] CAN'T FIND DOCUMENT, ERROR ON FILE PATH OR URL")
    page_num = doc.page_count
    print(f"[INFO] NUMNER OF PAGE : {page_num}")

    images_list = []
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat, dpi=300)  # render page to an image
        pix = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pix = np.array(pix)
        image = (rgb2gray(pix)*255).astype(np.uint8)
        images_list.append(image)
        if png_name is not None: pix.save(f"x.png")
        
    return images_list


def image_to_base64_string(numpy_image):
    """
    function: find bbox for tabular format image
        <arg> pad_width: int/number to pad
    """
    PIL_image = Image.fromarray(np.uint8(numpy_image))
    buffered = io.BytesIO()
    PIL_image.save(buffered, format="png")
    b64string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return b64string