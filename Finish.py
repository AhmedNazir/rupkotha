def finish(project =''):
    
    with open(project+'//'+project+'.txt',encoding='utf-8') as fr:
        data = fr.read()
        data = data.replace('া ে','ো')
        data = data.replace('|','')
        # data = data.replace('﻿________________','') 

        with open(project+'//'+project+'filter.txt','w',encoding='utf-8') as fw:
            for line in data.split('\n') :
                fw.write(line.strip())
                fw.write('\n')

    with open(project+'//'+project+'filter.txt',encoding='utf-8') as fr:
        with open(project+'//'+project+'.html','w',encoding='utf-8') as fw:
            for line in fr.readlines():
                if line != '\n':
                    # fw.write('<p>'+line+'</p>\n<br/>\n')

                    if line[-2] in '।?"”': # line[-1] == '\n'
                        fw.write(line+'</p>\n<br/>\n'+'<p>')
                    else:
                        fw.write(line)

def clear(project = ''):
    open(project+'//'+project+'.txt','w',encoding='utf-8').close()
    open(project+'//'+project+'_filter.txt','w',encoding='utf-8').close()
    open(project+'//'+project+'.html','w',encoding='utf-8').close()

