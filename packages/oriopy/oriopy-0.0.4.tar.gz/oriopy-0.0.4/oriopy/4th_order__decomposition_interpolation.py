# -*- coding: utf-8 -*-

"""

Program for fiber orientation interpolation of tensors of fourth order.

Interpolation of the eigenvalues and determination of the rotation matrix R 
by Euclidean averaging of the measured values.

@author: juliane.blarr@kit.edu

For more information please consider the following paper:
    
Blarr, J., Sabiston, T., Krauß, C. et al. Implementation and comparison of 
algebraic and machine learning based tensor interpolation methods applied to 
fiber orientation tensor fields obtained from CT images. 
Computational Materials Science 2023.

Please cite this paper if you use this code.

"""

import numpy as np


def reading_4th(info):
    
    """
    Returns the coordinates and 4th order orientation tensors in Mandel 
    notation.
    """
    
    tensor = np.zeros((6,6))
    list = info.split('\n')
    
    coordstr = list[0].split(': ')[1]
    coordlst = coordstr.split(', ')
    coord = (float(coordlst[0]), float(coordlst[1]))

    line = list[1].split(' ')   
    tensor[0][0] = float(line[14])
    tensor[0][1] = tensor[1][0] = float(line[11])
    tensor[0][2] = tensor[2][0] = float(line[9])
    tensor[1][1] = float(line[4])
    tensor[1][2] = tensor[2][1] = float(line[2])
    tensor[2][2] = float(line[0])
    tensor[3][3] = 2*float(line[2])
    tensor[3][4] = tensor[4][3] = 2*float(line[6])
    tensor[3][5] = tensor[5][3] = 2*float(line[7])
    tensor[4][4] = 2*float(line[9])
    tensor[4][5] = tensor[5][4] = 2*float(line[10])
    tensor[5][5] = 2*float(line[11])
    tensor[0][3] = tensor[3][0] = np.sqrt(2)*float(line[10])
    tensor[0][4] = tensor[4][0] = np.sqrt(2)*float(line[12])
    tensor[0][5] = tensor[5][0] = np.sqrt(2)*float(line[13])
    tensor[1][3] = tensor[3][1] = np.sqrt(2)*float(line[3])
    tensor[1][4] = tensor[4][1] = np.sqrt(2)*float(line[7])
    tensor[1][5] = tensor[5][1] = np.sqrt(2)*float(line[8])
    tensor[2][3] = tensor[3][2] = np.sqrt(2)*float(line[1])
    tensor[2][4] = tensor[4][2] = np.sqrt(2)*float(line[5])
    tensor[2][5] = tensor[5][2] = np.sqrt(2)*float(line[6])
    
    return(coord, tensor)

def point_output_4th(Eigenvalues,measured_values,x_value,y_value):
    
    """
    Returns the interpolated 4th order tensor at a point.
    Interpolation via the decomposition method for tensors of fourth order.
    """
    
    weights = weighting(x_value, y_value, measured_values)
    
    EV = np.zeros(6)
    for i in [0,1,2,3,4,5]:
        args = {}
        for j in Eigenvalues:
            args[j]= Eigenvalues[j][i]
        EV[i] = interpolation(args,weights)
    Lambda = np.diag(EV)
    
    euclidean = np.zeros((6,6))
    for i in [0,1,2,3,4,5]:
        for k in [0,1,2,3,4,5]:
            args = {}
            for j in measured_values:
                args[j]= measured_values[j][i][k]
            euclidean[i][k] = interpolation(args,weights)
    Eigenvalues_euk,R = eigendecomposition_4th(euclidean)
    
    #print(R)
    
    Orientierungstensor = matrix_de_decomposition(Lambda,R)
    return Orientierungstensor


def weighting(x_value, y_value, measured_values):
    
    """
    Calculates the weights for given coordinates.
    Uses: Shepard's method with p = 2.
    """
    
    distances = {}
    weights = {}
    for i in measured_values:
        distance = np.sqrt((i[0]-x_value)**2 + (i[1]-y_value)**2)
        distances[i] = distance
    ges = 0
    for i in distances:
        ges += distances[i]**(-2)
    for i in measured_values:
        w = distances[i]**(-2)/ges
        weights[i] = w
    return weights

def interpolation(args,weights):

    """
    Calculates interpolated value.
    """
    
    total = 0
    for i in args:
        total += weights[i]*args[i]
    return total

def eigendecomposition_4th(A):
    
    """
    Returns the eigenvalues and the rotation matrix (eigenvector tensor) R.
    """
    
    EV, R = np.linalg.eig(A)
    #sort EV
    idx = EV.argsort()[::-1]   
    EV = EV[idx]
    R = R[:,idx]
    return (EV, R)


