import os
os.environ['MKL_NUM_THREADS'] = '1'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gs
import matplotlib.pylab as pl
from matplotlib.colors import ListedColormap
import matplotlib.colors as colors
from matplotlib.ticker import MaxNLocator
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

C = ['#e6e7e8','#e5e6e7','#e4e6e7','#e4e5e6','#e3e5e5','#e3e4e5','#e2e4e4','#e2e3e4','#e1e2e3','#e1e2e3','#e0e1e2','#e0e1e1','#dfe0e1','#dfdfe0','#dedfe0','#dededf','#dddedf','#dcddde','#dcdddd','#dbdcdd','#dbdbdc','#dadbdc','#dadadb','#d9dada','#d9d9da','#d8d9d9','#d8d8d9','#d7d7d8','#d7d7d8','#d6d6d7','#d6d6d6','#d5d5d6','#d4d4d5','#d4d4d5','#d3d3d4','#d3d3d3','#d2d2d3','#d2d2d2','#d1d1d2','#d1d0d1','#d0d0d1','#d0cfd0','#cfcfcf','#cfcecf','#cecdce','#cecdce','#cdcccd','#cccccc','#cccbcc','#cbcbcb','#cbcacb','#cac9ca','#cac9ca','#c9c8c9','#c9c8c8','#c8c7c8','#c8c6c7','#c7c6c7','#c7c5c6','#c6c5c5','#c6c4c5','#c5c4c4','#c4c3c4','#c4c2c3','#c3c2c3','#c3c1c2','#c2c0c1','#c1c0c1','#c1bfc0','#c0bebf','#bfbebe','#bfbdbe','#bebcbd','#bdbcbc','#bdbbbc','#bcbabb','#bbbaba','#bbb9ba','#bab8b9','#b9b8b8','#b8b7b8','#b8b6b7','#b7b6b6','#b6b5b6','#b6b4b5','#b5b4b4','#b4b3b4','#b4b2b3','#b3b1b2','#b2b1b2','#b2b0b1','#b1afb0','#b0afb0','#b0aeaf','#afadae','#aeadae','#aeacad','#adabac','#acabab','#acaaab','#aba9aa','#aaa9a9','#aaa8a9','#a9a7a8','#a8a7a7','#a8a6a7','#a7a5a6','#a6a5a5','#a5a4a5','#a5a3a4','#a4a3a3','#a3a2a3','#a3a1a2','#a2a1a1','#a1a0a1','#a19fa0','#a09e9f','#9f9e9f','#9f9d9e','#9e9c9d','#9d9c9d','#9d9b9c','#9c9a9b','#9b9a9b','#9b999a','#9a9899','#999898','#999798','#989697','#979697','#979596','#969596','#969495','#959494','#959394','#949393','#939293','#939292','#929192','#929091','#919090','#918f90','#908f8f','#908e8f','#8f8e8e','#8e8d8e','#8e8d8d','#8d8c8d','#8d8c8c','#8c8b8b','#8c8a8b','#8b8a8a','#8b898a','#8a8989','#898889','#898888','#888788','#888787','#878686','#878586','#868585','#868485','#858484','#848384','#848383','#838283','#838282','#828181','#828181','#818080','#818080','#807f7f','#7f7e7f','#7f7e7e','#7e7d7e','#7e7d7d','#7d7c7c','#7d7c7c','#7c7b7b','#7c7b7b','#7b7a7a','#7a7a7a','#7a7979','#797879','#797878','#787777','#787777','#777676','#767676','#767575','#757575','#757474','#747474','#747373','#747373','#737373','#737272','#737272','#727272','#727171','#727171','#717171','#717070','#717070','#707070','#706f6f','#6f6f6f','#6f6f6f','#6f6e6e','#6e6e6e','#6e6e6e','#6e6d6d','#6d6d6d','#6d6d6d','#6d6c6c','#6c6c6c','#6c6c6c','#6c6b6b','#6b6b6b','#6b6a6a','#6b6a6a','#6a6a6a','#6a6969','#6a6969','#696969','#696868','#686868','#686868','#686767','#676767','#676767','#676666','#666666','#666666','#666565','#656565','#656565','#656464','#646464','#646464','#646363','#636363','#636363','#626262','#626262','#626262','#616161','#616161','#616161','#606060','#606060','#606060','#5f5f5f','#5f5f5f','#5f5f5f','#5e5e5e']
middling_grey = mpl.colors.ListedColormap(C)
quarterlines = [120, 131, 169, 259, 351, 442, 538, 629, 734, 808, 906, 1000, 1098, 1182, 1273, 1372, 1471, 1558]

