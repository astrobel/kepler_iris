import os
# os.environ['MKL_NUM_THREADS'] = '1'

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.gridspec as gs
# import matplotlib.pylab as pl
# from matplotlib.colors import ListedColormap
# import matplotlib.colors as colors
# from matplotlib.ticker import MaxNLocator
from astropy.stats import LombScargle
from astropy.utils.exceptions import AstropyWarning
from astropy.io import fits
import lightkurve as lk
import cutouts as cut
import subtraction as sub
import eventfixer as fx
import fit_and_clip as fc
import nancleaner as nc
import glob, sys, warnings, argparse

quarterlines = [120, 131, 169, 259, 351, 442, 538, 629, 734, 808, 906, 1000, 1098, 1182, 1273, 1372, 1471, 1558]

parser = argparse.ArgumentParser(description='Compare noise and S/N for targets with both Kepler and IRIS light curves.')
parser.add_argument('-n', '--ngc', required=True, type=int, choices=[6791, 6819], help='Cluster')

params = parser.parse_args()

cluster = params.ngc
centroid = 'e'

wd = os.getcwd()
sd = '/suphys/icol6407/../../import/silo4/icol6407/iris2/'

quarterlist = np.arange(0,18)

members = pd.read_csv(f'{cluster}comparison.csv')
kics = members['Kepler_ID']
kep_qs = members['Kep_quarters']
stamp_qs = members['Stamp_quarters']
signal = members['Signal']

noise_i = np.zeros(len(kics))
sn_i = np.zeros(len(kics))
noise_k = np.zeros(len(kics))
sn_k = np.zeros(len(kics))

# kern = 100 # for smoothing
# sigma = (factor**2) * 2 # for clipping

time = []
x_cent = []
y_cent = []

raw_k = np.zeros((1,2))
masked_k = np.zeros((1,2))
means_k = []

for n, kic in enumerate(kics):

    for q in quarterlist:

        lc = lk.search_lightcurvefile(kic, quarter=q).download()

        if lc != None:
            table = lc.hdu[1].data
            flux_n, time_n = nc.nancleaner2d(table['SAP_FLUX'], table['TIME'])
            means_k.append(np.nanmean(flux_n))
            time, flux = fx.fixer(q, time_n, flux_n, cluster)
            temp = np.c_[time, flux]
            raw_k = np.r_[raw_k, temp]
            time, flux = fc.fitandclip(time, flux)
            temp = np.c_[time, flux]
            masked_k = np.r_[masked_k, temp]

    raw_k = np.delete(raw_k, 0, axis=0) # remove placeholder zeros
    masked_k = np.delete(masked_k, 0, axis=0)
    masked_k[:,1] = masked_k[:,1]/np.nanmean(means_k)

    ### DATA HANDLING ###

    # for amplitude summary plot
    medbins = int(280 / 30)
    bins = np.zeros(medbins)

    time = masked_k[:,0]
    flux = masked_k[:,1]

    # amplitude spectrum
    ofac = int(5)
    hifac = int(1)
    freqs, ampls = LombScargle(np.asarray(time), np.asarray(flux)).autopower(method='fast', normalization='psd', samples_per_peak=ofac, nyquist_factor=hifac)
    hifac *= (283/11.57)/max(freqs)
    freqs, ampls = LombScargle(np.asarray(time), np.asarray(flux)).autopower(method='fast', normalization='psd', samples_per_peak=ofac, nyquist_factor=hifac)
    ampls = ampls * 4. / len(time)
    ampls = np.sqrt(ampls)
    ampls *= 1e6
    freqs *= 11.57
    
    for j in range(medbins):
        bins[j] = np.median(ampls[(freqs > j*30) & (freqs <= (j+1)*30)])

    noise_k[n] = bins[-1]
    sn_k[n] = max(ampls)/bins[-1]

    # and get other data to put it all in the same place
    os.chdir(f'{sd}{kic}_{centroid}/')
    f = open(f'{kic}_{centroid}.dat')
    for param in f:
        if param.startswith('high'):
            noise_i[n] = np.float64(param.split('high freq noise = ')[1].split(' ppm')[0])
        if param.startswith('S/N'):
            sn_i[n] = np.float64(param.split('S/N = ')[1].split('\n')[0])
    os.chdir(wd)

output = {'KIC':kics, 'noise_iris':noise_i, 'sn_iris':sn_i, 'noise_kep':noise_k, 'sn_kep':sn_k}
out = pd.DataFrame(data=output)
out.to_csv(f'{cluster}kepnoise.csv')