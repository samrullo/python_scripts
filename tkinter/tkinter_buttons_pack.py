# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 22:26:18 2018

@author: amrul
"""

from tkinter import *
root=Tk()
Button(root,text='ALL IS WELL').pack(side=TOP,expand=Y,fill=BOTH)
Button(root,text='BACK TO BASICS').pack(side=TOP,expand=Y,fill=BOTH)
Button(root,text='CATCH ME IF YOU CAN').pack(side=TOP,expand=Y,fill=BOTH)
Button(root,text='LEFT').pack(side=LEFT,expand=Y,fill=BOTH)
Button(root,text='CENTER').pack(side=LEFT,expand=Y,fill=BOTH)
Button(root,text='RIGHT').pack(side=RIGHT,expand=Y,fill=BOTH)
root.mainloop()