import Nonrotate_Map
from Nonrotate_Map import *
import cv2
import numpy as np
from scipy.interpolate import griddata
from skimage import data
from skimage.feature import match_template
import scipy

class Nonrotate_registration():

    def __init__(self, txtscan_x, txtscan_y, txtscan_z):
        self.txtscan_x = txtscan_x
        self.txtscan_y = txtscan_y
        self.txtscan_z = txtscan_z

    def ScanToImg(self):
        # Get the scan_x data
        pt = TwoD_nonrotate_map(self.txtscan_x, self.txtscan_y, self.txtscan_z)
        pt_scan, scangoog_x, scan_y, scan_z = pt.scan_coordinates()

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
        img = np.zeros([100, 100])

        while (len(scan_z) < 10001):
            scan_z.append(z_min)

        for flag_y in range(100):
            for flag_x in range(100):
                flag_z = flag_y * 100 + flag_x
                if (flag_y % 2 == 0):  # even number
                    img[flag_y][flag_x] = scan_z[flag_z]
                if (flag_y % 2 == 1):  # odd number
                    img[flag_y][99 - flag_x] = scan_z[flag_z]

        # scale the image and normalized
        dist = np.zeros((100, 100))
        ScantoImage = cv2.normalize(-img, dist, 0, 255, cv2.NORM_MINMAX)
        plt.imshow(ScantoImage)
        plt.colorbar()
        Scan_img = ScantoImage
        return Scan_img

    def BrainToImg(self):
        # Read the data
        pt = TwoD_nonrotate_map(self.txtscan_x, self.txtscan_y, self.txtscan_z)
        pt_scan, scan_x, scan_y, scan_z = pt.scan_coordinates()
        pt_brain, brain_x, brain_y, brain_z = pt.Brain_coordinates()
        brain_xarray = np.asarray(brain_x)
        brain_yarray = np.asarray(brain_y)
        points_brain = np.column_stack((brain_xarray, brain_yarray))
        values_brain = np.asarray(brain_z)

        # Get the range of x and y
        x_max = max(brain_x)
        x_min = min(brain_x)
        y_max = max(brain_y)
        y_min = min(brain_y)
        z_max = max(brain_z)
        z_min = min(brain_z)

        # Determine the number of pixels in x and y axis
        # define the geometric parameters of the brain model 8.6,11.8,1.27,100
        N_x = round(8.6 / 1.27 * 100)
        N_y = round(11.8 / 1.27 * 100)

        # Create the mesh grid mapping
        grid_x, grid_y = np.mgrid[0:x_max:x_max / N_x, 0:y_max:y_max / N_y]
        grid_z0 = -scipy.interpolate.griddata(points_brain, values_brain, (grid_x, grid_y), method='nearest')

        grid_ranges = [[0, x_max, x_max / N_x], [0, y_max, y_max / N_y], [0, x_max, x_max / N_x]]

        # flip the image for visualization
        grid_z2 = np.fliplr(np.flipud(grid_z0))
        Brain_img = np.rot90(grid_z2)

        # Viz the result
        fig = plt.figure()
        ax = plt.imshow(Brain_img)
        plt.colorbar()

        return Brain_img

    def ImageRegistration(self,Scan_img,Brain_img):
        #image registration and the result
        # Scan_img
        fig = plt.figure()
        ax = plt.imshow(Scan_img)
        # brain image
        fig = plt.figure()
        ax = plt.imshow(Brain_img)

        match_result = match_template(Brain_img, Scan_img)
        ij = np.unravel_index(np.argmax(match_result), match_result.shape)
        x, y = ij[::-1]

        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 3))

        ax1.imshow(Scan_img)
        ax1.set_axis_off()
        ax1.set_title('template')

        ax2.imshow(Brain_img)
        ax2.set_axis_off()
        ax2.set_title('image')
        # highlight matched region
        hcoin, wcoin = Scan_img.shape
        rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
        ax2.add_patch(rect)

        ax3.imshow(match_result)
        ax3.set_axis_off()
        ax3.set_title('`match_template`\n result')
        # highlight matched region
        ax3.autoscale(False)
        ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

        plt.show()
        x_center = x
        y_center = y

        return x_center, y_center