import DataManip as Dm
import os
import math


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
    t = Dm.Test()
    f0 = False
    breaks = []
    while line:
        row = [float(x) for x in line.split()]
        if len(row) == 0:
            if len(t.Time) > 0:
                breaks.append(t.Time[-1])
        else:
            if f0:
                if len(row) == 3:
                    t.push(row)
                else:
                    print(t.Time[-1])
            else:
                if row[0] == 0:
                    f0 = True
        line = f.readline()

    f.close()
    return t, breaks


def retrieve_data(window, folder):
    # Retrieve all data from folder and remove analysis file
    file_names = next(os.walk(folder))[2]
    tests = []
    load_t = []
    for fn in file_names:
        if not ("analysis" in fn.lower()):
            t, breaks = read_file(folder + "/" + fn)
            tests.append(t)
            if len(breaks) > 1:
                load_t.append(breaks[1])

    print(load_t)

    # Get the title for the plot from the folder name
    fname = folder.split('/')[-1]
    title = fname.replace('-', ' ')

    # Get the loading rate
    load_time = fname.split('-')[-1]
    load_time = int(load_time[:3])
    rate = 240/load_time
    window.load_time = load_time


    # Equation constants
    A = (4*rate**2) / (math.pi * (1 - (0.25 ** 2)) * math.tan(math.radians(70.3)))

    return tests, title, A


# Pushes the most recent fit to the output file
def output_params(title, data):
    f = open("Fit_Results/" + title + ".txt", "w")
    output = "Set Number  | E_infinity | E_1        | Lambda_1   | P0         | Tau        | b          |\n"
    output += "-" * 91 + "\n"
    for i in range(len(data)):
        output += "Set {0:<7} |".format(i)
        for e in data[i]:
            output += "{0:^12.5}|".format(e)
        output += "\n"
    f.write(output)
    f.close()

