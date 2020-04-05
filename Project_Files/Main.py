import tkinter as tk
import tkinter.ttk
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

import FileIO
import DataManip
import GUI
import Functions

matplotlib.use("TkAgg")


class Window:
    def __init__(self):
        # List of Tests Plotted
        self.Tests = []
        self.Temporaries = []
        self.TempPlots = []

        # Initialize data dependent variables
        self.load_time = 0
        self.max_time = 0
        self.max_load = 0
        self.min_load = 0
        self.title = ""

        # Reuseable frames
        self.root = tk.Tk()
        self.root.wm_title("Nano-Indentation Graphs")   # Title the window
        print(ttk.Style().theme_names())
        ttk.Style().theme_use('aqua')
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(side="right", fill='y')
        self.graph = Frame(self.root)   # Container for graph canvas
        self.graph.pack(side="left")

        # Dictionaries for stored widgets and variables
        self.widgets = {}
        self.vars = {}

        # Get the display size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        ### Build the graph ###
        # Create the figure
        self.fig = Figure(figsize=(8,6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Load (uN)")
        # Create the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Build Tabs
        GUI.buildDir(self)
        GUI.buildFit(self)
        GUI.buildSets(self)


    # Prompt for a data folder
    def open_folder(self, folder=None):
        if folder is None: folder = tk.filedialog.askdirectory()
        Tests, title, A = FileIO.retrieve_data(self, folder)
        if len(Tests) == 0:
            self.error(8)
            return
        self.Tests = Tests
        self.title = title
        Functions.A = A
        self.max_time = round(max([max(t.Time) for t in self.Tests]))
        self.max_load = max([max(t.Load) for t in self.Tests])
        self.min_load = min([min(t.Load) for t in self.Tests])
        self.plot(self.title)

    # Prompt for location to save image
    def save_as(self):
        file_path = tk.filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if file_path is None:
            return
        self.fig.savefig(file_path.name)

    # Clear the figure and Plot new data
    def plot(self, title):
        # Clear any fits
        self.clear_fits()
        # Delete Associated buttons
        if self.widgets.get('check buttons') is not None:
            for b in self.widgets['check buttons']:
                b.forget()
        else:   # Initialize the check button data
            for child in self.widgets['check frame'].winfo_children():
                child.destroy()
            self.widgets['check buttons'] = []
        # Clear the option menu
        #self.menu['menu'].delete(1, "end")
        #self.choice.set("-Select Set for Fit-")
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Load (uN)")

        index = 0
        for test in self.Tests:
            test.plotref = self.ax.scatter(test.Time, test.Load, s=1)
            # Create checkbox
            test.active = IntVar()
            color = test.plotref.get_facecolors()[0][:3] * 256  # Matches the color to its respective plot
            check_button = GUI.push_check(self.widgets['check frame'], color, test.active,\
                                          self.Tests.index(test), self.checked)
            s = "Set %d" % (self.Tests.index(test))
        #    self.menu['menu'].add_command(label=s, command=tk._setit(window.choice, s))
            self.widgets['check buttons'].append(check_button)
            index += 1
        self.revert()

        # Create the title
        self.fig.suptitle(title, fontsize=20)
        self.canvas.draw()

        # Set max range for sliders
        #self.upper.delete(0, END)
        #self.upper.insert(0, self.max_time)
        #self.lower.delete(0, END)
        #self.lower.insert(0, 0)

    # Hides/shows plots when boxes are checked
    def checked(self):
        for test in self.Tests:
            if test.active.get() != test.plotref.get_visible():
                s = "Set %d" % (self.Tests.index(test))
                # if test.active.get():
                #     self.menu["menu"].add_command(label=s, command=tk._setit(self.choice, s))
                #     if self.choice.get() == "-Select Set for Fit-":
                #         self.choice.set(s)
                # else:
                #     i = 0
                #     while i <= self.menu['menu'].index("end"):
                #         if self.menu['menu'].entrycget(i, "label") == s:
                #             if self.choice.get() == s:
                #                 self.choice.set("-Select Set for Fit-")
                #             self.menu["menu"].delete(i, i)
                #             break
                #         i += 1
                test.plotref.set_visible(test.active.get())
                if not (test.active.get()):
                    for p in test.fits:
                        p.pop(0).remove()
                    test.fits.clear()
        self.canvas.draw()

    # Selects all checkboxes
    def check_all(self, deselect=False):
        for child in self.check_frame.winfo_children():
            if not deselect:    child.select()
            else:
                child.deselect()
                self.clear_fits()
        self.checked()

    # Updates lower range when upper slider is moved
    def update_lower(self, v):
        self.lower.configure(to=v)

    # Updates upper range when lower slider is moved
    def update_upper(self, v):
        self.upper.configure(from_=v)

    # Set the values of the lower and upper fitting scales
    def set_range(self, low, high):
        if low >= 0 and high >= 0:
            self.lower.delete(0, END)
            self.lower.insert(0, low)
            self.upper.delete(0, END)
            self.upper.insert(0, high)

    # Resets plot to original view
    def revert(self):
        self.ax.set_xlim(-1, self.max_time + 1)
        self.ax.set_ylim(self.min_load - (self.max_load/15), self.max_load + (self.max_load/15))
        self.canvas.draw()

    # Zoom to loading curve
    def zoom_loading(self):
        self.ax.set_xlim(0, self.load_time)
        self.canvas.draw()

    # Zoom to holding curve
    def zoom_holding(self):
        self.ax.set_xlim(self.load_time, self.max_time - 10)
        self.canvas.draw()

    # Zoom to unloading curve
    def zoom_unloading(self):
        self.ax.set_xlim(self.max_time - 10, self.max_time)
        self.canvas.draw()

    # Zoom to a specified range
    def zoom_range(self):
        # If entry is empty, assume zero
        for e in self.z_range:
            if e.get() == "":
                e.insert(0, "0")
        lower = self.z_range[0].get()
        upper = self.z_range[1].get()
        try:
            lower = float(lower)
            upper = float(upper)
            if lower < upper:
                self.ax.set_xlim(lower, upper)
                self.canvas.draw()
            else:
                self.error(6)
        except ValueError:
            self.error(6)

    '''
    Clears all displayed fits
    Requires: None
    Effects: removes all plots in self.TempPlots and self.Tests[all].fits and clears all lists
    Returns: None
    '''
    def clear_fits(self):
        # Erase manual fits
        for p in self.TempPlots:
            p.pop(0).remove()
        self.TempPlots.clear()
        # Erase auto fits
        for t in self.Tests:
            for p in t.fits:
                p.pop(0).remove()
            t.fits.clear()
        self.canvas.draw()

    '''
    Finds closest time index in a given test's Time array
    Requires: valid test index
    Effects: None
    Returns: index such that Time[index] is closest time in Time to given value
    '''
    def get_time_index(self, time, test_index):
        if time in self.Tests[test_index].Time:
            return self.Tests[test_index].Time.index(time)
        start_index = int(len(self.Tests[test_index].Time) / 2)
        index = start_index
        count = 1
        while abs(self.Tests[test_index].Time[index] - time) >= 0.016:
            count += 1
            shift = int(len(self.Tests[test_index].Time) / (2 ** count))
            if self.Tests[test_index].Time[index] > time:
                index -= shift
            else:
                index += shift
            if shift == 0:
                break
        a = abs(self.Tests[test_index].Time[index-1] - time)
        b = abs(self.Tests[test_index].Time[index] - time)
        c = abs(self.Tests[test_index].Time[index + 1] - time)
        if a == min([a, b, c]):
            return index - 1
        if c == min([a, b, c]):
            return index + 1
        return index

    '''
    Fits all displayed sets and outputs results to text file under the title of the plot
    Requires: None
    Effects: Writes a table of fit parameters to <self.title>.txt
    Returns: None
    '''
    def fit_and_print(self):
        data = []
        for test in self.Tests:
            row = ["----------"]*6
            if test.active.get():
                row[0:3] = DataManip.auto_fit(self, "Load", False, self.Tests.index(test))
                row[3:] = DataManip.auto_fit(self, "Hold", False, self.Tests.index(test))
            data.append(row)
        if data:
            FileIO.output_params(self.title, data)

    '''
    Callback for when a new manual fit function is selected
    Requires: self.func_select.get() is a valid function name in Functions.py
    Effects: updates manual fit menu to hold the new function's parameters
    Returns: None
    '''
    def func_select_callback(self, *args):
        selection = self.func_select.get()
        self.param_entries = GUI.set_params_menu(self.param_frame, getattr(Functions, selection))

    '''
    Copies the results of the most recent auto-fit to the manual fit parameter menu
    Requires: cur_eq is valid equation and (if valid) param_entries contains correct number of parameters
    Effects: Manual parameter menu- updates function to function of most recent fit, and enters parameters into entries
    Throws: Pop-up warning if no results exist
    Returns: None
    '''
    def copy_results(self):
        if window.cur_eq is not None:
            self.func_select.set(window.cur_eq.__name__)
        else:
            self.error(4)
            return
        for i in range(len(self.param_entries)):
            self.param_entries[i].insert(0, self.result_params[i])

    def toggle_fit(self):
        if self.fit_choice.config('text')[-1] == 'Fit to Default':
            self.fit_choice.config(text='Fit to View')
        else:
            self.fit_choice.config(text='Fit to Default')

    # Begin the loop
    def start(self):
        tk.mainloop()

    # Destroy the window
    def quit(self):
        self.root.quit()
        self.root.destroy()

    # Handles error messages
    def error(self, code=0):
        message = "An Error Occur- Who knows what's wrong"
        if code == 0:
            message = "An unknown error occurred, please help"
        elif code == 1:
            message = "No set selected, please select a set and try again"
        elif code == 2:
            message = "Invalid p0 values for the selected function, default values will be used"
        elif code == 3:
            message = "Invalid bound values for the selected function, default values will be used"
        elif code == 4:
            message = "No results to copy, please make a fit and try again"
        elif code == 5:
            message = "This function has not been implemented yet"
        elif code == 6:
            message = "Invalid range for zoom, please re-enter and try again"
        elif code == 7:
            message = "Overlapping content is displayed in originally selected directory"
        elif code == 8:
            message = "No data found in selected content"
        messagebox.showinfo("Warning", message)


if __name__ == '__main__':
    window = Window()
    window.start()
