# -*- coding: utf-8 -*-

"""
Program to interpolate fiber orientation tensors with the component averaging 
method.

@author: juliane.blarr@kit.edu
2022

For more information please consider the following paper:
    
Blarr, J., Sabiston, T., Krauß, C. et al. Implementation and comparison of 
algebraic and machine learning based tensor interpolation methods applied to 
fiber orientation tensor fields obtained from CT images. 
Computational Materials Science 2023.

"""

import numpy as np

"""
Self-implemented methods
"""

        
def reading(info):
    
    """
    Reads the coordinates and tensors.
    """
    
    tensor = np.zeros((3,3))
    content_list = info.split('\n')
    
    coordstr = content_list[0].split(': ')[1]
    coordlst = coordstr.split(', ')
    coord = (float(coordlst[0]), float(coordlst[1]))
    
    for i in [1,2,3]:
        j = i-1
        line = content_list[i].split('  ')
        for k in [0,1,2]:
            tensor[j][k]= float(line[k+1])
            
    return(coord, tensor)

def point_output_ca(tensor,xwert,ywert):
    
    """
    Calculates the interpolated tensor at a specific point.
    Interpolation via the component averaging (Euclidean) method.
    Abbreviation 'ca' for 'component averaging'.
    """
    
    weights = weighting(xwert, ywert, measured_values)
    #print ("Gewichte: ", weights)
    
    X = np.zeros([3,3])
    for i in [0,1,2]:
        args = {}
        for j in measured_values:
            args[j]= measured_values[j][i]

        X[i] = interpolation(args,weights)

    Orientierungstensor = X
    return Orientierungstensor

def weighting(x_value, y_value, values):
    
    """
    Calculates the weights for a given point
    Uses Shepard's method with p = 2.
    """
    
    distances = {}
    weights = {}
    for i in values:
        distance = np.sqrt((i[0]-x_value)**2 + (i[1]-y_value)**2)
        distances[i] = distance
    total = 0
    for i in distances:
        total += distances[i]**(-2)
    for i in values:
        w = distances[i]**(-2)/total
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



if __name__ == "__main__":

    """
    The purpose of this script is to interpolate fiber orientation tensors (FOT).
    It starts by reading in a .txt-file with FOT and its belonging position.
    
    Each tensor for a new position is then calculated by a weighted average of the 
    components of the measured, existing FOT.
    The weights are chosen by Shepard's inverse distance weighting.
    
    The tensors (original and interpolated) are written in a MATLAB-file.
    
    The MATLAB-file is used to then visualize the FOT field via tensor glyphs using 
    the method by Barmpoutis (cited in the paper of Blarr et al.).
    """
    
    
    """
    Reading in the .txt-file and saving the coordinates as keys and the 
    tensors as values of a dictionary.
    """
    measured_values = {}
    with open("example//input_file_FOT.txt", "r", encoding="utf-8") as f1:
        #print(Datei.read())
        list1 = f1.read().split('\n\n')
        for i in list1:
            coord, tensor = reading(i)
            measured_values[coord] = tensor
                
    
    """
    Defining the output field and naming the output-file.
    """
    filename = input("Name of the outputfile: ")
    xmin = int(input("Lower X limit: "))
    xmax = int(input("Upper X limit: "))
    ymin = int(input("Lower Y limit: "))
    ymax = int(input("Upper Y limit: "))
        
    """
    Writing the MATLAB-File.
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
            line = "A(:,:,{},{}) = [{} {} {}; {} {} {}; {} {} {}]".format(x,y,A[0][0],A[0][1],A[0][2],A[1][0],A[1][1],A[1][2],A[2][0],A[2][1],A[2][2])
            print(line, file=f)
            Koord = "[{},{}],".format(x,y)
            KO += Koord
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
                    A = point_output_ca(measured_values,i,j)
                    line = "A(:,:,{},{}) = [{} {} {}; {} {} {}; {} {} {}]".format(i,j,A[0][0],A[0][1],A[0][2],A[1][0],A[1][1],A[1][2],A[2][0],A[2][1],A[2][2])
                    print(line, file=f)
        #Last commands
        print("", file=f)
        print("%Plotting", file=f)
        print("plotDTIcolor(A,KO)", file=f)
        