warnings.simplefilter('ignore', category=AstropyWarning)
warnings.simplefilter('ignore', category=UserWarning)
warnings.simplefilter('ignore', category=lk.utils.LightkurveWarning)

mpl.rc('text', usetex=True)
mpl.rcParams['text.latex.preamble'] = [
    r'\usepackage{helvet}',
    r'\usepackage[EULERGREEK]{sansmath}',
    r'\sansmath'
]
mpl.rcParams['axes.formatter.useoffset'] = False
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True

class MidpointNormalize(colors.Normalize):
   # from https://matplotlib.org/users/colormapnorms.html#custom-normalization-two-linear-ranges
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def magnitude(flux, refflux, refmag):
    mag = refmag - 2.5 * np.log10(flux/refflux)
    return mag

def magnituder(flux1, time1, refflux, refmag):

    fluxnew, timenew = nc.nancleaner3d(flux1, time1)
    avs = np.nansum(np.nansum(fluxnew, axis=1), axis=1)
    avgflux = np.median(avs)
    if refflux == 0:
        refflux = avgflux
    mag = magnitude(avgflux, refflux, refmag)

    return mag, avgflux

parser = argparse.ArgumentParser(description='Perform image subtraction on NGC 6791 and NGC 6819 targets.')
parser.add_argument('-k', '--kic', required=True, type=int, help='KIC ID')
parser.add_argument('-s', '--stampfilepath', required=False, default='./superstamps/', type=str, help='File location of superstamps')
parser.add_argument('-r', '--regridfactor', required=False, default=2, type=int, help='Regridding factor')
parser.add_argument('-c', '--centroid', required=True, choices=['e', 't'], type=str, help='Ensemble or target centroid?')
parser.add_argument('-d', '--dims', required=False, default=3, type=int, choices=np.arange(2,20), help='Cutout dimensions')
parser.add_argument('-m', '--missing', required=False, default=None, nargs='+', choices=np.arange(1,18), type=int, help='Any quarters to cut?')
parser.add_argument('-f', '--figures', required=False, default=True, type=bool, help='Make summary plots?')
parser.add_argument('-i', '--interactive', required=False, default=False, type=bool, help='Show plot?')

params = parser.parse_args()

kic = params.kic
factor = params.regridfactor
centroid = params.centroid
missing = params.missing
cutoutdims = params.dims
makefigs = params.figures

cluster = 0
kic = str(kic)
if kic.startswith('2'): # change these eventually to if cluster == flag
    cluster = 6791
    quarterlist = list(np.arange(1, 18))
    # refstar = 2436824
    refflux = 29291.74088601505
    refKp = 14.515
elif kic.startswith('5') or kic.startswith('4'):
    cluster = 6819
    quarterlist = [1,2,3,4,5,7,8,9,11,12,13,15,16,17]
    # refstar = 5111949
    refflux = 106088.38055590221
    refKp = 12.791
if missing != None:
    quarterlist = [i for i in quarterlist if i not in missing]
kic = int(kic)
emptyquarters = []

members = pd.read_csv(f'kiclist{cluster}.csv')
kics = members['Kepler_ID']
ras = members['RA (J2000)']
decs = members['Dec (J2000)']
teff = members['Teff']
Kps = members['kepmag']

target_ra = ras[kics ==  kic].values[0]
target_dec = decs[kics == kic].values[0]
Kp = Kps[kics == kic].values[0]

wd = os.getcwd()
sd = '/headnode2/icol6407/iris/'
# sd = '/suphys/icol6407/../../import/silo4/icol6407/iris/'

try:
    os.chdir(sd)
    os.mkdir(f'{kic}_{centroid}')
    os.chdir(wd)
