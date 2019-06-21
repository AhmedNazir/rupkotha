import os


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
                        fw.write(line[:-1]+'</p>\n<br/>\n' + '<p>')   # line[-1] = '\n'
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
                else: fw.write(' ')
            except:
                fw.write('\n')

        fr.close()
        fw.close()
    print("Filter DONE!!!")
