from my_classes import MyDataset
from my_functions import extract_features
from torchvision import datasets
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch import device, cuda
import numpy as np

########################################### computing on the GPU for better performance ##########################################
gpu = device('cuda' if cuda.is_available() else 'cpu')


####################################################### fetching dataset   #######################################################
mnist_train_downloaded = datasets.MNIST(root='.', train=True, download=True)
mnist_test_downloaded = datasets.MNIST(root='.', train=False, download=True)

####################################################### extracting features ######################################################

new_train_data = [] 
i = 0 
for image_tensor in mnist_train_downloaded.data : 
    image_tensor.to(gpu)
    a = extract_features(image_tensor)
    print ("iteration : {} \n{}".format(i,a))
    new_train_data.append(a)
    i+=1

""" new_train_dataset = MyDataset(new_train_data, mnist_train_downloaded.targets) """

new_test_data = []  
for image_tensor in mnist_test_downloaded.data : 
    new_test_data.append(extract_features(image_tensor))

""" new_test_dataset = MyDataset(new_test_data, mnist_train_downloaded.targets) """

############## splitting training dataset into training data, validation data, training labes and validation labels ###############

training_data, validation_data, training_targets, validation_targets = train_test_split(new_train_data,mnist_train_downloaded.targets, test_size=10000)

####################################### creating our 3 datasets (training, test, validation) ######################################

training_dataset = MyDataset(training_data, training_targets)
test_dataset = MyDataset(mnist_test_downloaded.data, mnist_test_downloaded.targets)
validation_dataset = MyDataset(validation_data, validation_targets)

################################################### creating our data loaders #####################################################

batch_size = 64     #64 is most used value in MNIST training, but we can change it to our preference since it's a hyperparameter
training_DL = DataLoader(training_dataset,batch_size=batch_size)
test_DL = DataLoader(test_dataset,batch_size=batch_size)
validation_DL = DataLoader(validation_dataset,batch_size=batch_size)
print(len(training_DL))


############################################################# training ############################################################


############################################################# testing  ############################################################


############################################################# saving model ########################################################