except FileExistsError:
    os.chdir(f'{sd}{kic}_{centroid}')
    extant_files = glob.glob('./*.fits')
    for f in extant_files:
        os.remove(f)
    os.chdir(wd)

kern = 100 # for smoothing
sigma = (factor**2) * 2 # for clipping

time = []
x_cent = []
y_cent = []

### GETTING CROWDING MAGNITUDE

mag = 0

for i, q in enumerate(quarterlist):

    target_ra = ras[kics ==  kic].values[0]
    target_dec = decs[kics == kic].values[0]

    skip, flux1, time1, eo, w, cadence, fitslist = cut.cutout(kic, q, params.stampfilepath, cluster, target_ra, target_dec, cutoutdims)
    if skip == False:
        mag1, bigflux = magnituder(flux1, time1, refflux, refKp)
        mag += mag1
        # print(q, mag1, bigflux)
        # saving fluxes and times
        exec("flux1_%d = flux1" % q)
        exec("time1_%d = time1" % q)
        exec("cadence_%d = cadence" % q)
        exec("fitslist_%d = fitslist" % q)
        exec("w_%d = w" % q)
        exec("eo_%d = eo" % q)
    else:
        emptyquarters.append(q)

for q in emptyquarters:
    quarterlist.remove(q)

if len(quarterlist) != 0: # this is a useful way to vet for stars that made it onto the list by accident (i.e. they're off the stamps)
    mag /= len(quarterlist)
    # print(mag)
else:
    sys.exit("No quarters available for this target")

# print(Kp)

mag_diff = Kp - mag
if mag_diff > 0:
    isolation = 0.75/np.power(2.5,mag_diff) + 0.25
else:
    isolation = 1

### DOING SUBTRACTION
raw = np.zeros((1,3))
masked = np.zeros((1,3))
means = []

total_exposure = 0
start_time = 0
end_time = 0

for i, q in enumerate(quarterlist):

    exec("flux1 = flux1_%d" % q)
    exec("time1 = time1_%d" % q)
    exec("cadence = cadence_%d" % q)
    exec("fitslist = fitslist_%d" % q)
    exec("w = w_%d" % q)
    exec("eo = eo_%d" % q)

    output, maskarr, avgflux, regridded_base, xc, yc = sub.subtract(flux1, time1, cadence, q, factor, './centroids/', centroid, cutoutdims, cluster, isolation)

    hdr = w.to_header()

    # hdr = fits.Header()
    hdr['HLSPTARG'] = (f'KIC {kic}', 'HLSP target identifier')
    hdr['HLSPID'] = ('IRIS', 'HLPS collection identifier')
    hdr['HLSPLEAD'] = ('Isabel Colman', 'HLSP project lead')
    hdr['LICENSE'] = ('CC BY 4.0', 'license for use of these data')
    hdr['LICENURL'] = ('https://creativecommons.org/licenses/by/4.0/', 'data license URL')
    # hdr['REFERENC'] = ('https://doi.org/10.17909/t9-w8fw-4r14', 'bibliographic identifier') #wait for DOI from publisher
    hdr['KEPLERID'] = (kic, 'unique Kepler target identifier')
    hdr['QUARTER'] = (q, 'Observing quarter')
    hdr['CLUSTER'] = (f'NGC {cluster}', 'cluster superstamp on which target falls')
    hdr['RA_OBJ'] = (target_ra, '[deg] right ascension')
    hdr['DEC_OBJ'] = (target_dec, '[deg] declination')
    hdr['RADESYS'] = ('ICRS', 'check description of RADE4') ###
    hdr['EQUINOX'] = (2000.0, 'equinox of the celestial coordinate system')
    hdr['FILTER'] = ('Kepler', 'name of filter used to define passband')
    hdr['XPOSURE'] = (1800, '[s] cadence of exposure')

    for j, val in enumerate(fitslist):
        hdr[val] = fitslist[val]

    primary_hdu = fits.PrimaryHDU(header=hdr)

    col1 = fits.Column(name='CADENCE', array=output[:,0], format='K')
    col2 = fits.Column(name='TIME', array=output[:,1], format='D')
    col3 = fits.Column(name='FLUX', array=output[:,2], format='D')

    data_hdu = fits.BinTableHDU.from_columns([col1, col2, col3])
    data_hdu.header.update({'TUNIT2':('BJD - 2454833', 'column units: barycenter corrected JD'), 'TUNIT3':('e-/s', 'column units: electrons per second')})
    hdul = fits.HDUList([primary_hdu, data_hdu])

    # for saving things to put in the header of the entire corrected lc fits file
    if np.min(quarterlist) == np.max(quarterlist):
        beginning = fitslist['DATE-BEG']
        start_time = fitslist['TSTART']
        ending = fitslist['DATE-END']
        end_time = fitslist['TSTOP']
    elif q == np.min(quarterlist):
        beginning = fitslist['DATE-BEG']
        start_time = fitslist['TSTART']
    elif q == np.max(quarterlist):
        ending = fitslist['DATE-END']
        end_time = fitslist['TSTOP']
    total_exposure += fitslist['TELAPSE'][0]

    writeq = q
    if q < 10:
        writeq = f'0{q}'

    os.chdir(f'{sd}{kic}_{centroid}/')
    hdul.writeto(f'hlsp_iris_kepler_phot_kplr{kic}-q{writeq}_kepler_v1.0_lc.fits')
    os.chdir(wd)

    xc = np.r_[xc, x_cent]
    yc = np.r_[yc, y_cent]

    flux = output[:,2]
    time = output[:,1]
    cadence = output[:,0]
    means.append(np.nanmean(flux))
    cadence_keep, time_keep, flux_keep = fx.fixer_c(q, cadence, time, flux, cluster)
    temp = np.c_[cadence_keep, time_keep, flux_keep]
    raw = np.r_[raw, temp]
    time_final, flux_final = fc.fitandclip(time_keep, flux_keep)
    cadence_final, flux_chuck = fc.fitandclip(cadence_keep, flux_keep)
    temp = np.c_[cadence_final, time_final, flux_final]
    masked = np.r_[masked, temp]

    avgflux = np.flipud(avgflux)
    # if eo == 0: # scrapping for pixel plot compatibility
    #     avgflux = np.fliplr(avgflux)

