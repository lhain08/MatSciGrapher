from tkinter import *
from tkinter import ttk
import tkinter as tk
import DataManip
import webcolors
import inspect
import Functions


# Create the top frame for load/save/quit
def create_top(parent, load_cmd=None, save_cmd=None, quit_cmd=None):
    frame = Frame(parent, bg='White')

    # Create the buttons
    load_button = Button(frame, text="Load Data", command=load_cmd, width=15)
    load_button.pack(side=LEFT, padx=5)
    save_button = Button(frame, text="Save Plot", command=save_cmd, width=15)
    save_button.pack(side=LEFT, padx=5)
    quit_button = Button(frame, text="Quit", command=quit_cmd, width=15)
    quit_button.pack(side=LEFT, padx=5)

    return frame


# Creates the side frame for zooming and fitting sections
def create_zoom_and_fit(window, load_zoom_cmd=None, load_fit_cmd=None, hold_zoom_cmd=None, hold_fit_cmd=None,
                        unload_zoom_cmd=None, unload_fit_cmd=None, zoom_range_cmd=None, zoom_out_cmd=None,
                        clear_cmd=None):
    parent = window.nb
    # Create the frame
    border = Frame(parent, bd=3, relief=GROOVE)
    frame = Frame(border)

    # Create the header
    header_text = Label(frame, text="Automatic Zoom and Fit", font='Helvetica 11 bold')
    header_text.grid(row=0, columnspan=3, sticky="n")
    ttk.Separator(frame, orient=HORIZONTAL).grid(pady=10, column=0, row=1, columnspan=3, sticky='ew')

    # Get the function list
    options = get_funcs()

    # Create Loading label and buttons
    load_zoom = Button(frame, text="Loading", command=load_zoom_cmd, width=9)
    load_zoom.grid(row=2, column=0)
    window.load_choice = StringVar(frame)
    window.load_choice.set("Loading")
    menu = OptionMenu(frame, window.load_choice, *options)
    menu.config(width=8)
    menu.grid(row=2, column=1)
    load_fit = Button(frame, text="Fit", command=load_fit_cmd)
    if load_fit_cmd is None: load_fit['state'] = DISABLED
    load_fit.grid(row=2, column=2)

    # Create Holding label and buttons
    hold_zoom = Button(frame, text="Holding", command=hold_zoom_cmd, width=9)
    hold_zoom.grid(row=3, column=0)
    window.hold_choice = StringVar(frame)
    window.hold_choice.set("Holding")
    menu = OptionMenu(frame, window.hold_choice, *options)
    menu.config(width=8)
    menu.grid(row=3, column=1)
    hold_fit = Button(frame, text="Fit", command=hold_fit_cmd)
    if hold_fit_cmd is None: hold_fit['state'] = DISABLED
    hold_fit.grid(row=3, column=2)

    # Create Unloading label and buttons
    unload_zoom = Button(frame, text="Unloading", command=unload_zoom_cmd, width=9)
    unload_zoom.grid(row=4, column=0)
    window.unload_choice = StringVar(frame)
    window.unload_choice.set(options[0])
    menu = OptionMenu(frame, window.unload_choice, *options)
    menu.config(width=8)
    menu.grid(row=4, column=1)
    unload_fit = Button(frame, text="Fit", command=unload_fit_cmd)
    if unload_fit_cmd is None: unload_fit['state'] = DISABLED
    unload_fit.grid(row=4, column=2)

    # Zoom to range
    r_frame = Frame(frame)
    c = parent.register(DataManip.validate_float)
    Label(r_frame, text="Manual Zoom", font="Helvetica 11 bold").grid(row=0, column=0, columnspan=3)
    range_entries = (Entry(r_frame, width=10, validate="key", vcmd=(c, '%P')), Entry(r_frame, width=10))
    range_entries[0].grid(row=1, column=0)
    label = Label(r_frame, text=" to ")
    label.grid(row=1, column=1)
    range_entries[1].grid(row=1, column=2)
    zoom_b = Button(master=r_frame, width=20, text="Zoom to Range", command=zoom_range_cmd)
    zoom_b.grid(row=2, column=0, columnspan=3, sticky="we")
    z_out = Button(r_frame, text="Zoom Out", command=zoom_out_cmd)
    z_out.grid(row=3, column=0, columnspan=3, sticky="we")
    window.fit_choice = Button(r_frame, text="Fit to Default", command=window.toggle_fit)
    window.fit_choice.grid(row=4, column=0, columnspan=3, sticky='we')
    r_frame.grid(row=8, column=0, columnspan=3, pady=10)

    # Create frame for checkboxes to be added
    ttk.Separator(frame, orient=HORIZONTAL).grid(pady=10, column=0, row=7, columnspan=3, sticky='ew')
    check_frame = Frame(frame)
    check_frame.grid(row=6, column=0, columnspan=3)

    # Push Buttons and drop down to check box menu
    f = Frame(frame)
    f.grid(row=5, column=0, columnspan=3)
    fitall = Button(f, text="Fit & Save", command=window.fit_and_print, width=9)
    clear = Button(f, text="Clear Fits", command=window.clear_fits, width=9)
    checkAll = Button(f, text="Select All", command=window.check_all, width=9)
    uncheckAll = Button(f, text="Deselect All", command=lambda: window.check_all(True), width=9)
    fitall.grid(row=0, column=0, sticky="e")
    clear.grid(row=0, column=1, sticky="w")
    checkAll.grid(row=1, column=0, sticky="e")
    uncheckAll.grid(row=1, column=1, sticky="w")
    window.choice = StringVar(parent)
    window.choice.set("-Select Set for Fit-")
    options = {"-Select Set for Fit-"}
    window.menu = OptionMenu(f, window.choice, *options)
    window.menu.grid(row=2, column=0, columnspan=2, sticky="ew")
    window.menu.items = []
    # Create a frame for the results menu
    ttk.Separator(frame, orient=HORIZONTAL).grid(pady=10,column=0, row=9, columnspan=3, sticky='ew')
    results = Frame(frame)
    results.grid(row=10, column=0, columnspan=3)

    frame.pack(side=TOP, padx=6, pady=6)

    # Place frames into window class
    window.s_frame = border
    window.check_frame = check_frame
    window.z_range = range_entries

    return results


