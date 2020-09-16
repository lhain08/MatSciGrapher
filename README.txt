This utility requires python 3.7 as well as the following external libraries:
- TKinter
- Matplotlib
- Numpy
- SciPy
- Inspect
- Webcolors

This utility takes data from 3 stage nanoindentation tests and plots them
In the utility you can use automatic zoom and fit capabilities and toggle between sets and fitting functions
Plots can be saved as PNG files and fitting results and results can be exported to a text file
To use your own fitting functions, just add them into the Functions.py file with the following specifications
    - First parameter is the xdata (time), you may have as many secondary fit parameters as necessary, just write them in as usual
    - Return a numpy array of ydata (load)
    - You can set bounds on your parameters using .__setattr__("bounds", ([<lower bounds>], [<upper bounds>])
    - You can set initial guesses for fitting using .__setattr__("p0", [<initial values>])
        - This can make results more accurate and efficient if you have expected values for each parameter
    - If you want an open ended bound, np.inf or -np.inf (+/- infinity) can be used as a bound
