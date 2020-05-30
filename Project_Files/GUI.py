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

    ### SAVE ###
    ttk.Separator(parent, orient=HORIZONTAL).pack(pady=10, fill='x', anchor='ne')
    Label(parent, text="Save Data", font="Helvetica 15 bold").pack(side=TOP)

    # Save plot button
    Button(parent, text="Save Plot", command=window.save_as, width=20).pack(side=TOP)


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
    Button(sub_frame, text="Loading", command=window.zoom_loading, width=9, takefocus=NO).grid(row=3, column=0)
    window.vars['load choice'] = StringVar(sub_frame)
    window.vars['load choice'].set("Loading")
    menu = OptionMenu(sub_frame, window.vars['load choice'], *options)
    menu.config(width=8)
    menu.grid(row=3, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'LOAD'), takefocus=NO).grid(row=3, column=2)

    # Create Holding label and buttons
    Button(sub_frame, text="Holding", command=window.zoom_holding, width=9, takefocus=NO).grid(row=4, column=0)
    window.vars['hold choice'] = StringVar(sub_frame)
    window.vars['hold choice'].set("Holding")
    menu = OptionMenu(sub_frame, window.vars['hold choice'], *options)
    menu.config(width=8)
    menu.grid(row=4, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'HOLD'), takefocus=NO).grid(row=4, column=2)

    # Create Unloading label and buttons
    Button(sub_frame, text="Unloading", command=window.zoom_unloading, width=9, takefocus=NO).grid(row=5, column=0)
    window.unload_choice = StringVar(sub_frame)
    window.unload_choice.set(options[0])
    menu = OptionMenu(sub_frame, window.unload_choice, *options)
    menu.config(width=8)
    menu.grid(row=5, column=1)
    Button(sub_frame, text="Fit", command=lambda: dm.autoFit(window, 'UNLOAD'), takefocus=NO).grid(row=5, column=2)

    # Create Set Selection menu
    window.vars['set choice'] = StringVar(parent)
    window.vars['set choice'].set("-Select Set for Fit-")
    options = {"-Select Set for Fit-"}
    window.widgets['menu'] = OptionMenu(sub_frame, window.vars['set choice'], *options)
    window.widgets['menu'].grid(row=2, column=0, columnspan=3, sticky="ew")
    window.widgets['menu'].items = []

    # Manual Zoom option
    Label(parent, text="Zoom to Range", font="Helvetica 15 bold").pack(side=TOP)
    # Configure wrapper
    wrap = Frame(parent)
    wrap.pack(side=TOP, fill='x')
    wrap.grid_columnconfigure(0, weight=1, uniform="zoom")
    wrap.grid_columnconfigure(1, weight=1, uniform="zoom")
    # Build the Entries
    c = parent.register(dm.validate_float)
    frame = LabelFrame(wrap, text="Upper")
    upper = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    upper.pack(fill='x')
    frame.grid(row=0, column=1, sticky='ew')
    window.widgets['upper zoom'] = upper

    frame = LabelFrame(wrap, text="Lower")
    lower = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    lower.pack(fill='x')
    frame.grid(row=0, column=0, sticky='ew')
    window.widgets['lower zoom'] = lower
    # Zoom Button
    Button(parent, text="Zoom", command=window.zoom_range).pack(side=TOP, fill='x')
    # Toggle Fit Range choice
    window.fit_choice = Button(parent, text="Fit to Default", command=window.toggle_fit)
    window.fit_choice.pack(side=TOP, fill='x')
    window.vars['fit choice'] = 'Fit to Default'


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


'''
Takes the window object and creates the tab for displaying results
'''
def buildResults(window):
    # Initiate the parent tab
    parent = Frame(window.nb)
    window.nb.add(parent, text="Results")

    # Header text
    Label(parent, text="All Fit Results", font="Helvetica 15 bold").pack(side=TOP)

    # Text Box for result history
    window.widgets['history'] = tk.Text(parent, width=parent.winfo_width(), state='disabled')
    window.widgets['history'].pack(side=TOP, expand=True, fill='both', anchor='nw')
    window.widgets['history'].tag_configure("bold", font="Helvetica 12 bold")


