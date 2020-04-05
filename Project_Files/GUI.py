from tkinter import *
from tkinter import ttk
import tkinter as tk
import DataManip as dm
import webcolors
import inspect
import Functions
import FileIO

# Returns a list of all the available functions in Functions.py
def get_funcs():
    options = []
    for f in dir(Functions):
        if type(getattr(Functions, f)).__name__ == "function":
            options.append(f)
    return options

'''
Takes the window object and appends a new tab to the notebook
New tab holds load/store options including directory for selecting data
'''
def buildDir(window):
    # Prompt for a directory
    tk.messagebox.showinfo(title="Open Data", message="Please select a directory for your data")
    dir = tk.filedialog.askdirectory(parent=window.root)

    # Initiate the parent tab
    parent = Frame(window.nb)
    window.nb.add(parent, text="Load/Save")

    ### Header and Buttons ###
    Label(parent, text="Select Data", font='Helvetica 15 bold').pack(side='top')
    Button(parent, command=lambda: window.widgets['tree'].delete(*window.widgets['tree'].get_children()),\
           text="Clear Directories", takefocus=NO).pack(side='top')
    select_call = lambda: window.error(7)\
        if FileIO.populate_tree(window.widgets['tree'], tk.filedialog.askdirectory(parent=window.root)) else False
    Button(parent, command=select_call, text="Select Directory", takefocus=NO).pack(side='top')

    ### Directory Tree ###
    # Create tree
    tFrame = Frame(parent)
    tFrame.pack(side='top', expand=False)
    window.widgets['tree'] = ttk.Treeview(tFrame, selectmode='browse')
    window.widgets['tree'].column("#0", stretch=YES)
    window.widgets['tree'].heading("#0", text="Directory")
    window.widgets['tree'].pack(side='top', fill=BOTH, expand='yes')

    # Populate tree
    FileIO.populate_tree(window.widgets['tree'], dir)

    # Add load data button
    Button(parent, command=lambda: window.open_folder(window.widgets['tree'].focus()),\
           text="Open Selected Data", takefocus=NO).pack(side='top')


'''
Takes the window object and appends a new tab to the notebook
New tab contains graph zoom and fit options
'''
def buildFit(window):
    parent = Frame(window.nb)
    window.nb.add(parent, text="Auto-Fit")
    sub_frame = Frame(parent)
    sub_frame.pack(side='top')

    # Create the header
    header_text = Label(sub_frame, text="Automatic Zoom and Fit", font='Helvetica 15 bold')
    header_text.grid(row=0, columnspan=3, sticky="n")
    ttk.Separator(sub_frame, orient=HORIZONTAL).grid(pady=10, column=0, row=1, columnspan=3, sticky='ew')

    # Get the function list
    options = get_funcs()

    # Create Loading label and buttons
    Button(sub_frame, text="Loading", command=window.zoom_loading, width=9, takefocus=NO).grid(row=2, column=0)
    window.vars['load choice'] = StringVar(sub_frame)
    window.vars['load choice'].set("Loading")
    menu = OptionMenu(sub_frame, window.vars['load choice'], *options)
    menu.config(width=8)
    menu.grid(row=2, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'LOAD'), takefocus=NO).grid(row=2, column=2)

    # Create Holding label and buttons
    Button(sub_frame, text="Holding", command=window.zoom_holding, width=9, takefocus=NO).grid(row=3, column=0)
    window.hold_choice = StringVar(sub_frame)
    window.hold_choice.set("Holding")
    menu = OptionMenu(sub_frame, window.hold_choice, *options)
    menu.config(width=8)
    menu.grid(row=3, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'HOLD'), takefocus=NO).grid(row=3, column=2)

    # Create Unloading label and buttons
    Button(sub_frame, text="Unloading", command=window.zoom_unloading, width=9, takefocus=NO).grid(row=4, column=0)
    window.unload_choice = StringVar(sub_frame)
    window.unload_choice.set(options[0])
    menu = OptionMenu(sub_frame, window.unload_choice, *options)
    menu.config(width=8)
    menu.grid(row=4, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'UNLOAD'), takefocus=NO).grid(row=4, column=2)


def buildSets(window):
    parent = Frame(window.nb)
    window.nb.add(parent, text="Select Sets")

    # Headers
    Label(parent, text="Choose sets to be displayed", font="Helvetica 15 bold").pack(side='top')

    # Build the container for checkboxes
    window.widgets['check frame'] = Frame(parent)
    window.widgets['check frame'].pack(side='top')
    # Add some temporary text as a placeholder
    Label(window.widgets['check frame'], text="No data has been loaded.").pack()
    Label(window.widgets['check frame'], text="You will be able to select which").pack()
    Label(window.widgets['check frame'], text="sets you want displayed here").pack()


# Takes a frame and color and adds a checkbox for a single set
def push_check(frame, color, intvar, i, cmd):
    color = webcolors.rgb_to_hex([int(x) for x in color])
    check_button = Checkbutton(frame, text="Set %d" % i, variable=intvar, command=cmd, fg=color, takefocus=NO)
    check_button.pack(side=TOP)
    check_button.select()
    return check_button