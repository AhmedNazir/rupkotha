from init import getService, clear
from Ocr import ocr
from Split import split,splitImage, getPageNumber,renamePage
from Finish import finish, filterData, check, store,remove,storeLinear

import threading
import time


def main():

    bookID = 5
    file = 'Vol-65.pdf'
    title = "Tin Goyenda"
    writer = "Rokib Hasan, Samsuddin Nawab"
    bookName = str(10000+bookID)

    # clear combined OCR file .........
    clear(bookName)

    # spliting PDF .........
    # split(file, bookName)
    # splitImage(file,bookName)

    total_page = getPageNumber(file)
    print('total Pages : ' + str(total_page)+'\n')

    # Starting and Ending page number.....
    start = 1
    stop = total_page
    # stop = 10
    # '''
    if start > total_page or stop > total_page or start > stop:
        if start > stop:
            print('please check starting and ending page number !!!')
        else:
            print('out of pages!!!')
        exit(0)

    t = time.time()
    service = getService()

    for i in range(start, stop+1):
        pdf = str(1000 + i)+'.pdf'

        # OCR function.....
        # ocr(service, pdf, bookName)

    print(f"done in : {time.time()-t}\n")



    # check(total_page, getService(), bookName)
    # '''
    finish(bookName)
    filterData(bookName)
    # renamePage(bookName)
    # store(bookName,title,writer)
    storeLinear(bookName,title,writer)
    # remove(bookName)

main()
