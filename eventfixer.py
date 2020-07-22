import numpy as np

def fixer(q, time, flux, cluster):

    # qtol = 0.5 # how many days to clip at either side of each quarter

    # clip beginning and end of quarter
    # time = np.delete(time, np.where(time >= np.nanmax(time) - qtol))
    # time = np.delete(time, np.where(time <= np.nanmin(time) + qtol))
    # flux = np.delete(flux, np.where(time >= np.nanmax(time) - qtol))
    # flux = np.delete(flux, np.where(time <= np.nanmin(time) + qtol))

    # events = [183, 231, 323.5, 399, 430, 567, 599, 689, 763, 887, 937, 969, 1032, 1062, 1070, 1160, 1294, 1306, 1336, 1418, 1488, 1526, 1586] # to cut 4 days from start of event
    # qs = [2, 2, 3, 4, 4, 6, 6, 7, 8, 9, 10, 10, 11, 11, 11, 12, 14, 14, 14, 15, 16, 16, 17] # quarter corresponding to event
    events = [160.3, 181.6, 214.63, 230.4, 254.5, 291, 322, 352.35, 372.9, 383.8, 396.2, 443.3, 476, 504, 538, 567, 598.5, 630, 656.3, 660.5, 690.6, 718.04, 735, 762, 805, 845, 906.5, 937, 969.3, 1063.6, 1126.5, 1154.5, 1182.5, 1215.5, 1273.5, 1305.5, 1336.5, 1415.5, 1435.8, 1471.6]
    qs = [1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 9, 10, 10, 10, 11, 12, 13, 14, 14, 15, 15, 15, 16, 16, 17] # quarter corresponding to event
    cut = [13.7, 6.4, 2.17, 3.1, 9.5, 2.41, 5, 2.46, 1.3, 2.2, 0.7, 2.2, 2, 2, 12, 3, 3.5, 5, 7.1, 1.14, 2.4, 6.96, 5, 4, 6, 3, 5.5, 3.6, 3, 1.9, 2.4, 3, 3.5, 3.25, 1.5, 3, 3.5, 4.5, 1.2, 8.4] # how much to cut from start of event
    # if cluster == 6791: # may add this in later but for now only made it worse
    #    events.extend([1403.3, 1410.2, 1419.5, 1434.4])
    #    qs.extend([15, 15, 15, 15])
    #    cut.extend([3.5, 2, 2, 4.5])
    # if cluster == 6819:
    #    events.append()
    #    qs.append()
    #    cut.append()   

    # clip individual safe modes etc... hardcoded
    for i in range(len(qs)):
        if q == qs[i]:
            flux = np.concatenate((flux[np.where(time <= events[i])], flux[np.where(time >= events[i]+cut[i])]))
            time = np.concatenate((time[np.where(time <= events[i])], time[np.where(time >= events[i]+cut[i])]))
        else:
            pass

    return time, flux

def fixer_c(q, cadence, time, flux, cluster):

    # qtol = 0.5 # how many days to clip at either side of each quarter

    # clip beginning and end of quarter
    # time = np.delete(time, np.where(time >= np.nanmax(time) - qtol))
    # time = np.delete(time, np.where(time <= np.nanmin(time) + qtol))
    # flux = np.delete(flux, np.where(time >= np.nanmax(time) - qtol))
    # flux = np.delete(flux, np.where(time <= np.nanmin(time) + qtol))

    # events = [183, 231, 323.5, 399, 430, 567, 599, 689, 763, 887, 937, 969, 1032, 1062, 1070, 1160, 1294, 1306, 1336, 1418, 1488, 1526, 1586] # to cut 4 days from start of event
    # qs = [2, 2, 3, 4, 4, 6, 6, 7, 8, 9, 10, 10, 11, 11, 11, 12, 14, 14, 14, 15, 16, 16, 17] # quarter corresponding to event
    events = [160.3, 181.6, 214.63, 230.4, 254.5, 291, 322, 352.35, 372.9, 383.8, 396.2, 443.3, 476, 504, 538, 567, 598.5, 630, 656.3, 660.5, 690.6, 718.04, 735, 762, 805, 845, 906.5, 937, 969.3, 1063.6, 1126.5, 1154.5, 1182.5, 1215.5, 1273.5, 1305.5, 1336.5, 1415.5, 1435.8, 1471.6]
    qs = [1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 9, 10, 10, 10, 11, 12, 13, 14, 14, 15, 15, 15, 16, 16, 17] # quarter corresponding to event
    cut = [13.7, 6.4, 2.17, 3.1, 9.5, 2.41, 5, 2.46, 1.3, 2.2, 0.7, 2.2, 2, 2, 12, 3, 3.5, 5, 7.1, 1.14, 2.4, 6.96, 5, 4, 6, 3, 5.5, 3.6, 3, 1.9, 2.4, 3, 3.5, 3.25, 1.5, 3, 3.5, 4.5, 1.2, 8.4] # how much to cut from start of event
    # if cluster == 6791: # may add this in later but for now only made it worse
    #    events.extend([1403.3, 1410.2, 1419.5, 1434.4])
    #    qs.extend([15, 15, 15, 15])
    #    cut.extend([3.5, 2, 2, 4.5])
    # if cluster == 6819:
    #    events.append()
    #    qs.append()
    #    cut.append()   

    # clip individual safe modes etc... hardcoded
    for i in range(len(qs)):
        if q == qs[i]:
            flux = np.concatenate((flux[np.where(time <= events[i])], flux[np.where(time >= events[i]+cut[i])]))
            cadence = np.concatenate((cadence[np.where(time <= events[i])], cadence[np.where(time >= events[i]+cut[i])]))
            time = np.concatenate((time[np.where(time <= events[i])], time[np.where(time >= events[i]+cut[i])]))
        else:
            pass

    return cadence, time, flux