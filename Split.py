from pikepdf import Pdf
import os
import subprocess,time


def splitPDF(pdf_path='', book="", password=""):
    pdf = Pdf.open(pdf_path, password='')
    path = 'book' + '//' + book + '//'

    n = 1
    for page in pdf.pages:
        dst = Pdf.new()
        dst.pages.append(page)
        dst.save(path + '/input/' + str(1000 + n)+'.pdf')
        n = n + 1

    pdf.save(path + book + '.pdf')

    print("\nsplit DONE!!!")


def splitImage(pdfname='', book=""):
    outputPath = os.getcwd()+'\\book\\'+book+'\\images\\'
    PDFTOPPMPATH = "E:\\Software\\poppler\\poppler-0.68.0\\bin\\pdftoppm.exe"
    PDFFILE = os.getcwd()+'\\'+pdfname
    subprocess.Popen(f'{PDFTOPPMPATH} -png {PDFFILE} {outputPath}')

def isImageConversionCompleted(bookName):
    i = 0
    while True:
        pages = os.listdir('book'+'//'+bookName+'//'+'input')
        images = os.listdir('book'+'//'+bookName+'//'+'images')
        if len(pages) == len(images):
            return
        else:
            i=i+1
            print(f"Image Convertion is not completed  waited {5*i} seconds")
            time.sleep(5)

def renamePage(bookName):
    isImageConversionCompleted(bookName)

    pages = os.listdir('book'+'//'+bookName+'//'+'images')
    for page in pages:
        newName = 1000 + int(page[1:-4])
        newName=str(newName)+'.png'
        old_file = os.path.join('book'+'//'+bookName+'//'+'images',page)
        new_file = os.path.join('book'+'//'+bookName+'//'+'images', newName)
        os.rename(old_file, new_file)


def getPageNumber(pdfname):
    pdf = Pdf.open(pdfname, password='')
    return len(pdf.pages)


def split(path='', book="", password=""):
    if path[-3:].lower() == 'pdf':
        splitPDF(path, book, password)

