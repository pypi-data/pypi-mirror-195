"""
RSA 25/2/23

This class handles 3d matrices
"""

import math
import numpy as np

# class interface
from . import vectorthree as v3

class MatrixThree(object):
    def __init__(self, vals = [0,0,0,0,0,0,0,0,0]):
        self.matrix = vals
        self.newver = True
        self.npy = np.zeros((3,3))
        self.npy[0,0] = vals[0]
        self.npy[0,1] = vals[1]
        self.npy[0,2] = vals[2]
        self.npy[1,0] = vals[3]
        self.npy[1,1] = vals[4]
        self.npy[1,2] = vals[5]
        self.npy[2,0] = vals[6]
        self.npy[2,1] = vals[7]
        self.npy[2,2] = vals[8]

        
    def get_inverse(self):
        ############################### https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html
        if self.newver:
            try:
                from numpy.linalg import inv   
                from numpy.linalg import det
                minv = inv(self.npy)
                m3inv = MatrixThree(minv.reshape(9))
                return m3inv
            except:
                print("!!!!!! error", self.get_key(), det(self.npy))
            return None
        ###############################
        else:
            detWhole = self.get_determinant()
            transp = []
            transp.append(self.matrix[0])
            transp.append(self.matrix[3])
            transp.append(self.matrix[6])
            transp.append(self.matrix[1])
            transp.append(self.matrix[4])
            transp.append(self.matrix[7])
            transp.append(self.matrix[2])
            transp.append(self.matrix[5])
            transp.append(self.matrix[8])

            transpose = MatrixThree(transp)
            matinverse = MatrixThree()
            matinverseSwitch = MatrixThree()

            factor = 1;

            for i in range(3):        
                for j in range(3):            
                    thisValue = transpose.get_value(i, j)
                    detReduced = transpose.get_inner_determinant(i, j)
                    matinverse.put_value(detReduced * factor / detWhole, i, j)
                    factor *= -1
            return matinverse
        
    def get_determinant(self):        
        if self.newver:
            #################################
            from numpy.linalg import det
            return det(self.npy.transpose())
            #################################
        else:
            factor = -1
            det = 0
            for i in range(3):        
                factor = factor * -1
                row_val = self.matrix[3 * i]
                newdet = self.get_inner_determinant(i, 0)
                det = det + (factor * row_val * newdet)
            return det
    

    def get_inner_determinant(self, col, row):        
        smallMat = []
        if (col == 0):         
            if (row != 0):
                smallMat.append(self.matrix[1])
                smallMat.append(self.matrix[2])                
            if (row != 1):            
                smallMat.append(self.matrix[4])
                smallMat.append(self.matrix[5])            
            if (row != 2):            
                smallMat.append(self.matrix[7])
                smallMat.append(self.matrix[8])                        
        elif (col == 1):        
            if (row != 0):
                smallMat.append(self.matrix[0])
                smallMat.append(self.matrix[2])            
            if (row != 1):            
                smallMat.append(self.matrix[3])
                smallMat.append(self.matrix[5])            
            if (row != 2):            
                smallMat.append(self.matrix[6])
                smallMat.append(self.matrix[8])                    
        else: #(col == 1)        
            if (row != 0):
                smallMat.append(self.matrix[0])
                smallMat.append(self.matrix[1])            
            if (row != 1):            
                smallMat.append(self.matrix[3])
                smallMat.append(self.matrix[4])            
            if (row != 2):            
                smallMat.append(self.matrix[6])
                smallMat.append(self.matrix[7])                    
        n11 = smallMat[0]
        n12 = smallMat[1]
        n21 = smallMat[2]
        n22 = smallMat[3]
        return n11 * n22 - n12 * n21
        
    
    def get_value(self, row, col):        
        if self.newver:
            return self.npy[row,col]
        else:
            pos = row * 3 + col
            return self.matrix[pos]
            
        
        
    def put_value(self, val, row, col):    
        pos = row * 3 + col
        self.npy[row,col] = val
        self.matrix[pos] = val

    
    
    def multiply(self, col, byRow):
        ###################################### https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
        if self.newver:
            if byRow:
                mm= np.matmul(self.npy.transpose(), col.npy)
            else:
                mm= np.matmul(self.npy, col.npy)
                            
            vv = mm.reshape(3)
            vm3 = v3.VectorThree(vv[0],vv[1],vv[2])
            return vm3
        else:
            ######################################
            #So, this is by row not by column, or,,, anyway which is which...
            col0 = col.A
            col1 = col.B
            col2 = col.C
            scaled = v3.VectorThree()

            if byRow:
                poses = [0,1,2,3,4,5,6,7,8]
            else:
                poses = [0,3,6,1,4,7,2,5,8]
            s0 = col0 * self.matrix[poses[0]]
            s1 = col0 * self.matrix[poses[1]]
            s2 = col0 * self.matrix[poses[2]]
            s0 += col1 * self.matrix[poses[3]]
            s1 += col1 * self.matrix[poses[4]]
            s2 += col1 * self.matrix[poses[5]]
            s0 += col2 * self.matrix[poses[6]]
            s1 += col2 * self.matrix[poses[7]]
            s2 += col2 * self.matrix[poses[8]]
            scaled.put_by_idx(0, s0)
            scaled.put_by_idx(1, s1)
            scaled.put_by_idx(2, s2)
            return scaled

    def get_key(self):
        return str(self.matrix)

    
        