'''
Module: advanced Python
Assignment #5 (October 18, 2021)


--- Goal
Write a class to handle a sequence of voltage measurements at different times.

--- Specifications
- the class name must be VoltgeData
- the class must be initialized with two generic iterables of the same length
  holding the numerical values of times and voltages
- alternatively the class can be initialized from a text file
- the class must expose two attributes: 'times' and 'voltages', each returning
  a numpy array of type numpy.float64 of the corresponding quantity.
- the values should be accessible with the familiar square parenthesis syntax:
  the first index must refer to the entry, the second selects time (0) or
  voltage (1). Slicing must also work.
- calling the len() function on a class instance must return the number of
  entries
- the class must be iterable: at each iteration, a numpy array of two
  values (time and voltage) corresponding to an entry in the file must be
  returned
- the print() function must work on class instances. The output must show one
  entry (time and voltage), as well as the entry index, per line.
- the class must also have a debug representation, printing just the values
  row by row
- the class must be callable, returning an interpolated value of the tension
  at a given time
- the class must have a plot() method that plots data using matplotlib.
  The plot function must accept an 'ax' argument, so that the user can select
  the axes where the plot is added (with a new figure as default). The user
  must also be able to pass other plot options as usual
- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py
  as a sequence of proper UnitTests
- [optional] support a third optional column for the voltage errors
'''

import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt


class VoltageData:
    '''Class handling a sequence of voltage measurements at different times'''

    def __init__(self, times, voltages):
        '''Class constructor. Times and voltages are itarable of the same lenght'''

        times = np.array(times, dtype=np.float64)
        voltages = np.array(voltages, dtype=np.float64)
        self.data = np.column_stack([times, voltages])
        self._spline =  interpolate.InterpolatedUnivariateSpline(times, voltages, k=3)

    @property
    def times(self):
        return self.data[:, 0]  # righe della colonna 0

    @property
    def voltages(self):

        return self.data[:, 1]  # righe della colonna 1

    def __getitiem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        header = 'Row-> Time [s], Voltage [mV]\n'

        return header + '\n'.join([f'{i}->{row[0]: .1f}, {row[1]:.2f}'\
                          for i, row in enumerate(self)])

    def __repr__(self):
        return '\n'.join([f'{i}->{row[0]}, {row[1]}'\
                          for i, row in enumerate(self)])

    def __call__(self, t):
        return(self._spline(t))

    def plot(self, ax=None, draw_spline=False, **plot_opts):
        if ax is None:
            plt.figure(('Volt-time'))

        else:
            plt.sca(ax)
        plt.plot(self.times, self.voltages, **plot_opts)

        if draw_spline==True:
            x = np.linspace(min(self.times), max(self.times), 100)
            plt.plot(x, self(x), '-')



if __name__ == '__main__':
    ''' '''
    t = [1., 2., 3.]
    v = [10., 20., 30.]

    t, v = np.loadtxt('sample_data_file.txt', unpack=True)
    vdata = VoltageData(t, v)
    vdata.plot(draw_spline=True)
    plt.show()
