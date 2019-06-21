from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber
from Finish import finish, filterData

import threading
import time



def workplace(service,pages, projectName):
    for page in pages:
        pdf = projectName+str(page).zfill(3)+'.pdf'

        # OCR function.....
        ocr(service, pdf, projectName)



def main():

    file = 'sample.pdf'

    project_number = 7
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

    t = time.time()
    q = []
    for i in range(worker):
        q.append(list(range(start+i,stop+1,worker)))

    service = []
    for i in range(worker):
        service.append(getService(ID=i))

    th = []
    for i in range(worker):
        temp = threading.Thread( target=workplace, args=(service[i], q[i], projectName,))
        th.append(temp)

    for i in range(worker):
        th[i].start()

    for i in range(worker):
        th[i].join()

    print(f"done in : {time.time()-t}\n")

    # combinding all output....
    finish(projectName)

    filterData(projectName)

main()
