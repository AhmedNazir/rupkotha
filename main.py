from init import getService, clear
from Ocr import ocr
from Split import split,getPageNumber
from Finish import finish


def main():

    file = 'sample.pdf'
    project_number = 6
    projectName = 'project' + str(project_number).zfill(3)

    # clear combined OCR file .........
    clear(projectName)

    # spliting PDF .........
    split(path=file, projectName=projectName)

    # Starting and Ending page number.....
    start = 31
    stop = 35


    total_page = getPageNumber(file)
    if start > total_page or stop > total_page or start > stop:
        if start > stop:
            print('please check starting and ending page number !!!')
        else:
            print('out of pages!!!')
        exit(0)

    service = getService()
    for i in range(start, stop+1):
        pdf = projectName+str(i).zfill(3)+'.pdf'

        # OCR function.....
        ocr(service, pdf, projectName)

    # combinding all output....
    finish(projectName)

main()
