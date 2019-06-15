from Ocr import ocr
from Split import split
from Finish import finish,clear

def main():

    file= 'sample'
    project_number = 1
    pdfname= 'project' + str(project_number).zfill(3)

    # clear(pdfname) # clear ...............

    total_page = split(path =file,name=pdfname)

    start = 1
    stop =5 # total_page

    folder = pdfname+'\\'
    for i in range(start,stop):
        name =pdfname+str(i).zfill(3)+'.pdf'
        # ocr(name,folder,pdfname)

    finish(pdfname)

main()