import numpy
from matplotlib import pyplot as plt
from scipy import interpolate

class VoltageData:

    def __init__(self, times, voltages):
        t = numpy.array(times, dtype=numpy.float64)
        v = numpy.array(voltages, dtype=numpy.float64)
        self._data = numpy.column_stack([t, v]) # unisce n colonne
        self.spline = interpolate.InterpolatedUnivariateSpline(self.timestamps,
                                                               self.voltages,
                                                               k=3)
    
    @property
    def timestamps(self):
        return self._data[:, 0]
    
    @property
    def voltages(self):
        return self._data[:, 1]
        
        
    @classmethod #altro costruttore
    def from_file(cls, file_path):
        timestamps, voltages = numpy.loadtxt(file_path, unpack=True)
        return cls(timestamps, voltages)
    
    def __len__(self):
        return len(self._data) # di certo che i due sono lunghi uguali grazie a numpy
    
    def __getitem__(self, indices): #operatore []; indices è tupla con riga e colonna: devo controllare cosa succede se do indices con solo un numero -> uso column_stack nel costruttore
        return self._data[indices]
    
    def __iter__(self): #lo implemento con un generatore che restituisce riga della matrice 2D di numpy
        for row in self._data:
            yield row

    def __str__(self): # uso list comprehension
        return '\n'.join([f'{i}) {line[0]} {line[1]}' for i, line in enumerate(self)])
    
    def __call__(self, t):
        return self.spline(t)
    
    def plot(self, ax=None, fmt='bo', **plot_options):
       from matplotlib import pyplot as plt
       # The user can provide an existing figure to add the plot, otherwise we
       # create a new one.
       if ax is not None:
           plt.sca(ax) # sca (Set Current Axes) selects the given figure
       else:
           ax = plt.figure('voltage_vs_time')
       plt.plot(self.timestamps, self.voltages, fmt, **plot_options)
       plt.xlabel('Time [s]')
       plt.ylabel('Voltage [mV]')
       plt.grid(True)
       return ax
      
        