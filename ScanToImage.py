import numpy as np
import cv2
import Nonrotate_Map as Nmap
from Nonrotate_Map import *
from scipy.interpolate import griddata
from skimage import data
from skimage.feature import match_template

def ScanToImg(txtscan_x, txtscan_y, txtscan_z):
    # Get the scan_x data
    pt = TwoD_nonrotate_map("Scan_x_L1","Scan_y_L1","Scan_z_L1")
    pt_scan,scan_x,scan_y,scan_z = pt.scan_coordinates()

    # Get the range of x and y
    x_max = max(scan_x)
    x_min = min(scan_x)
    y_max = max(scan_y)
    y_min = min(scan_y)
    z_max = max(scan_z)
    z_min = min(scan_z)

    # The number of array
    N_x = 100
    N_y = 100

    # Generate the scan image
    img = np.zeros([100,100])

    while (len(scan_z)<10001):
        scan_z.append(z_min)

    for flag_y in range(100):
        for flag_x in range(100):
            flag_z = flag_y * 100 + flag_x
            if (flag_y % 2 == 0): # even number
                img[flag_y][flag_x] = scan_z[flag_z]
            if (flag_y % 2 == 1): # odd number
                img[flag_y][99-flag_x] = scan_z[flag_z]

    #scale the image and normalized
    dist = np.zeros((100, 100))
    ScantoImage = cv2.normalize(-img, dist, 0, 255, cv2.NORM_MINMAX)
    plt.imshow(ScantoImage)
    plt.colorbar()
    Scan_img = ScantoImage
    return Scan_img
