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
                        fw.write(line[:-1]+'</p>\n<br/>\n'+'<p>')   # line[-1] = '\n'
                    else:
                        fw.write(line)


def filter(data):
    data = data.replace('াে', 'ো')
    data = data.replace('|', '')
    data = data.replace('।।', '।')
    data = data.replace('েে', 'ে')

    return data