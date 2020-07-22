import numpy as np
import matplotlib.pyplot as plt
import sys
# import scipy.ndimage.measurements as ms

def centroid(timespan, fluxarr, mask):

    # inputs: length of flux array, flux array (3 dimensional), aperture mask for centroiding over only target

    x_cent = np.zeros(timespan)
    y_cent = np.zeros(timespan)
    # index = np.indices((fluxarr.shape[1],fluxarr.shape[2]))

    for i in range(timespan):
        xfsum = 0
        yfsum = 0
        fsum = 0
        temp = fluxarr[i,:]
        # print(temp.shape)

        # xfsum = sum(map((lambda x,y: x*y), index[1,:][np.where(mask==3)], temp[np.where(mask==3)]))
        # yfsum = sum(map((lambda x,y: x*y), index[0,:][np.where(mask==3)], temp[np.where(mask==3)]))
        # fsum = sum(temp[np.where(mask==3)]) # fsr the original way is faster?? ;__;
        for index, val in np.ndenumerate(temp):

            # cent = np.unravel_index(np.nanargmax(temp), temp.shape)

            # if np.isnan(val) == False:
            #    xfsum += index[1] * temp[index]
            #    yfsum += index[0] * temp[index]
            #    fsum += temp[index]
            if mask[index] == 3:
                xfsum += index[1] * temp[index]
                yfsum += index[0] * temp[index]
                fsum += temp[index]
            else:
                pass

        x_cent[i] = xfsum / fsum
        y_cent[i] = yfsum / fsum
        # x_cent[i] = cent[1]
        # y_cent[i] = cent[0]

        # if temp.shape[0] == 50:
        #    print(cent, x_cent[i], y_cent[i])
        #    if i == 100:
        #       sys.exit()

        # y_cent[i], x_cent[i] = ms.center_of_mass(temp)

        # if i == 1000:

        #    print(y_cent[i], x_cent[i])
         
        #    plt.figure(1)

        #    plt.imshow(temp)
        #    plt.plot(y_cent[i], x_cent[i], 'r*', ms=5)

        #    plt.show()


    return x_cent, y_cent


def centroid_nomask(timespan, fluxarr):

    # inputs: length of flux array, flux array (3 dimensional), aperture mask for centroiding over only target

    x_cent = np.zeros(timespan)
    y_cent = np.zeros(timespan)

    for i in range(timespan):
        xfsum = 0
        yfsum = 0
        fsum = 0
        temp = fluxarr[i,:]
        for index, val in np.ndenumerate(temp):

            xfsum += index[1] * temp[index]
            yfsum += index[0] * temp[index]
            fsum += temp[index]

        x_cent[i] = xfsum / fsum
        y_cent[i] = yfsum / fsum

    return x_cent, y_cent