'''
Takes window object, parameter values, function object, and R^2 value
Inserts the results of the fit using the given equation into the history log
'''
def insert_results(window, params, eq, r_squared):
    # Insert header for history log
    window.widgets['history'].configure(state='normal')
    buffer = "Fit of Set %d with equation %s\n" % \
             (int(window.vars['set choice'].get().strip("Set ")), eq.__name__)
    window.widgets['history'].insert("end", buffer, "bold")

    # Insert r_squared at the top of the list
    window.widgets['history'].insert("end", "R^2: ", "bold")
    window.widgets['history'].insert("end", "{0}\n".format(r_squared))

    # Fill with rest of results
    param_names = inspect.getfullargspec(eq).args[1:]
    for i in range(len(params)):
        window.widgets['history'].insert("end", param_names[i] + ': ', "bold")
        window.widgets['history'].insert("end", str(params[i]) + '\n')
    window.widgets['history'].insert("end", '\n')
    window.cur_eq = eq
    window.result_params = params

    # Lock history log so user cannot edit results
    window.widgets['history'].configure(state='disabled')


def buildManual(window):
    # Create the tab
    parent = Frame(window.nb)
    window.nb.add(parent, text="Manual Plot")
    # Create a header
    Label(parent, text="Select a Function", font="Helvetica 15 bold").pack(side=TOP)

    # Create dropdown to select equation
    options = FileIO.get_funcs()
    window.vars['manual function'] = StringVar(parent)
    window.vars['manual function'].set(options[0])
    window.vars['manual function'].trace('w', lambda *args: window.func_select_callback())
    menu = OptionMenu(parent, window.vars['manual function'], *options)
    menu.pack(side=TOP, fill='x')

    # Create wrapper frame for holding parameter entry boxes
    window.widgets['manual params'] = Frame(parent)
    window.widgets['manual params'].pack(side=TOP)
    set_params_menu(window)

    # Copy paramaters button
    Button(parent, text="Copy Last Fit Results", command=window.copy_results).pack(side=TOP, fill='x')

    ### Bounds Entries ###
    # Header
    Label(parent, text="Enter Bounds for plot", font="Helvetica 15 bold").pack(side=TOP)
    # Configure wrapper
    wrap = Frame(parent)
    wrap.pack(side=TOP, fill='x')
    wrap.grid_columnconfigure(0, weight=1, uniform="bounds")
    wrap.grid_columnconfigure(1, weight=1, uniform="bounds")
    # Build the Entries
    c = parent.register(dm.validate_float)
    frame = LabelFrame(wrap, text="Upper")
    upper = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    upper.pack(fill='x')
    frame.grid(row=0, column=1, sticky='ew')
    window.widgets['upper entry'] = upper

    frame = LabelFrame(wrap, text="Lower")
    lower = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    lower.pack(fill='x')
    frame.grid(row=0, column=0, sticky='ew')
    window.widgets['lower entry'] = lower

    # Quick set buttons
    wrap = Frame(parent)
    wrap.pack(side=TOP, fill='x')
    for i in range(3):
        wrap.grid_columnconfigure(i, weight=1, uniform='quickset')
    Button(wrap, text='Load', command=lambda: window.set_range('LOAD')).grid(row=0, column=0, sticky='ew')
    Button(wrap, text='Hold', command=lambda: window.set_range('HOLD')).grid(row=0, column=1, sticky='ew')
    Button(wrap, text='Unload', command=lambda: window.set_range('UNLOAD')).grid(row=0, column=2, sticky='ew')

    # Buttons
    ttk.Separator(parent, orient=HORIZONTAL).pack(side=TOP, pady=10, fill='x', anchor='ne')
    Button(parent, text='Plot Function', command=lambda: dm.Manual_fit(window)).pack(side=TOP, fill='x')
    Button(parent, text='Clear All Fits', command=window.clear_fits).pack(side=TOP, fill='x')


# Populates the manual plot tab with parameter entry boxes
def set_params_menu(window):
    # Erases any previous parameters
    for child in window.widgets['manual params'].winfo_children():
        child.destroy()
    # Create a header
    header_text = Label(window.widgets['manual params'], text="Enter Parameters", font='Helvetica 15 bold')
    header_text.pack(side=TOP)

    # Get the parameter list
    functionObj = getattr(Functions, window.vars['manual function'].get())
    params = inspect.getfullargspec(functionObj).args
    c = window.widgets['manual params'].register(dm.validate_float)        # To allow entries to only take floats
    # Pack the labels and entries
    window.widgets['manual entries'] = []
    for p in params:
        if p.lower() != 'time':
            small_frame = Frame(window.widgets['manual params'])
            Label(small_frame, text=p + ": ").pack(side=LEFT)
            ent = Entry(small_frame, validate="key", vcmd=(c, '%P'))
            ent.pack(side=RIGHT)
            window.widgets['manual entries'].append(ent)
            small_frame.pack(side=TOP, anchor="e")