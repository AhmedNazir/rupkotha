import os
from Ocr import ocr
from database import database
from time import sleep
import sys


def check(totalPage, service, projectName):
    while True:
        input = os.listdir(projectName+'//'+'input')
        output = os.listdir(projectName+'//'+'output')

        if totalPage == len(output):
            print("fully checked!!!")
            return True

        for pdf in input:
            out = pdf[:-4]
            if out+'.txt' not in output:
                ocr(service, pdf, projectName)


def finish(project=''):

    data = ''
    list = os.listdir(project+"//output//")
    for path in list:
        file = open(project+"//output//"+path, encoding='utf-8')
        data = data + file.read()
        file.close()

    with open(project+'//'+project+'.txt', 'w', encoding='utf-8') as fw:
        fw.write(data)

    data = filter(data)
    with open(project+'//'+project+'_filter.txt', 'w', encoding='utf-8') as fw:
        for line in data.split('\n'):
            fw.write(line.strip())
            fw.write('\n')

    with open(project+'//'+project+'_filter.txt', encoding='utf-8') as fr:
        with open(project+'//'+project+'.html', 'w', encoding='utf-8') as fw:
            fw.write('<p>')
            for line in fr.readlines():
                if line != '\n':

                    if line[-2] in '।!?"”':
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

    return data


def filterData(project=''):

    if not os.path.exists(project+'\\'+'filter'):
        os.makedirs(project+'\\'+'filter')

    data = ''
    list = os.listdir(project+"//output//")
    for path in list:
        fr = open(project+"//output//"+path, encoding='utf-8')
        fw = open(project+"//filter//"+path, 'w', encoding='utf-8')

        data = fr.read()
        for line in data.split('\n'):
            line = filter(line)
            line = line.strip()
            fw.write(line)

            try:
                if line[-1] in '।!?"”':
                    fw.write('\n')
                else:
                    fw.write(' ')
            except:
                fw.write('\n')

        fr.close()
        fw.close()
    print("Filter DONE!!!")


def store(projectName=''):
    db = database()

    output = os.listdir(projectName+'//'+'filter')

    i = 0
    for fileName in output:
        raw = open(projectName+'//'+'output'+'//' + fileName, encoding='utf-8').read()

        path = projectName+'//'+'filter'+'//' + fileName
        with open(path, encoding='utf-8') as f:
            txt = f.read()
            page = fileName[:-4]
            version = 1
            # final update
            db.child("book").child(projectName).child("final").child(page).update({
                "data": txt,
                "filter": txt,
                "raw": raw,
                "version": version,
                "volunteer": "rupkotha"
            })

            # history
            db.child("book").child(projectName).child("history").child(page).child(version).update({
                "data": txt,
                "volunteer": "rupkotha"
            })

        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*i, i))
        sys.stdout.flush()
        i = i+1
