# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 22:06:58 2018

@author: amrul
"""

from tkinter import *


def command_00(txt):
    print('The text is:%s'%(txt))
    pass

root=Tk()
label=Label(root,text='Date')
entry=Entry(root,width=50)
button=Button(root,text='Press',command=lambda:command_00(entry.get()))

var='Select Country'
optmenu=OptionMenu(root,var,'US','UK')
label.pack()
button.pack()    
entry.pack()
optmenu.pack()
root.mainloop()