def matrix_de_decomposition(Lambda,R):
    return R.dot(Lambda).dot(R.T)



if __name__ == "__main__":

    """
    The purpose of this script is to interpolate fiber orientation tensors of 
    fourth order (FOT). It starts by reading in a .txt-file with the FOT and 
    their respective positions in a plate.

    The tensors get split into a shape and an orientation part. In the case
    of the fourth order tensors, the tensors are decomposed into their
    Eigenvalues as invariants (shape) and their Eigenvectors in form of
    the rotation matrix R (orientation).

    For the interpolation, a distance based weighting is used. The Eigenvalues
    and the Eigenvectors are interpolated separatly. An interpolated, new
    tensor is created from the weighted values.

    The tensors (original and interpolated) are written in a MATLAB-file.

    The MATLAB-file is used to then visualize the FOT field via tensor 
    glyphs using the method by Barmpoutis (cited in the paper of Blarr et al.).
    """
    
    
    """
    Reading the .txt-file and saving the coordinates as keys and the tensors 
    as values of a dictionary.
    """

    measured_values = {}
    with open("example//input_file_FOT_4th_order.txt", "r", encoding="utf-8") as Datei:
        #print(Datei.read())
        list = Datei.read().split('\n\n')
        for i in list:
            coord, tensor = reading_4th(i)
            measured_values[coord] = tensor

            
    Eigenvalues = {}
    
    for i in measured_values:
        EV,R = eigendecomposition_4th(measured_values[i])
        Eigenvalues[i] = EV
        

    """
    Defining the output field and naming the output-file.
    """

    filename = input("Name der Datei: ")
    xmin = int(input("Unterer X-Wert: "))
    xmax = int(input("Oberer X-Wert: "))
    ymin = int(input("Unterer Y-Wert: "))
    ymax = int(input("Oberer X-Wert: "))
    

    """
    Writing the MATLAB-file.
    """
    
    filename += ".m"
    with open(filename, 'w') as f:
        print("clear", file=f)
        print("", file=f)
        print("%Original tensors", file=f)
        #Printing the original (measured) tensors
        KO = "KO = {"
        for i in measured_values:
            A = measured_values[i]
            x = int(i[0])
            y = int(i[1])
            line = "A(:,:,{},{}) = [ {} {} {} {} {} {};\n               {} {} {} {} {} {};\n".format(x,y,A[0][0],A[0][1],A[0][2],A[0][3],A[0][4],A[0][5],A[1][0],A[1][1],A[1][2],A[1][3],A[1][4],A[1][5])
            line += "               {} {} {} {} {} {};\n               {} {} {} {} {} {};\n".format(A[2][0],A[2][1],A[2][2],A[2][3],A[2][4],A[2][5],A[3][0],A[3][1],A[3][2],A[3][3],A[3][4],A[3][5])
            line += "               {} {} {} {} {} {};\n               {} {} {} {} {} {}]".format(A[4][0],A[4][1],A[4][2],A[4][3],A[4][4],A[4][5],A[5][0],A[5][1],A[5][2],A[5][3],A[5][4],A[5][5])
            print(line, file=f)
            coord = "[{},{}],".format(x,y)
            KO += coord
        print("", file=f)
        print("%Coordinates of the original tensors", file=f)
        KO = KO[0:-1]+"}"
        print(KO, file=f)
        print("", file=f)
        print("%Interpolated tensors", file=f)
        #Interpolating and printing the tensors
        for i in range(xmin,xmax+1):
            for j in range(ymin,ymax+1):
                test = (i,j)
                if test not in measured_values:
                    A = point_output_4th(Eigenvalues,measured_values,i,j)
                    line = "A(:,:,{},{}) = [ {} {} {} {} {} {};\n               {} {} {} {} {} {};\n".format(i,j,A[0][0],A[0][1],A[0][2],A[0][3],A[0][4],A[0][5],A[1][0],A[1][1],A[1][2],A[1][3],A[1][4],A[1][5])
                    line += "               {} {} {} {} {} {};\n               {} {} {} {} {} {};\n".format(A[2][0],A[2][1],A[2][2],A[2][3],A[2][4],A[2][5],A[3][0],A[3][1],A[3][2],A[3][3],A[3][4],A[3][5])
                    line += "               {} {} {} {} {} {};\n               {} {} {} {} {} {}]".format(A[4][0],A[4][1],A[4][2],A[4][3],A[4][4],A[4][5],A[5][0],A[5][1],A[5][2],A[5][3],A[5][4],A[5][5])
                    print(line, file=f)
        #Last commands
        print("", file=f)
        print("%Plotting", file=f)
        print("plot_4d(A,KO)", file=f)