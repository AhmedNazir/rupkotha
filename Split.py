from pikepdf import Pdf
import os


def split(path='',name="",password=""):
    pdf = Pdf.open(path + '.pdf', password='')

    if not os.path.exists(name):
        os.makedirs(name)

    n = 1
    for page in pdf.pages:
        dst = Pdf.new()
        dst.pages.append(page)
        dst.save(name + '/' +name+ '{:03d}.pdf'.format(n))
        n = n + 1

    pdf.save(name + '/' + name + '.pdf')

    # print("success !!!" +str(len(pdf.pages)))
    # print("SPLIT  success !!!")
    return n-1



