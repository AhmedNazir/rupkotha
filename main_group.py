from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber,splitImage,renamePage
from Finish import finish, filterData, check, store,remove

import threading
import time


def main():

    file = 'Vol-30.pdf'

    bookID = 11

    bookName = str(10000+bookID)
    # clear combined OCR file .........
    clear(bookName)

    # spliting PDF .........
    split(file,bookName)
    splitImage(file,bookName)


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

    # '''
    worker = 10  # max = 10
    service = []
    for i in range(worker):
        service.append(getService(ID=i))

    t = time.time()
    for i in range(start, stop+1, worker):
        tt = time.time()
        pdf = []
        for j in range(worker):
            temp = str(1000 + j)+'.pdf'
            pdf.append(temp)

        th = []
        for j in range(worker):
            temp = threading.Thread(target=ocr, args=(
                service[j], pdf[j], bookName,))
            th.append(temp)

        for j in range(worker):
            th[j].start()

        for j in range(worker):
            th[j].join()
        print(f"\ndone in : {(time.time()-tt)/worker}\n")

    print(f"done in : {time.time()-t}\n")

    # '''

    # combinding all output....
    check(total_page, getService(), bookName)
    renamePage(bookName)
    finish(bookName)
    filterData(bookName)
    store(bookName,title,writer)
    remove(bookName)

title = "abc"
writer = "xyz"
main()
