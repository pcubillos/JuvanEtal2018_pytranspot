#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d as gaussf

sys.path.append("../pyratbay")
import pyratbay as pb
import pyratbay.constants as pc


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Initialize Pyrat object:
pyrat = pb.pyrat.init("spectrum_001Xsolar.cfg")
wl   = 1.0/(pyrat.spec.wn*pc.A)
q    = pyrat.atm.q
temp = pyrat.atm.temp

# Compute spectrum:
#pyrat.phy.rplanet = 1.182*pc.rjup
pyrat = pb.pyrat.run(pyrat, [temp, q])
sigma = 5.0
spectrum = gaussf(np.sqrt(pyrat.spec.spectrum), sigma)

# The data:
bandwl = np.array([7280.0,  8386.0, 6641.0])
rprs   = 0.136 + np.array([0.001325, 0.001640, 0.001257])
rprse  = [0.000371, 0.001161, 0.000505]
width  = [550, 950, 495]

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# The plot:
lw = 1.5
plt.figure(5, (8.5,5))
plt.clf()
ax = plt.axes([0.12, 0.12, 0.82, 0.82])
# models:
plt.plot(wl, spectrum, "-", lw=lw, zorder=0,
         label=r"$100\times\,{\rm solar}$", color='orange')
# data:
plt.errorbar(bandwl, rprs, rprse, xerr=width, fmt="o", color="b",
             ms=8, zorder=1, capthick=lw,
             lw=lw, label=r"$\rm This\ work$")
plt.xlim(5000, 10000)
plt.ylabel(r"$R_{\rm p} / R_{\rm s}$", fontsize=16)
plt.xlabel(r"$\rm Wavelength\ \ (A)$", fontsize=16)
#plt.legend(loc='best', fontsize=11)
plt.savefig("../plots/WASP491_spectrum.ps")

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Save to file:
with open("WASP-41b_1Xsolar.dat", "w") as f:
  f.write("# Wavelength(A)   Rp/Rs\n")
  for i in np.arange(len(wl)):
    f.write("  {:7.1f}         {:.7e}\n".format(wl[i], spectrum[i]))

