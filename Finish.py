import os
from Ocr import ocr
from database import database, getStorage
from time import sleep, time
import sys
import threading
import shutil


def check(totalPage, service, bookName):
    while True:
        input = os.listdir('book'+'\\'+bookName+'\\'+'input')
        output = os.listdir('book'+'\\'+bookName+'\\'+'output')

        if totalPage == len(output):
            print("fully checked!!!")
            return True

        for page in input:
            out = page[:-4]
            if out+'.txt' not in output:
                ocr(service, page, bookName)


def finish(bookName):
    path = 'book\\'+bookName
    data = ''
    pages = os.listdir(path+"\\output\\")

    for page in pages:
        file = open(path+"\\output\\"+page, encoding='utf-8')
        data = data + file.read()
        file.close()

    with open(path+'\\' + bookName + '_raw.txt', 'w', encoding='utf-8') as fw:
        fw.write(data)

    data = filter(data)
    with open(path+'\\' + bookName+'.txt', 'w', encoding='utf-8') as fw:
        for line in data.split('\n'):
            fw.write(line.strip())
            fw.write('\n')

    with open(path+'\\'+bookName+'.txt', encoding='utf-8') as fr:
        with open(path+'\\'+bookName+'.html', 'w', encoding='utf-8') as fw:
            fw.write('<p>')
            for line in fr.readlines():
                if line != '\n':

                    if line[-2] in '।!?"”’\'':
                        # line[-1] = '\n'
                        fw.write(line[:-1]+'</p>\n<br/>\n' '<p>')
                    else:
                        fw.write(line)
            fw.write('</p>')

    print("Combinding DONE!!!")


def filter(data):
    data = data.replace('াে', 'ো')
    data = data.replace('|', '')
    data = data.replace('।।', '।')
    data = data.replace('োে', 'ো')
    data = data.replace('ঁা', 'াঁ')

    return data


def filterData(bookName=''):

    path = 'book'+'\\' + bookName
    if not os.path.exists(path+'\\'+'filter'):
        os.makedirs(path+'\\'+'filter')

    data = ''
    pages = os.listdir(path+"\\output\\")
    for page in pages:
        fr = open(path+"\\output\\"+page, encoding='utf-8')
        fw = open(path+"\\filter\\"+page, 'w', encoding='utf-8')

        data = fr.read()
        for line in data.split('\n'):
            line = filter(line)
            line = line.strip()
            fw.write(line)

            try:
                if line[-1] in '।!?"”’\'':
                    fw.write('\n')
                else:
                    fw.write(' ')
            except:
                fw.write('\n')

        fr.close()
        fw.close()
    print("Filter DONE!!!")


def savePage(bookName, db, store, totalPages, fileName):
    filetype = '.png'
    raw = ''
    with open('book'+'\\'+bookName+'\\'+'output'+'\\' + fileName, encoding='utf-8') as fr:
        raw = fr.read()

    path = 'book'+'\\'+bookName+'\\'+'filter'+'\\' + fileName
    with open(path, encoding='utf-8') as f:
        txt = f.read()
        page = fileName[:-4]
        version = 1
        volunteer = 'rupkotha'

        file = store.child("images/book/"+bookName+'/'+page + filetype).put(
            'book'+'/'+bookName+'/'+'images'+'/' + page + filetype)
        image = store.child("images/book/"+bookName+'/' +
                            page + filetype).get_url(file['downloadTokens'])

        # final update
        db.child("book").child(bookName).child("pages").child(page).update({
            "text": txt,
            "filter": txt,
            "raw": raw,
            "version": version,
            "volunteer": volunteer,
            'proof': False,
            'format': False,
            'image': image,

            # 'todo' : {
            #     "1":{
            #         "task" : "proof",
            #         "done" : False,
            #     },
            #     '2':{
            #         "task" : "format",
            #         "done":False,
            #     }
            # },
            #
            # "chat" : {
            #     "1":{
            #         "message":"hello",
            #         "sender":"rupkotha",
            #         "time": time.time(),
            #     }
            # },
        })

        # history
        db.child("book").child(bookName).child("history").child(page).child(version).update({
            "text": txt,
            "volunteer": "rupkotha"
        })

        print(fileName)


def storeLinear(bookName, title, writer):
    output = os.listdir('book'+'\\'+bookName+'\\'+'filter\\')
    totalPages = len(output)

    pages = list(range(1, totalPages+1))
    workplace(bookName, pages, database(), getStorage(), totalPages)


def workplace(bookName, pages, db, store, totalPages):
    for page in pages:
        fileName = str(1000 + page)+'.txt'
        savePage(bookName, db, store, totalPages, fileName)


def store(bookName, title, writer):

    output = os.listdir('book'+'\\'+bookName+'\\'+'filter\\')
    totalPages = len(output)

    # worker...
    worker = 5
    store = []
    db = []
    for i in range(worker):
        store.append(getStorage())
        db.append(database())

    q = []
    for i in range(worker):
        q.append(list(range(1+i, totalPages+1, worker)))

    th = []
    for i in range(worker):
        temp = threading.Thread(target=workplace, args=(
            bookName, q[i], db[i], store[i], totalPages))
        th.append(temp)

    for i in range(worker):
        th[i].start()

    for i in range(worker):
        th[i].join()

    txt = ''
    html = ''
    with open("book"+"//"+bookName+'//'+bookName+'.txt', encoding='utf-8') as fr:
        txt = fr.read()

    with open("book"+"//"+bookName+'//'+bookName+'.html', encoding='utf-8') as fr:
        html = fr.read()

    format = [False, ]
    proof = [False, ]

    for _ in range(totalPages):
        proof.append(False)
        format.append(False)

    db[0].child("book").child(bookName).child("combine").update({
        # 'text': txt,
        # 'html': html,
        "pages": totalPages,
        "proof": proof,
        "format": format,
        "writer": writer,
        "title": title,
    })

    db[0].child("book").child(bookName).child("dump").update({
        'text': txt,
        'html': html,
    })


    checkDatabase(bookName, db[0], store[0])


def checkDatabase(bookName, db, store):
    output = os.listdir('book'+'\\'+bookName+'\\'+'filter\\')
    totalPages = len(output)
    pages = db.child('book').child(bookName).child('pages').get()

    count = 0
    for page in pages.each():
        count = count + 1

    print(f"{count}/{totalPages}")

    # while True:
    #     pages = db.child('book').child(bookName).child('pages').get()
    #     flag = True
    #     for page in pages.each():
    #         pageName = page.key()+'.txt'
    #         if pageName not in output:
    #             savePage(bookName, db, getStorage(), totalPages, pageName)
    #             flag = False

    #     if(flag):
    #         print("checked")
    #         return


def remove(bookName):
    shutil.rmtree(bookName, True)