raw = np.delete(raw, 0, axis=0) # remove placeholder zeros
masked = np.delete(masked, 0, axis=0)
masked[:,2] = masked[:,2]/np.nanmean(means)

print(f'{kic} nothing yet')

hdr = w.to_header()

# hdr = fits.Header()
hdr['HLSPTARG'] = (f'KIC {kic}', 'HLSP target identifier')
hdr['HLSPID'] = ('IRIS', 'HLPS collection identifier')
hdr['HLSPLEAD'] = ('Isabel Colman', 'HLSP project lead')
hdr['LICENSE'] = ('CC BY 4.0', 'license for use of these data')
hdr['LICENURL'] = ('https://creativecommons.org/licenses/by/4.0/', 'data license URL')
# hdr['REFERENC'] = ('https://doi.org/10.17909/t9-w8fw-4r14', 'bibliographic identifier') #wait for DOI from publisher
hdr['KEPLERID'] = (kic, 'unique Kepler target identifier')
hdr['QUARTER'] = (q, 'Observing quarter')
hdr['CLUSTER'] = (f'NGC {cluster}', 'cluster superstamp on which target falls')
hdr['RA_OBJ'] = (target_ra, '[deg] right ascension')
hdr['DEC_OBJ'] = (target_dec, '[deg] declination')
hdr['RADESYS'] = ('ICRS', 'check description of RADE4') ###
hdr['EQUINOX'] = (2000.0, 'equinox of the celestial coordinate system')
hdr['FILTER'] = ('Kepler', 'name of filter used to define passband')
hdr['XPOSURE'] = (1800, '[s] cadence of exposure')

for j, val in enumerate(fitslist):
    if fitslist[val][0] != 'TSTART' and fitslist[val][0] != 'TSTOP' and fitslist[val][0] != 'TELAPSE' and fitslist[val][0] != 'EXPOSURE' and fitslist[val][0] != 'DATE-BEG'  and fitslist[val][0] != 'DATE-END':
        hdr[val] = fitslist[val]

