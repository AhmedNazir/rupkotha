from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber
from Finish import finish, filterData

import threading
import time


def main():

    file = 'sample.pdf'

    project_number = 5
    projectName = 'project' + str(project_number).zfill(3)

    # clear combined OCR file .........
    clear(projectName)

    # spliting PDF .........
    split(path=file, projectName=projectName)

    total_page = getPageNumber(file)

    # Starting and Ending page number.....
    start = 24
    stop = total_page

    if start > total_page or stop > total_page or start > stop:
        if start > stop:
            print('please check starting and ending page number !!!')
        else:
            print('out of pages!!!')
        exit(0)

    #.................

    
    worker = 8 # max = 8
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

    #.........................
    '''
    service = getService()
    for i in range(start, stop+1):
        pdf = projectName+str(i).zfill(3)+'.pdf'

        # OCR function.....
        # ocr(service, pdf, projectName)
    
    '''
    # combinding all output....
    finish(projectName)

    filterData(projectName)
    


main()
