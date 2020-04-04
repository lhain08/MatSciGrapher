from tkinter import *
from tkinter import ttk
import tkinter as tk
import DataManip
import webcolors
import inspect
import Functions
import FileIO


'''
Takes the window object and appends a new tab to the notebook
New tab holds load/store options including directory for selecting data
'''
def buildDir(window):
    parent = Frame(window.nb)
    window.nb.add(parent, text="Load/Save")

    ### Header and Buttons ###
    Label(parent, text="Select Data", font='Helvetica 15 bold').pack(side='top')
    Button(parent, command=lambda: window.widgets['tree'].delete(*window.widgets['tree'].get_children()),\
           text="Clear Directories").pack(side='top')
    select_call = lambda: window.error(7)\
        if FileIO.populate_tree(window.widgets['tree'], tk.filedialog.askdirectory(parent=window.root)) else False
    Button(parent, command=select_call, text="Select Directory").pack(side='top')

    ### Directory Tree ###
    # Create tree
    window.widgets['tree'] = ttk.Treeview(parent, selectmode='browse')
    window.widgets['tree'].pack()

    # Populate tree
    tk.messagebox.showinfo(title="Open Data", message="Please select a directory for your data")
    dir = tk.filedialog.askdirectory(parent=window.root)
    FileIO.populate_tree(window.widgets['tree'], dir)

    # Add load data button
    Button(parent, command=lambda: window.open_folder(window.widgets['tree'].focus()),\
           text="Open Selected Data").pack(side='top')


'''
Takes the window object and appends a new tab to the notebook
New tab contains graph zoom and fit options
'''
def buildFit(window):
    parent = Frame(window.nb)
    window.nb.add(parent, "Auto-Fit")
