from my_classes import MyDataset
from my_functions import extract_features, cell_division
from torchvision import datasets
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch import device, cuda, from_numpy, save, load
import numpy as np
import cv2
from timeit import default_timer as timer

########################################### computing on the GPU for better performance ##########################################
gpu = device('cuda:0' if cuda.is_available() else 'cpu')


####################################################### fetching dataset   #######################################################
#we can also use these two instructions to fetch mnist dataset
mnist_train = datasets.MNIST(root='.', train=True, download=True)
mnist_test = datasets.MNIST(root='.', train=False, download=True)
#mnist_train = load('MNIST\\processed\\training.pt', map_location=device('cuda:0'))
#mnist_test = load('MNIST\\processed\\test.pt', map_location=device('cuda:0'))

####################################################### extracting features ######################################################
#debut de la phase 'feature extraction'
start = timer()

new_train_data = [] 
i = 0 
for image_tensor in mnist_train.data :
    #transformer l'image en noir et blanc uniquement, l'arriere plan est noir et le chiffre est blanc
    image_binary = cv2.threshold(image_tensor.numpy(), 0, 255, cv2.THRESH_BINARY)[1]    
    image_binary_tensor = from_numpy(image_binary)
    image_binary_tensor.to(gpu)
    a = extract_features(image_binary_tensor)
    print ("iteration : {} \n{}".format(i,a))
    new_train_data.append(a)
    i+=1
#convert train data to tensor    
new_train_data = from_numpy(np.array(new_train_data))
print("Train data size : ", new_train_data.size())
    

new_test_data = []  
for image_tensor in mnist_test.data :
    #transformer l'image en noir et blanc uniquement, l'arriere plan est noir et le chiffre est blanc
    image_binary = cv2.threshold(image_tensor.numpy(), 0, 255, cv2.THRESH_BINARY)[1]    
    image_binary_tensor = from_numpy(image_binary)
    image_binary_tensor.to(gpu)
    a = extract_features(image_binary_tensor)
    new_test_data.append(a)
#convert test data to tensor    
new_test_data = from_numpy(np.array(new_test_data))
print("Test data size : ", new_test_data.size())

print("Feature extraction took {} seconds to finish".format(timer()-start))


############## splitting training dataset into training data, validation data, training labes and validation labels ###############

training_data, validation_data, training_targets, validation_targets = train_test_split(new_train_data,mnist_train.targets, test_size=10000)

####################################### creating our 3 datasets (training, test, validation) ######################################

training_dataset = MyDataset(training_data, training_targets)
test_dataset = MyDataset(new_test_data, mnist_test.targets)
validation_dataset = MyDataset(validation_data, validation_targets)

#### saving our datasets as .pt files
save(training_dataset,'datasets\\training_'+str(cell_division[0])+'x'+str(cell_division[1])+'.pt')
save(test_dataset,'datasets\\test_'+str(cell_division[0])+'x'+str(cell_division[1])+'.pt')
save(validation_dataset,'datasets\\validation_'+str(cell_division[0])+'x'+str(cell_division[1])+'.pt')