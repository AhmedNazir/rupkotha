from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber
from Finish import finish, filterData, check, store

import threading
import time


def main():

    file = 'sample.pdf'

    project_number = 1
    projectName = 'project' + str(project_number).zfill(3)

    # clear combined OCR file .........
    clear(projectName)

    # spliting PDF .........
    split(path=file, projectName=projectName)

    total_page = getPageNumber(file)

    # Starting and Ending page number.....
    start = 1
    stop = total_page

    if start > total_page or stop > total_page or start > stop:
        if start > stop:
            print('please check starting and ending page number !!!')
        else:
            print('out of pages!!!')
        exit(0)

    t = time.time()
    service = getService()

    for i in range(start, stop+1):
        pdf = projectName+str(i).zfill(3)+'.pdf'

        # OCR function.....
        ocr(service, pdf, projectName)

    print(f"done in : {time.time()-t}\n")

    check(total_page, getService(), projectName)
    finish(projectName)
    filterData(projectName)
    store(projectName)


main()
