from torch import FloatTensor, device, cuda, from_numpy
from torch import sum 
import numpy as np

########################################### computing on the GPU for better performance ##########################################
gpu = device('cuda:0' if cuda.is_available() else 'cpu')

cell_division = (7,7)       #la division des images par cellules
def extract_features(image_tensor)  :
    pixels = image_tensor.size()   
    image_tensor_float = image_tensor.float()
    N = sum(image_tensor_float).item()
    cell_list = []  #each element of this list is a tensor of 3 features representing the features of a cell
    vertical_step = pixels[1]//cell_division[1]
    horizontal_step = pixels[0]//cell_division[0]
    #load variables in the gpu
    image_tensor_float.to(gpu)
    for i in range (0, pixels[1], vertical_step) :          #iteration verticale de cellules 
        for j in range (0, pixels[0], horizontal_step) :    #iteration horizontale de cellules
            feature_list = []
            cell = image_tensor_float[i:i+vertical_step,j:j+horizontal_step]
            cell.to(gpu)
            n = sum(cell).item()
            feature1 = n/N
            feature_list.append(feature1)
            #print("feature 1 : " ,feature1)
            #pour chaque cellule, on cherche b tel que Y=a+b*X avec X et Y les abscisses et les ordonnées des points gris relativement à la cellule où ils sont 
            X,Y = [],[]   
            #X et Y représentent l'abscisse et l'ordonné
            for x in range(horizontal_step):
                for y in range(vertical_step):
                    if(cell[y,x].item() == 255):   #l'image est binaire et le chiffre est écrit en blanc sur un arrière plan noir, donc on traite les pixels blancs pas les noirs
                        X.append(x)
                        Y.append(y)
            cov_matrix = np.cov(X,Y)
            b = cov_matrix[0][1]/cov_matrix[1][1]   #d'après la méthode des moindres carrés
            feature2 = 2*b/(1+b**2)
            feature_list.append(feature2)
            feature3 = (1-b**2)/(1+b**2)
            feature_list.append(feature3)
            #tester si feature_list contient NaN, si oui on remplace la liste par [0.0, 0.0, 0.0]
            s = np.sum(feature_list)
            if np.isnan(s) : 
                feature_list = [0.0, 0.0, 0.0]
            #convert feature list to tensor and add it to cell list
            cell_list.append(feature_list)
    #convert cell list to tensor and return it
    return cell_list

