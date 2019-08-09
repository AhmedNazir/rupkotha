from init import getService, clear
from Ocr import ocr
from Split import split, getPageNumber,splitImage,renamePage
from Finish import finish, filterData, check, store,remove,storeLinear
import threading
import time


def workplace(service, pages, bookName):
    for page in pages:
        pdf = str(1000 + page)+'.pdf'

        # OCR function.....
        ocr(service, pdf, bookName)


def main(file='', bookID=0):
    bookName = str(10000 + bookID)

    # clear combined OCR file .........
    clear(bookName)

    # spliting PDF .........
    split(file, bookName)
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

    t = time.time()
    q = []
    for i in range(worker):
        q.append(list(range(start+i, stop+1, worker)))

    service = []
    for i in range(worker):
        service.append(getService(ID=i))

    th = []
    for i in range(worker):
        temp = threading.Thread(target=workplace, args=(
            service[i], q[i], bookName,))
        th.append(temp)

    for i in range(worker):
        th[i].start()

    for i in range(worker):
        th[i].join()

    print(f"done in : {time.time()-t}\n")

    # '''

    # combinding all output....
    check(total_page, getService(), bookName)
    finish(bookName)
    renamePage(bookName)
    filterData(bookName)
    store(bookName,title,writer)
    remove('book\\'+bookName)

bookID = 3
file = 'sample.pdf'
title = "অ্যাডভেঞ্চার সমগ্র"
writer = "হিমাদ্রি কিশোর দাশগুপ্ত"


main(file, bookID)