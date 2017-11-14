import sys
import pylab
import cv2
import numpy as np
import Nonrotate_Map as Nmap
from Nonrotate_Map import *
from scipy.interpolate import griddata
import scipy
import matplotlib.pyplot as plt

def BrainToImg(txtscan_x, txtscan_y, txtscan_z):
    #Read the data
    pt = TwoD_nonrotate_map("Scan_x_L1","Scan_y_L1","Scan_z_L1")
    pt_scan,scan_x,scan_y,scan_z = pt.scan_coordinates()
    pt_brain,brain_x,brain_y,brain_z = pt.Brain_coordinates()
    brain_xarray = np.asarray(brain_x)
    brain_yarray = np.asarray(brain_y)
    points_brain = np.column_stack((brain_xarray,brain_yarray))
    values_brain = np.asarray(brain_z)

    #Get the range of x and y
    x_max = max(brain_x)
    x_min = min(brain_x)
    y_max = max(brain_y)
    y_min = min(brain_y)
    z_max = max(brain_z)
    z_min = min(brain_z)

    #Determine the number of pixels in x and y axis
    # define the geometric parameters of the brain model 8.6,11.8,1.27,100
    N_x = round(8.6/1.27*100)
    N_y = round(11.8/1.27*100)

    #Create the mesh grid mapping
    grid_x, grid_y = np.mgrid[0:x_max:x_max/N_x, 0:y_max:y_max/N_y]
    grid_z0 = -scipy.interpolate.griddata(points_brain, values_brain, (grid_x, grid_y), method='nearest')

    grid_ranges = [[0, x_max, x_max/N_x], [0, y_max, y_max/N_y], [0, x_max, x_max/N_x]]

    # flip the image for visualization
    grid_z2 = np.fliplr(np.flipud(grid_z0))
    Brain_img = np.rot90(grid_z2)

    # Viz the result
    fig = plt.figure()
    ax = plt.imshow(Brain_img)
    plt.colorbar()

    return Brain_img
