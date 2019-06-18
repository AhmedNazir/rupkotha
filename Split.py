from pikepdf import Pdf
import os


def split(path='',projectName="",password=""):
    pdf = Pdf.open(path + '.pdf', password='')

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
        dst.save(projectName + '/input/' +projectName+ '{:03d}.pdf'.format(n))
        n = n + 1

    pdf.save(projectName + '/' + projectName + '.pdf')

def getPageNumber(path):
    pdf = Pdf.open(path + '.pdf', password='')
    return len(pdf.pages)