hdr['DATE-BEG'] = beginning
hdr['DATE-END'] = ending
hdr['TSTART'] = start_time
hdr['TSTOP'] = end_time
hdr['TELAPSE'] = (total_exposure, '[d] time elapsed between start and end of observation')

primary_hdu = fits.PrimaryHDU(header=hdr)

col1 = fits.Column(name='CADENCE', array=masked[:,0], format='K')
col2 = fits.Column(name='TIME', array=masked[:,1], format='D')
col3 = fits.Column(name='CORRECTED_FLUX', array=masked[:,2], format='D')

data_hdu = fits.BinTableHDU.from_columns([col1, col2, col3])
data_hdu.header.update({'TUNIT2':('BJD - 2454833', 'column units: barycenter corrected JD'), 'TUNIT3':('e-/s', 'column units: electrons per second')})
hdul = fits.HDUList([primary_hdu, data_hdu])

os.chdir(f'{sd}{kic}_{centroid}/')
hdul.writeto(f'hlsp_iris_kepler_phot_kplr{kic}-stitched_kepler_v1.0_lc.fits')
os.chdir(wd)

if centroid == 't':
    os.chdir(f'{sd}{kic}_{centroid}/')
    np.savetxt(f'kic{kic}_f{factor}_centroids.dat', np.c_[x_cent,y_cent], fmt='%.5f')
    os.chdir(wd)
else:
    pass

### DATA HANDLING ###

# for amplitude summary plot
medbins = int(280 / 30)
bins = np.zeros(medbins)

newdim = regridded_base.shape[0]

time = masked[:,1]
flux = masked[:,2]

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
maxforplotting = np.max(ampls)

print(f'{kic} just the FITS files')

# for amplitudes summary plot
for j in range(medbins):
    bins[j] = np.median(ampls[(freqs > j*30) & (freqs <= (j+1)*30)])

os.chdir(f'{sd}{kic}_{centroid}/')
stardata = open(f'{kic}_{centroid}.dat', 'w')
stardata.write(f'Teff = {teff[kics==kic].values[0]:.0f} K\n')
stardata.write(f'high freq noise = {bins[-1]:.2f} ppm\n')
stardata.write(f'S/N = {max(ampls)/bins[-1]:.2f}\n')
stardata.write(f'Kp = {Kp}\n')
stardata.write(f'crowding magnitude = {mag}\n')
stardata.close()
os.chdir(wd)

print(f'{kic} FITS and dat but no figure')

cmap = pl.cm.Greys_r
maskcmap = cmap(np.arange(cmap.N))
maskcmap[:,-1] = np.linspace(1, 0, cmap.N)
maskcmap = ListedColormap(maskcmap)

fig = plt.figure(figsize=(15,10))
grid = gs.GridSpec(8,5, width_ratios=[1,2,1.5,1,1])

img = plt.subplot(grid[0:3,0])
amp = plt.subplot(grid[0:4,1])
pixels = plt.subplot(grid[4:,0:2])
first = plt.subplot(grid[0:2,2:])
smth = plt.subplot(grid[2:4,2:])
zoom = plt.subplot(grid[4:6,2:])
ft = plt.subplot(grid[6:,2:])

# star and mask
img.set_title(f'{kic}')
star = img.imshow(regridded_base, cmap='OrRd')
img.imshow(maskarr, cmap=maskcmap, alpha=0.5) # for one gaussian mask only
star.axes.get_xaxis().set_ticklabels([])
star.axes.get_yaxis().set_ticklabels([])
star.axes.get_xaxis().set_ticks([])
star.axes.get_yaxis().set_ticks([])
if np.isnan(teff[kics==kic].values[0]) == False:
    img.text(0.5, newdim+factor, r'T$_{eff}$'+f' = {teff[kics==kic].values[0]:.0f} K')
img.text(0.5, newdim+(factor*1.5), f'Kp = {Kp:.2f}')
img.text(0.5, newdim+(factor*2), f'high freq noise = {bins[-1]:.2f} ppm')
img.text(0.5, newdim+(factor*2.5), f'S/N = {max(ampls)/bins[-1]:.2f}')

# pixel plot
if 9 in quarterlist:
    temp_q = 9
