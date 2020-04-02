import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import filedialog as fd
import os
import math
from scipy import optimize
import numpy as np
import threading

TESTING = True
global TESTING_PLOT_REFERENCE
TESTING_PLOT_REFERENCE = None

# Define the plot style
plt.style.use("Solarize_Light2")


# Class to hold data for each test
class Test:
    def __init__(self):
        self.Name = ""
        self.Depth = []
        self.Load = []
        self.Time = []
        self.plotref = None

    def push(self, r):
        self.Depth.append(r[0])
        self.Load.append(r[1])
        self.Time.append(r[2])

    def get_time_range(self, low, high):
        li = 0
        hi = len(self.Time)
        ci = 0
        while ci < hi:
            if self.Time[ci] >= low and li == 0:
                li = ci
            elif self.Time[ci] >= high:
                hi = ci
                break
            ci += 1
        return li, hi


def holding_eqn(time, tao, b):
    if (tao == 0):
        return 0
    else:
        global P0
        time = np.array(time)
        time = time - time[0]
        return P0 * (math.exp(1)**(-(time/tao)**b))


def equation(time, Einf, E1, lambda1):
    time = np.array(time)
    P1 = 0.5*Einf*time**2
    P2 = (E1/lambda1)*(time-(1/lambda1))
    P3 = (E1/lambda1**2)*math.exp(1)**(-lambda1*time)
    P = A*(P1+P2+P3)
    return P

def equation_2(time, Einf, E1, lambda1, E2, lambda2):
    time = np.array(time)
    P1 = 0.5*Einf*time**2
    Summation = 0
    for (E, L) in [(E1, lambda1), (E2, lambda2)]:
        Summation += (E/L)*(time-(1/L))
        Summation += (E/L**2)*math.exp(1)**(-L*time)
    P = A*(P1+Summation)
    return P

# Function to read in a data file
def read_file(addr):
    f = open(addr, "r")
    n = 0
    # Skip over header text (n is a precaution to make sure that if something goes wrong the loop will end)
    while len(f.readline().split("\t")) != 3:
        n += 1
        if n > 10:
            print('Error: data not found in file', addr)
            exit(1)
    # Now start interpreting the data
    line = f.readline()
    t = Test()
    f0 = False
    while line:
        row = [float(x) for x in line.split()]
        if f0:
            t.push(row)
        else:
            if row[0] == 0:
                f0 = True
        line = f.readline()

    f.close()
    return t


# Zoom to the loading view
def zoom_load(event):
    ax.set_xlim(0, peak1_time)
    plt.show()


# Zoom to the holding view
def zoom_hold(event):
    ax.set_xlim(peak1_time, peak2_time)
    plt.show()


# Zoom to the unloading view
def zoom_unload(event):
    ax.set_xlim(peak2_time, max_time)
    plt.show()


# Reset view
def zoom_reset(event):
    ax.set_xlim(0, max_time)
    plt.show()


def onclick(event):
    global DELETE
    if DELETE:
        DELETE = False
        click_time = event.xdata
        click_load = event.ydata
        index = 0
        for i in range(0, len(Tests[0].Time)):
            if Tests[0].Time[i] >= click_time:
                index = i
                break
        mn = [20, 0]
        for T in Tests:
            dist = abs(T.Load[index] - click_load)
            if dist < mn[0]:
                mn[0] = dist
                mn[1] = T

        if mn[0] < 2:
            remove_set(mn[1])


def remove_set(T):
    T.plotref.remove()
    Tests.remove(T)
    plt.show()


def toggle_delete(event):
    global DELETE
    DELETE = not DELETE


