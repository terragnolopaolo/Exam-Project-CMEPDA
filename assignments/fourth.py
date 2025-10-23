import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):

    def __init__(self, x, y, k=3):
        self._x = x
        self._y = y
        super().__init__(x, y, k=3) # uso inheritance (decisamente più comodo)
        _y = self._y.cumsum()
        _y /= _y[-1]
        self.cdf = InterpolatedUnivariateSpline(x, _y)
        self.pdf = InterpolatedUnivariateSpline(_y, x)
        # self._spline = InterpolatedUnivariateSpline(x, y) # here I use composition
        xppf, ippf = np.unique(_y, return_index=True)
        yppf = x[ippf]
        self.ppf = InterpolatedUnivariateSpline(xppf, yppf)

    # Le seguenti funzioni non servono più perché ora la mia classa è una spline, eredita da essa.
    # def __call__(self, x): # instead of evaluate()
    #   return self._spline(x)
    
    # def integral(self, x1, x2):
    #   return self._spline.integral(x1, x2)
    
    def plot(self):
        x = np.linspace(self._x.min(), self._x.max(), 200)
        plt.plot(x, self(x))

    def prob(self, x1, x2):
        return self.cdf(x2) - self.cdf(x1)
    
    def rnd(self, size=1000):
        return self.ppf(np.random.uniform(size=size))

# For every PDF I can definte a Comulative Density Function CDF

# Triangular distribution
x = np.linspace(0., 1., 10) # 10 valori nell'intervallo [0, 1] separati dallo stesso passo
y = 2. * x
pdf = ProbabilityDensityFunction(x, y)

assert np.allclose(pdf(0.5), 1) # per risolvere problema comparazione float
assert np.allclose(pdf.integral(0., 1.), 1.)
pdf.plot()
plt.show() # if I put it inside the function plot(), the code will stop there