else:
    temp_q = quarterlist[0] # grab first available quarter if no q9
exec("time_pix = time1_%d" % temp_q)
exec("flux_pix = flux1_%d" % temp_q)

masks = np.zeros((flux_pix.shape[1]*flux_pix.shape[2], flux_pix.shape[1], flux_pix.shape[2]), dtype='bool')
for i in range(flux_pix.shape[1]*flux_pix.shape[2]):
    masks[i][np.unravel_index(i, (flux_pix.shape[1], flux_pix.shape[2]))] = True

pixel_list = []
for j in range(flux_pix.shape[1]*flux_pix.shape[2]):
    flux_picked = [y for y in flux_pix[range(len(time_pix)), masks[j]]]
    lc = lk.LightCurve(time=time_pix, flux=flux_picked)
    try:
        pixel_list.append(lc.remove_nans().flatten().to_periodogram())
    except ValueError:
        pixel_list.append(None) # this error occurs when there are pixels missing and appending none is tantamount to putting a gap there
    except IndexError:
        pixel_list.append(None)

pixels.get_xaxis().set_ticks([])
pixels.get_yaxis().set_ticks([])
pixels.set(xlabel='Frequency', ylabel='Amplitude')

nested_grid = gs.GridSpecFromSubplotSpec(flux_pix.shape[1], flux_pix.shape[2], subplot_spec=grid[4:,0:2], wspace=0, hspace=0)
for k in range(flux_pix.shape[1]*flux_pix.shape[2]):
    if pixel_list[k]:
        x, y = np.unravel_index(k, (flux_pix.shape[1], flux_pix.shape[2]))
        gax = fig.add_subplot(nested_grid[x, y]) # just this should be fine since no flipping?
        gax.plot(pixel_list[k].frequency.value, pixel_list[k].power.value, 'k-', lw=0.5)

        gax.margins(y=.1, x=0)
        gax.set_xticklabels('')
        gax.set_yticklabels('')
        gax.set_xticks([])
        gax.set_yticks([])

# amplitude summary
amp.xaxis.set_major_locator(MaxNLocator(integer=True))
main = amp.scatter(range(medbins), bins, c='r', linewidths=0.5, edgecolors='k')
amp.set_xlabel('bin number')
amp.set_ylabel('median amplitude by bin (ppm)')

# raw flux
time = raw[:,1]
flux = raw[:,2]
for q in range(len(quarterlines)):
    first.axvline(x=quarterlines[q], color='red', linestyle='--', alpha=0.7)
first.plot(time, flux, 'k.', ms=3)
first.set_xlim(quarterlines[0], 1600)
first.set_xlabel('time (d)')
first.set_ylabel('flux')

# fitted flux
time = masked[:,1]
flux = masked[:,2]
smth.plot(time, flux, 'k.', ms=3)
smth.set_xlim(quarterlines[0], 1600)
smth.set_xlabel('time (d)')
smth.set_ylabel('normalised flux')

# fitted flux: zoomed
if 9 in emptyquarters: # default nice quarter to plot is 9, otherwise pick highest quarter to zoom in on
    qa = quarterlines[max(quarterlist)-1]
    qb = quarterlines[max(quarterlist)]
else:
    qa = quarterlines[9]
    qb = quarterlines[10]
zoom.plot(time[(time >= qa) & (time <= qb)], flux[(time >= qa) & (time <= qb)], 'k.', ms=3)
zoom.set_xlim(qa, qb)
zoom.set_xlabel('time (d)')
zoom.set_ylabel('normalised flux')

# amplitude spectrum
ft.loglog(freqs, ampls, 'k-', lw=0.5)
ft.set_xlim(0.1, 283)
ft.set_ylim(0.1, np.nanmax(maxforplotting)*1.1)
ft.set_xlabel(r'frequency ($\mu$Hz)')
ft.set_ylabel('amplitude (ppm)')

grid.tight_layout(fig)
os.chdir(f'{sd}{kic}_{centroid}/')
plt.savefig(f'kic{kic}_factor{factor}_{centroid}_summary.png')
os.chdir(wd)
if params.interactive == True:
    plt.show()
else:
    plt.close()

print(f'{kic} done')