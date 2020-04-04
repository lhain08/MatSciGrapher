import DataManip as Dm
import os
import math


# Function to read in a data file
def read_file(addr):
    f = open(addr, "r", errors='ignore')
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
                if row[0] == 0:
                    f0 = True
        line = f.readline()

    f.close()
    return t, breaks


def retrieve_data(window, folder):
    # Retrieve all data from folder and remove analysis file
    print(folder)
    if os.path.isfile(folder):
        file_names = [os.path.split(folder)[1]]
        folder = os.path.split(folder)[0]
    else:
        file_names = next(os.walk(folder))[2]
    tests = []
    load_t = []
    for fn in file_names:
        if not ("analysis" in fn.lower()):
            t, breaks = read_file(folder + "/" + fn)
            tests.append(t)
            if len(breaks) > 1:
                load_t.append(breaks[1])

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


'''
Take a tree and folder and recursively populate the tree below the starting folder
'''
def populate_tree(tree, folder, parent='', count = 0):
    returnVal = 0   # Catches overlap issues
    try:
        id = tree.insert(parent, 'end', parent.rstrip('/') + '/' + folder, text=folder)
    except:
        return 1
    try:
        files = next(os.walk(parent.rstrip('/') + '/' + folder))
    except StopIteration:
        return

    # limit the depth of the population
    if count >= 6: return

    for sub_folder in files[1]:
        returnVal = populate_tree(tree, sub_folder, id, count+1)
    for file in files[2]:
        tree.insert(id, 'end', id+'/'+file, text=file)

    return returnVal


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