# Takes a frame and color and adds a checkbox for a single set
def push_check(frame, color, intvar, i, cmd):
    color = webcolors.rgb_to_hex([int(x) for x in color])
    check_button = Checkbutton(frame, text="Set %d" % i, variable=intvar, command=cmd, selectcolor=color)
    check_button.pack(side=TOP)
    check_button.select()
    return check_button


# takes a function name and creates a label and entry box for each parameter excluding time
def set_params_menu(frame, function_name):
    # Erases any previous parameters
    for child in frame.winfo_children():
        child.destroy()
    # Create a header
    header_text = Label(frame, text="Parameters", font='Helvetica 9 bold')
    header_text.pack(side=TOP)

    # Get the parameter list
    params = inspect.getfullargspec(function_name).args
    c = frame.register(DataManip.validate_float)        # To allow entries to only take floats
    # Pack the labels and entries
    entries = []
    for p in params:
        if p is not 'time':
            small_frame = Frame(frame)
            lab = Label(small_frame, text=p + ": ")
            lab.pack(side=LEFT)
            ent = Entry(small_frame, validate="key", vcmd=(c, '%P'))
            ent.pack(side=RIGHT)
            small_frame.pack(side=TOP, anchor="e")
            entries.append(ent)

    return entries       # Return references so frames can be destroyed and entries can be accessed


# Creates the header for the Bottom taskbar and the function picker
# Returns reference to the option menu
def function_menu(frame, cmd=None):
    lab = Label(frame, text="Manual Plot Manager", font='Helvetica 11 bold')
    lab.pack(side=LEFT, anchor="w", padx=20)

    lab2 = Label(frame, text="select a fitting function: ")
    lab2.pack(side=LEFT, anchor="w")

    # Retrieve the names of all functions in the Function module
    options = get_funcs()

    tkvar = StringVar(frame)
    tkvar.set(options[0])
    menu = OptionMenu(frame, tkvar, *options)
    menu.pack(side=LEFT, anchor="w")
    # Trigger the callback when the selection changes
    if cmd is not None:
        tkvar.trace('w', lambda *args: cmd())

    return menu, tkvar


"""
Takes an empty frame and the window class as well as optional commands to attach to buttons
Fills the manual fit range frame with entries for range and buttons for auto range and fit/clear fit
returns instances of entries so values can be retrieved
"""
def create_scale_box(frame, window, load_cmd=None, hold_cmd=None, unlo_cmd=None, full_cmd=None):
    # Create a header
    Label(frame, text="Manual Plot Range", font='Helvetica 9 bold').grid(row=0, columnspan=2, column=0, sticky='we')
    # Create range labels
    label = Label(frame, text="Upper Bound: ")
    label.grid(row=1, column=1)
    label = Label(frame, text="Lower Bound: ")
    label.grid(row=1, column=0)
    # Create entry boxes
    c = frame.register(DataManip.validate_float)
    upper = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    upper.grid(row=2, column=1, padx=8, sticky='ew')
    lower = Entry(frame, validate="key", vcmd=(c, '%P'), width=5)
    lower.grid(row=2, column=0, padx=8, sticky='ew')
    # Create auto range buttons
    row = Frame(frame)
    l = Button(row, text="Loading", command=load_cmd)
    h = Button(row, text="Holding", command=hold_cmd)
    u = Button(row, text="Unloading", command=unlo_cmd)
    f = Button(row, text="Full Range", command=full_cmd)
    l.pack(side=LEFT)
    h.pack(side=LEFT)
    u.pack(side=LEFT)
    f.pack(side=LEFT)
    # Create fit/clear fit buttons
    row.grid(row=3, column=0, columnspan=2)
    row2 = Frame(frame)
    fit = Button(row2, text="Manual Fit", command=lambda: DataManip.Manual_fit(window))
    fit.pack(side=LEFT)
    clr = Button(row2, text="Clear Fits", command=window.clear_fits)
    clr.pack(side=LEFT)
    row2.grid(row=4, column=0, columnspan=2)

    return lower, upper


# Initializes the fitting results menu
def init_results(parent, cmd=None):
    header_text = Label(parent, text="Auto-Fit_Results", font='Helvetica 9 bold')
    header_text.pack(side=TOP)
    frame = Frame(parent)
    default_text = Label(frame, text="Run auto-fit to see results")
    default_text.pack(side=TOP)
    frame.pack(side=TOP)
    button = Button(parent, text="Copy to Manual", command=cmd)
    button.pack(side=TOP)

    return frame


# Inserts fitting results
def insert_results(frame, window, params, eq, r_squared):
    for child in frame.winfo_children():
        child.destroy()
    # Insert r_squared at the top of the list
    Label(frame, text="R^2: {0}".format(r_squared), pady=5).pack(side=TOP)
    param_names = inspect.getfullargspec(eq).args[1:]
    for i in range(len(params)):
        Label(frame, text="%s: %s" % (param_names[i], params[i])).pack(side=TOP)
    window.cur_eq = eq
    window.result_params = params
