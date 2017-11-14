# Test the 3D rigid transform algorithm

import os

#data_path = 'C:/Users/maguangshen/PycharmProjects/Brain research/vtkBodyScan/brain data files'

import vtk
import numpy
from stl import mesh

def ReadStl(filename):
    your_mesh = mesh.Mesh.from_file(filename)
    return your_mesh

def readstl(filename):

    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)

    mapper = vtk.vtkPolyDataMapper()

    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(reader.GetOutput())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # Create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Assign actor to the renderer
    ren.AddActor(actor)

    # Enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()

def main():
    filename = 'brain_slice.stl'
    #readstl(filename)
    mesh = ReadStl(filename)

if __name__ == '__main__':
    main()

