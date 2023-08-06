# -*- coding: utf-8 -*-

"""

Program to interpolate fiber orientation tensors with the help of a 
decomposition method based on separate quaternion (orientation) and invariant 
(shape) weighting.

@author: juliane.blarr@kit.edu
2022

For more information please consider the following paper:
    
Blarr, J., Sabiston, T., Krauß, C. et al. Implementation and comparison of 
algebraic and machine learning based tensor interpolation methods applied to 
fiber orientation tensor fields obtained from CT images. 
Computational Materials Science 2023.

Please cite this paper if you use this code.

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

def point_output_deco(invariants,quaternions,x_value,y_value):
    
    """
    Calculates the interpolated tensor at a specific point.
    Interpolation via the decomposition method.
    Abbreviation 'deco' for 'decomposition'.
    """
    
    weights = weighting(x_value, y_value, invariants)
    
    Inv = np.zeros(3)
    for i in [0,1,2]:
        args = {}
        for j in invariants:
            args[j]= invariants[j][i]
        Inv[i] = interpolation(args,weights)
    Lambda = EV(Inv)
    
    Q = np.zeros(4)
    for i in [0,1,2,3]:
        args = {}
        for j in quaternions:
            args[j]= quaternions[j][i]
        Q[i] = interpolation(args,weights)
    Q = Q/np.linalg.norm(Q) 
    
    R = rotation_matrix(Q)
    
    orientation_tensor = matrix_de_decomposition(Lambda,R)
    return orientation_tensor


def weighting(x_value, y_value, invariants):
    
    """
    Calculates the weights for a given point.
    Uses Shepard's method with p = 2.
    """
    
    distances = {}
    weights = {}
    for i in invariants:
        distance = np.sqrt((i[0]-x_value)**2 + (i[1]-y_value)**2)
        distances[i] = distance
    total = 0
    for i in distances:
        total += distances[i]**(-2)
    for i in invariants:
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

def eigendecomposition(A):
    
    """
    Calculates the linear invariants (K1,R2,R3) and the rotation matrix R.
    """
    
    EV, R = np.linalg.eig(A)
    invariants = invariantization(A)
    #Sorting the Eigenvalues and the Rotation matrix
    R2 = np.zeros((3,3))
    if EV[0] >= EV[1] and EV[0] >= EV[2]:
        R2[:,0] = R[:,0]
        if EV[1]>=EV[2]:
            R2[:,1] = R[:,1]
            R2[:,2] = R[:,2]
        else:
            R2[:,1] = R[:,2]
            R2[:,2] = R[:,1]
    elif EV[0] >= EV[1] and EV[0] < EV[2]:
        R2[:,0] = R[:,2]
        R2[:,1] = R[:,0]
        R2[:,2] = R[:,1]
    elif EV[0] >= EV[2] and EV[0] < EV[1]:
        R2[:,0] = R[:,1]
        R2[:,1] = R[:,0]
        R2[:,2] = R[:,2]
    elif EV[1] >= EV[2]:
        R2[:,0] = R[:,1]
        R2[:,1] = R[:,2]
        R2[:,2] = R[:,0]
    else:
        R2[:,0] = R[:,2]
        R2[:,1] = R[:,1]
        R2[:,2] = R[:,0]
    return (invariants, R2)

def invariantization(A):
    
    """
    Calculates the linear invariants of a tensor of second order.
    """
    
    K1 = np.trace(A)
    ADev = A - K1/3*np.eye(3)
    ADev_absolute = np.linalg.norm(ADev)
    R2 = np.sqrt(3/2) * ADev_absolute / np.linalg.norm(A)
    R3 = 3*np.sqrt(6)* np.linalg.det(ADev)/(ADev_absolute**3)
    return np.array([K1, R2, R3])

def EV(invariants):
    
    """
    Calculates the eigenvalue tensor from the invariants.
    """
    
    K1, R2, R3 = invariants
    L1 = K1/3 + 2*K1*R2/3/np.sqrt(3-2*R2**2)*np.cos(np.arccos(R3)/3)
    L2 = K1/3 + 2*K1*R2/3/np.sqrt(3-2*R2**2)*np.cos((np.arccos(R3)-2*np.pi)/3)
    L3 = K1/3 + 2*K1*R2/3/np.sqrt(3-2* R2**2)*np.cos((np.arccos(R3)+2*np.pi)/3)
    np.array([L1,L2,L3])
    return np.diag(np.array([L1,L2,L3]))

def matrix_de_decomposition(Lambda,R):
    return R.dot(Lambda).dot(R.T)

def quaternion(R):
    
    """
    Converts the rotation matrix into a quaternion.
    """
    
    t = np.trace(R)
    r = np.sqrt(1+t)
    w = r/2
    x = sgn(R[2][1]-R[1][2])*abs(1/2*np.sqrt(1+R[0][0]-R[1][1]-R[2][2]))
    y= sgn(R[0][2]-R[2][0])*abs(1/2*np.sqrt(1-R[0][0]+R[1][1]-R[2][2]))
    z= sgn(R[1][0]-R[0][1])*abs(1/2*np.sqrt(1-R[0][0]-R[1][1]+R[2][2]))
    Q = np.array([w,x,y,z])
    return Q


def rotation_matrix(Q):
    
    """
    Converts a quaternion back into a rotation matrix.
    """
    
    a = Q[0]
    b = Q[1]
    c = Q[2]
    d = Q[3]
    R = np.array([[a**2 +b**2-c**2-d**2, 2*(b*c-a*d), 2*(b*d + a*c)],
                  [2*(b*c + a*d), a**2 -b**2+c**2-d**2, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a**2 -b**2-c**2+d**2]])
    return R

def sgn(x):
    
    """
    Sign function.
    """
    
    if x > 0:
        r = 1
    elif x == 0:
        r = 0
    else:
        r = -1
    return r


if __name__ == "__main__":

    """
    The purpose of this script is to interpolate fiber orientation tensors (FOT).
    It starts by reading in a .txt-file with FOT and their respective positions.

    The tensors get split into a shape and an orientation part.
    The 'shape of the tensor' is represented by three invariants. The 'orientation
    of the tensor' is represented by a quaternion. A quaternion consists of four numbers,
    representing the rotation axis and the angle of rotation.

    For the interpolation, a distance based weighting is used. The three invariants and the
    four values of the quaternion are interpolated separatly. From the seven new values a
    new FOT is created.

    The tensors (original and interpolated) are written in a MATLAB-file.

    The MATLAB-file is used to then visualize the FOT field via tensor glyphs using the 
    method by Barmpoutis (cited in the paper of Blarr et al.).
    """


    """
    Reading the .txt-file and saving the coordinates as keys and the tensors 
    as values of a dictionary.
    """
    measured_values = {}
    with open("example//input_file_FOT.txt", "r", encoding="utf-8") as f1:
        #print(Datei.read())
        list1 = f1.read().split('\n\n')
        for i in list1:
            coord, tensor = reading(i)
            measured_values[coord] = tensor
               
    invariants = {}
    quaternions = {}
        
    """
    Processing the information from the .txt.-file.
    """
    
    for i in measured_values:
        Inv, R =eigendecomposition(measured_values[i])
        invariants[i] = Inv
        if np.linalg.det(R) <0:
            R *=-1
        Q = quaternion(R)
        K = np.zeros(4)
        for j in (0,1,2,3):
            K[j] = abs(Q[j])
        if Q[np.argmax(K)] < 0:
            Q = -Q
        quaternions[i] = Q
    
    """
    Defining the output field and naming the output-file.
    """
    filename = input("Name of the outputfile: ")
    xmin = int(input("Lower X limit: "))
    xmax = int(input("Upper X limit: "))
    ymin = int(input("Lower Y limit: "))
    ymax = int(input("Upper Y limit: "))
    
        
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
                    A = point_output_deco(invariants,quaternions,i,j)
                    line = "A(:,:,{},{}) = [{} {} {}; {} {} {}; {} {} {}]".format(i,j,A[0][0],A[0][1],A[0][2],A[1][0],A[1][1],A[1][2],A[2][0],A[2][1],A[2][2])
                    print(line, file=f)
        #Last commands
        print("", file=f)
        print("%Plotting", file=f)
        print("plotDTIcolor(A,KO)", file=f)

    