import math
import numpy as np
from scipy import optimize
import inspect

import Functions
import GUI


# Class to hold data for each test
class Test:
    def __init__(self):
        self.Name = ""
        self.Depth = []
        self.Load = []
        self.Time = []
        self.plotref = None
        self.fits = []
        self.active = None
        self.time_shift = 0
        self.load_shift = 0

    def push(self, r):
        # Calculate shifts
        if len(self.Time) == 0:
            self.time_shift = r[2]
            self.load_shift = r[1]
        self.Depth.append(r[0])
        self.Load.append(r[1] - self.load_shift)
        self.Time.append(r[2] - self.time_shift)


class LoadingEquation:
    def __init__(self):
        self.A = 0

    def loading_eq(self, time, E_infinity, E1, lambda1):
        time = np.array(time)
        p1 = 0.5*E_infinity*time**2
        p2 = (E1/lambda1)*(time-(1/lambda1))
        p3 = (E1/(lambda1**2))*(math.exp(1)**(-lambda1*time))
        p = self.A*(p1+p2+p3)
        return p

    def loading_eq_2(self, time, E_infinity, E1, lambda1, E2, lambda2):
        time = np.array(time)
        p1 = 0.5*E_infinity*time**2
        p2 = (E1/lambda1)*(time-(1/lambda1))
        p3 = (E1/lambda1**2)*math.exp(1)**(-lambda1*time)
        p4 = (E2/lambda2)*(time-(1/lambda2))
        p5 = (E2/lambda2**2)*math.exp(1)**(-lambda2*time)
        p = self.A*(p1+p2+p3+p4+p5)
        return p


class HoldingEquation:
    def __init__(self):
        self.P0 = 0

    def holding_eq(self, time, tao, b):
        if tao == 0:
            return 0
        else:
            time = np.array(time)
            time = time - time[0]
            return self.P0 * (math.exp(1)**(-(time/tao)**b))


def auto_fit(plot, stage, show=True, test_index=None):
    if test_index is None:
        test_index = plot.choice.get()
        if test_index == "-Select Set for Fit-":
            plot.error(1)
            return
        test_index = int(plot.choice.get().split(" ")[-1])

    if stage.upper() == "LOAD":
        start_t = 0
        end_t = plot.load_time
        eq = getattr(Functions, plot.load_choice.get())
    elif stage.upper() == "HOLD":
        start_t = plot.load_time
        end_t = plot.max_time-10
        eq = getattr(Functions, plot.hold_choice.get())
    elif stage.upper() == "UNLOAD":
        start_t = plot.max_time-10    # When unloading equation is available
        end_t = plot.max_time
        eq = getattr(Functions, plot.unload_choice.get())
    else:
        plot.error()
        return
    if plot.fit_choice.config('text')[-1] == 'Fit to View':
        start_t, end_t = plot.ax.get_xlim()
    p = len(inspect.getfullargspec(eq).args[1:])
    index0 = plot.get_time_index(start_t, test_index)
    index1 = plot.get_time_index(end_t, test_index)
    # Verifies that the p0 and bound values in functions are valid
    try:
        p0 = eq.__getattribute__("p0")
        if len(p0) != p:
            plot.error(code=2)
            raise TypeError
    except (AttributeError, TypeError) as e:
        p0 = None
    try:
        bounds = eq.__getattribute__("bounds")
        if [len(x) for x in bounds] != [p, p]:
            plot.error(code=3)
            raise TypeError
    except (AttributeError, TypeError) as e:
        bounds = (-np.inf, np.inf)
    # Fit data to equation
    time_array = np.array(plot.Tests[test_index].Time[index0:index1])
    load_array = np.array(plot.Tests[test_index].Load[index0:index1])
    params, cov = optimize.curve_fit(eq, time_array, load_array, p0=p0, bounds=bounds, maxfev=100000)
    if show:
        plot.Tests[test_index].fits.append(plot.ax.plot(time_array, eq(time_array, *params), color="black"))
        plot.canvas.draw()
        residuals = load_array - eq(time_array, *params)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((load_array-np.mean(load_array))**2)
        r_squared = 1 - (ss_res / ss_tot)
        GUI.insert_results(plot.result_f, plot, params, eq, r_squared)
    return params


# Manual fit with parameters and bounds
def Manual_fit(window):
    bounds = [float(window.lower.get()), float(window.upper.get())]
    try:
        params = [float(e.get()) for e in window.param_entries]
    except ValueError:
        print("Please enter valid parameters")
        return

    eq = getattr(Functions, window.func_select.get())
    n = max([200,(bounds[1] - bounds[0])*5])
    time = np.linspace(bounds[0], bounds[1], num=n)
    window.TempPlots.append(window.ax.plot(time, eq(time, *params), color="black"))
    window.canvas.draw()


# Validation function for entries
def validate_float(s):
    try:
        float(s)
        return True
    except ValueError:
        if s == "-" or s == "." or s == "-.":
            return True
        return s == ""
