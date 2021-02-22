from torch import sum,FloatTensor
import numpy as np


def extract_features(image_tensor)  :
    pixels = image_tensor.size()   
    cell_division = (4,4)       #la division des images par cellule
    image_tensor_float = image_tensor.float()
    N = sum(image_tensor_float).item()
    #print("N : {}".format(N))
    cell_list = []
    vertical_step = pixels[1]//cell_division[1]
    #print(vertical_step)
    horizontal_step = pixels[0]//cell_division[0]
    #print(horizontal_step)
    for i in range (0, pixels[1], vertical_step) :          #iteration verticale de cellules 
        for j in range (0, pixels[0], horizontal_step) :    #iteration horizontale de cellules
            feature_list = []
            cell = image_tensor_float[i:i+vertical_step,j:j+horizontal_step]
            n = sum(cell).item()
            feature1 = n/N
            feature_list.append(feature1)
            #print("feature 1 : " ,feature1)
            #pour chaque cellule, on cherche b tel que Y=a+b*X avec X et Y les abscisses et les ordonnées des points gris relativement à la cellule où ils sont 
            X,Y = [],[]     
            #X et Y représentent l'abscisse et l'ordonné
            for x in range(horizontal_step):
                for y in range(vertical_step):
                    if(cell[y,x].item() > 0):
                        X.append(x)
                        Y.append(y)
            #au cas où une cellule ne contient que des pixels blancs, on remplie X et Y par un élément pour ne pas avoir des erreurs lors du calcul de la Covariance
            #if not X or not Y :
            #    X = Y = [1,2]
            cov_matrix = np.cov(X,Y)
            b = cov_matrix[0][1]/cov_matrix[1][1]   #d'après la méthode des moindres carrés
            feature2 = 2*b/(1+b**2)
            feature_list.append(feature2)
            feature3 = (1-b**2)/(1+b**2)
            feature_list.append(feature3)
            cell_list.append(feature_list)
    return FloatTensor(cell_list)

