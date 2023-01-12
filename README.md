# Pytesseract-Practice
## Quick Start (tesseract 5.2.0)
    from PIL import Image
    import pytesseract

    img_path = <local image path>
    text = pytesseract.image_to_string(Image.open(img_path))
    print(text)

## Install Tesseract
    $ sudo apt-get install libpng-dev libjpeg-dev libtiff-dev zlib1g-dev  
    $ sudo apt-get install gcc g++  
    $ sudo apt-get install autoconf automake libtool checkinstall 

## Need image processing toolkit Leptonica to build Tesseract.
    $ cd ~  
    $ wget http://www.leptonica.org/source/leptonica-1.73.tar.gz  
    $ tar -zxvf leptonica-1.73.tar.gz  
    $ cd leptonica-1.73  
    $ ./configure  
    $ make  
    $ sudo checkinstall  
    $ sudo ldconfig  

    $ sudo apt-get install tesseract-ocr  

## tesseract usage
    $ tesseract --help

## List available languages for tesseract engine
    $ tesseract --list-langs

## Install Thai package
    $ sudo apt-get install tesseract-ocr-tha

## Using Python and Tesserect
    $ pip install pytesseract

## Task Lists
- [x] Quick Start
- [ ] Guide to Fine-Tuning
- [ ] etc.
