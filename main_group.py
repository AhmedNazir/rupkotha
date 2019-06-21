from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber
from Finish import finish, filterData

import threading
import time


def main():

    file = 'sample.pdf'

    project_number = 6
    projectName = 'project' + str(project_number).zfill(3)

    # clear combined OCR file .........
    clear(projectName)

    # spliting PDF .........
    split(path=file, projectName=projectName)

    total_page = getPageNumber(file)

    # Starting and Ending page number.....
    start = 25
    stop = 50

    if start > total_page or stop > total_page or start > stop:
        if start > stop:
            print('please check starting and ending page number !!!')
        else:
            print('out of pages!!!')
        exit(0)


    worker = 7 # max = 10
    service = []
    for i in range(worker):
        service.append(getService(ID=i))

    t = time.time()
    for i in range(start, stop+1, worker):

        pdf = []
        for j in range(worker):
            temp = projectName+str(i+j).zfill(3)+'.pdf'
            pdf.append(temp)

        th = []
        for j in range(worker):
            temp = threading.Thread( target=ocr, args=(service[j], pdf[j], projectName,))
            th.append(temp)

        for j in range(worker):
            th[j].start()

        for j in range(worker):
            th[j].join()

        print(f"done in : {time.time()-t}\n")

    # combinding all output....
    finish(projectName)

    filterData(projectName)
    


main()
