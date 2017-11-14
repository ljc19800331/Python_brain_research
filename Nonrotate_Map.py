#This script: 2D perpendicular image registration based on cross-correlation
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import sys
import vtk

class TwoD_nonrotate_map:

    def __init__(self, txtscan_x, txtscan_y, txtscan_z):
        self.txtscan_x = txtscan_x
        self.txtscan_y = txtscan_y
        self.txtscan_z = txtscan_z

    #def Read_xyzcoordinates(self):

    def Brain_coordinates(self):
        brain_txtx = open("brain_x.txt", "r")
        brain_txty = open("brain_y.txt", "r")
        brain_txtz = open("brain_z.txt", "r")
        brain_x = []
        brain_y = []
        brain_z = []
        a_x = []
        a_y = []
        a_z = []
        for line in brain_txtx:
            a_x = line.split()
            brain_x.append(float(a_x[0]))
        brain_txtx.close()
        for line in brain_txty:
            a_y = line.split()
            brain_y.append(float(a_y[0]))
        brain_txty.close()
        for line in brain_txtz:
            a_z = line.split()
            brain_z.append(float(a_z[0]))
        brain_txtz.close()
        pt_brain = VtkPointCloud()
        for k in range(len(brain_x)):
            point = ([brain_x[k], brain_y[k], brain_z[k]])
            pt_brain.addPoint(point)
        return pt_brain, brain_x, brain_y, brain_z

    def scan_coordinates(self):
        # read the x y z coordinates from scan txt files
        sys.path.append('C:/Users/maguangshen/PycharmProjects/Brain research/scan_918/L1/')
        a_x = []
        a_y = []
        a_z = []
        # L1
        filename_x = self.txtscan_x
        scan_L1x = open(filename_x, "r")
        scan_x = []
        for line in scan_L1x:
            a_x = line.split()
            scan_x.append(float(a_x[0]))

        filename_y = self.txtscan_y
        scan_L1y = open(filename_y, "r")
        scan_y = []
        for line in scan_L1y:
            a_y = line.split()
            scan_y.append(float(a_y[0]))

        filename_z = self.txtscan_z
        scan_L1z = open(filename_z, "r")
        scan_z = []
        for line in scan_L1z:
            a_z = line.split()
            scan_z.append(float(a_z[0]))
        scan_L1x.close()
        scan_L1y.close()
        scan_L1z.close()

        pt_scan = VtkPointCloud()
        for k in range(len(scan_x)):
            point = ([scan_x[k], scan_y[k], scan_z[k]])
            pt_scan.addPoint(point)
        return pt_scan, scan_x, scan_y, scan_z

    def vtk_pt(self,pointCloud):
        # Renderer
        renderer = vtk.vtkRenderer()
        renderer.AddActor(pointCloud.vtkActor)
        renderer.SetBackground(.2, .3, .4)
        renderer.ResetCamera()

        # Render Window
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)

        # Interactor
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Begin Interaction
        renderWindow.Render()
        renderWindowInteractor.Start()

class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

if __name__ == '__main__':
    txtscan_x = input('The txt file name of x')
    txtscan_y = input('The txt file name of y')
    txtscan_z = input('The txt file name of z')
    pt = TwoD_nonrotate_map(txtscan_x,txtscan_y,txtscan_z)
    pt_scan,scan_x,scan_y,scan_z = pt.scan_coordinates()
    pt_brain,brain_x,brain_y,brain_z = pt.Brain_coordinates()
    pt.vtk_pt(pt_scan)
    pt.vtk_pt(pt_brain)