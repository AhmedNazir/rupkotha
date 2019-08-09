import tkinter as tk
from tkinter import ttk
import json
import pyrebase
from database import database 

bookID = 11

book = str(10000+bookID)
page ='240'
version = 1
i = 1
volunteer = ''
volunteer_new = 'Ahmed Nazir'

txt = ''

db = database()

def load(i):
    global book,page,version, volunteer,txt
    if i>0:
        p = str(1000 + i)
        page = db.child('book').child(book).child('pages').child(p).get().key()
        version = db.child('book').child(book).child('pages').child(p).child('version').get().val()
        volunteer = db.child('book').child(book).child('pages').child(p).child('volunteer').get().val()
        temp = db.child('book').child(book).child('pages').child(p).child('text').get().val()
        txt = ''
        for line in temp.split('\n'):
            if line != '':
                txt= txt + line.strip() +'\n\n'
    else:
        page = 'invalid page number'
        version = 'invalid'
        volunteer = 'invalid'
        txt = ''

    book_label.config(text = "book : " + book )
    page_label.config(text ='page : ' + page )
    version_label.config(text ='version : ' + str(version))
    vounteer_label.config(text ='volunteer : '+ volunteer )

    go_box.delete("1.0", tk.END)
    go_box.update()
    go_box.insert("1.0",i)

    box.delete("1.0", tk.END)
    box.update()
    box.insert("1.0",txt)


def update():
    global book,page,version, volunteer,i
    new = box.get("1.0",tk.END)
    version = version + 1

    db.child('book').child(book).child('pages').child(page).update({
        'text' : new,
        "version" : version,
        "volunteer" : volunteer_new
    })

    db.child('book').child(book).child('history').child(page).child( version).update({
        "text" : new,
        'volunteer' : volunteer_new
    })
    load(i)


def previous():
    global i
    i = i - 1
    load(i)

def next():
    global i
    i = i + 1
    load(i)

def go():
    global i
    i = int(go_box.get("1.0",tk.END))
    load(i)


def combine():
    global book
    pages = db.child('book').child(book).child('pages').get()
    l = pages.each()
    txt = ''
    for page in l:
        txt = txt + db.child('book').child(book).child('pages').child(page.key()).child('text').get().val()
        print(page.key())

    with open(book+".txt", 'w', encoding='utf-8') as f:
        f.write(txt)

    db.child('book').child(book).child('combine').update({
        'text' : txt,
        # 'html' : 'dummy'
    })



root = tk.Tk()
root.title('PROOF')
root.minsize(600,600)

book_label = ttk.Label(root)
book_label.grid(row=0, column=0, sticky=tk.W)
book_label.config(text = book,font=12)

page_label = ttk.Label(root)
page_label.grid(row=1, column=0, sticky=tk.W)
page_label.config(text = page,font=12)

version_label = ttk.Label(root)
version_label.grid(row=2, column=0, sticky=tk.W)
version_label.config(text = version,font=12)

vounteer_label = ttk.Label(root)
vounteer_label.grid(row=3, column=0, sticky=tk.W)
vounteer_label.config(text = volunteer,font=12)

go_box = tk.Text(root, width=7, height = 1, font= "serif 14", wrap = 'word')
go_box.grid(row=4, column=1, sticky=tk.W)
go_box.insert('1.0',str(i))

go_button = ttk.Button(root, text = 'go',command = go)
go_button.grid(row=4, column=2, sticky=tk.W)

box = tk.Text(root, width=60, height = 25, font= "serif 14", wrap = 'word')
box.grid(row=5, column=0, sticky=tk.W)
box.insert('1.0',txt)

upadate_button = ttk.Button(root, text = 'update',command = update)
upadate_button.grid(row=6, column=0, sticky=tk.W)

previous_button = ttk.Button(root, text = 'previous',command = previous)
previous_button.grid(row=6, column=1, sticky=tk.W)

next_button = ttk.Button(root, text = 'next',command = next)
next_button.grid(row=6, column=2, sticky=tk.W)


combine_button = ttk.Button(root, text = 'combine',command = combine)
combine_button.grid(row=6, column=4, sticky=tk.W)

load(i)

root.mainloop()