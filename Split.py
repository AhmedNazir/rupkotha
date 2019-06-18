from pikepdf import Pdf
import os


def splitPDF(path='', projectName="", password=""):
    pdf = Pdf.open(path, password='')

    if not os.path.exists(projectName):
        os.makedirs(projectName)
    if not os.path.exists(projectName+'\\'+'output'):
        os.makedirs(projectName+'\\'+'output')
    if not os.path.exists(projectName+'\\'+'input'):
        os.makedirs(projectName+'\\'+'input')

    n = 1
    for page in pdf.pages:
        dst = Pdf.new()
        dst.pages.append(page)
        dst.save(projectName + '/input/' +  projectName + '{:03d}.pdf'.format(n))
        n = n + 1

    pdf.save(projectName + '/' + projectName + '.pdf')

def splitImage(path='', projectName="", password=""):
    print('Image Splitter Coming Soon... ')


def getPageNumber(path):
    pdf = Pdf.open(path, password='')
    return len(pdf.pages)


def split(path='', projectName="", password=""):
    if path[-3:].lower() == 'pdf':
        splitPDF(path, projectName, password)

    if path[-3:].lower() in ['jpg', 'png', 'bmp', 'gif']:
        splitImage(path, projectName, password)

    if path[-4:].lower() in ['jpeg']:
        splitImage(path, projectName, password)