def fit_eqn(event):
    # Open output file and add table header
    f = open("Table-" + fname + ".txt", 'w')
    f.write("%-12s | %-12s | %-12s | %-12s\n" % ("Sample", "E Infinity", "Ei", "Lambda 1"
                                                 ))
    f.write("-"*50+"\n")

    # Run non-linear regression
    for i in range(0, len(Tests)):
        # Fit loading
        upper_index = Tests[i].Time.index(peak1_time)

        params, params_cov = optimize.curve_fit(equation, Tests[i].Time[0:upper_index], Tests[i].Load[0:upper_index], p0 = [3,1.5,1.5], bounds= ([0, 0, 0], [np.inf, np.inf, np.inf]))
        f.write("%-12s | %12.4f | %12.4f | %12.4f\n" % ("Sample " + str(i), params[0], params[1], params[2]))
        print(params[0], params[1],params[2])
        ax.plot(Tests[i].Time[0:upper_index],equation(Tests[i].Time[0:upper_index],params[0], params[1], params[2]))

        # Fit holding
        lower_index = upper_index
        while (Tests[i].Time[upper_index] < peak2_time):
            upper_index += 1
        global P0
        P0 = Tests[i].Load[lower_index]
        params, params_cov = optimize.curve_fit(holding_eqn, Tests[i].Time[lower_index:upper_index], Tests[i].Load[lower_index:upper_index], bounds = (0, np.inf))
        ax.plot(Tests[i].Time[lower_index:upper_index], holding_eqn(Tests[i].Time[lower_index:upper_index], params[0], params[1]))

        plt.show()
    f.close()

def Plot_Test(event):
    global TESTING_PLOT_REFERENCE
    if TESTING_PLOT_REFERENCE != None:
        TESTING_PLOT_REFERENCE.pop(0).remove()
    a = float(TestingWindow.myapp.Einf.get())
    b = float(TestingWindow.myapp.E1.get())
    c = float(TestingWindow.myapp.L1.get())
    upper_index = Tests[i].Time.index(peak1_time)
    TESTING_PLOT_REFERENCE = ax.plot(Tests[i].Time[0:upper_index], equation(Tests[i].Time[0:upper_index],a,b,c))
    plt.show()


# Start the program
if __name__ == '__main__':
    global DELETE
    DELETE = False
    Tests = []
    # Prompt for a folder
    root = tk.Tk()
    folder = fd.askdirectory()
    root.destroy()

    # Retrieve all data from folder and remove analysis file
    filenames = next(os.walk(folder))[2]
    for fn in filenames:
        if not ("analysis" in fn.lower()):
            Tests.append(read_file(folder + "/" + fn))

    # Get the title for the plot from the folder name
    fname = folder.split('/')[-1]
    title = fname.replace('-', ' ')

    # Get the loading rate
    load_time = fname.split('-')[-1]
    load_time = int(load_time[:3])
    rate = 240/load_time

    # Equation constants
    A = (4*rate**2) / (math.pi * (1 - (0.25 ** 2)) * math.tan(math.radians(70.3)))


    # Plot Data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(0,len(Tests)):
        Tests[i].plotref = ax.scatter(Tests[i].Time, Tests[i].Load, s=1, label=i)

    # Find the max time
    max_time = max([max(t.Time) for t in Tests])
    # Find the end of the loading stage
    points_per_second = max([len(T.Time) for T in Tests])
    peak1_time = load_time
    # Find the end of the holding stage
    peak2_time = max_time - 10

    # Add title and labels
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Load (uN)")

    # Set up Load button
    axload = plt.axes([0.6, 0.02, 0.09, 0.04])
    bload = Button(axload, "Loading")
    bload.on_clicked(zoom_load)
    # Set up Hold button
    axhold = plt.axes([0.7, 0.02, 0.09, 0.04])
    bhold = Button(axhold, "Holding")
    bhold.on_clicked(zoom_hold)
    # Set up Unload button
    axunload = plt.axes([0.8, 0.02, 0.09, 0.04])
    bunload = Button(axunload, "Unload")
    bunload.on_clicked(zoom_unload)
    # Set up Reset button
    axreset = plt.axes([0.9, 0.02, 0.09, 0.04])
    breset = Button(axreset, "Reset")
    breset.on_clicked(zoom_reset)
    # Set up Delete button
    axdel = plt.axes([0.1, 0.02, 0.14, 0.04])
    bdel = Button(axdel, "Delete Set")
    bdel.on_clicked(toggle_delete)
    # Set up create table button
    axct = plt.axes([0.25, 0.02, 0.14, 0.04])
    bct = Button(axct, "Create Table")
    bct.on_clicked(fit_eqn)
    # Set up testing button
    if TESTING:
        axtb = plt.axes([0.4,0.02,0.14,0.04])
        tbt = Button(axtb, "Plot Test")
        tbt.on_clicked(Plot_Test)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    if TESTING:
        import TestingWindow
        thread = threading.Thread(target=TestingWindow.Start)
        thread.start()

    plt.show()

    if TESTING:
        thread.join()



