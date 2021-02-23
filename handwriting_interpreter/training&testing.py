from my_classes import MyDataset, MyNetwork
from my_functions import extract_features
from torchvision import datasets
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch import sum, device, cuda, from_numpy, nn, optim, flatten, no_grad, argmax, load, save
import numpy as np
import cv2

########################################### computing on the GPU for better performance ##########################################
gpu = device('cuda:0' if cuda.is_available() else 'cpu')

################################################ loading datasets from .pt files ##################################################
 
#training_dataset = load('datasets\\training_4x4.pt')
#test_dataset = load('datasets\\test_4x4.pt')
#validation_dataset = load('datasets\\validation_4x4.pt')

training_dataset = load('datasets\\training_7x7.pt')
test_dataset = load('datasets\\test_7x7.pt')
validation_dataset = load('datasets\\validation_7x7.pt')

################################################### creating our data loaders #####################################################

batch_size = 16     #64 is most used value in MNIST training, but we can change it to our preference since it's a hyperparameter
training_DL = DataLoader(training_dataset,batch_size=batch_size)
test_DL = DataLoader(test_dataset,batch_size=batch_size)
validation_DL = DataLoader(validation_dataset,batch_size=batch_size)

print(len(training_DL))
print(len(validation_DL))
print(len(test_DL))

############################################### Instantiating our Nearal network ##################################################
#model = MyNetwork(n_features = 48, hid1=64, hid2=42, out=10)   #n_features = 4*4*3, image is divided into 16 cells in the feature extraction process
model = MyNetwork(n_features = 147, hid1=64, hid2=64, out=10)    #n_features = 7*7*3, image is divided into 49 cells in the feature extraction process
#loss function
loss_function = nn.CrossEntropyLoss()
#cost optimization function
optimization_function = optim.Adam(model.parameters(), lr=0.00005)   #we tested at first with learning rate 0.001
#number of epochs
epochs = 40 #we tested at first with 10 epochs

############################################################# training ############################################################
for ep in range (epochs):
    #### Training: ####
    model.train()
    #initialise training loss
    training_loss = 0.0
    #iterating on data batches
    i=0
    for data, targets in training_DL :
        data.to(gpu)
        i += 1
        predictions = model(flatten(data, start_dim=1).float())
        #calculating the loss
        loss = loss_function(predictions,targets)
        #Backpropagation
        loss.backward()
        #optimization step
        optimization_function.step()
        #update the training_loss
        training_loss += loss.item()
    #training loss is the average of training_loss of all training data
    training_loss /= len(training_DL)

    #### Validation : ####
    model.eval()
    #initialise validation loss
    validation_loss = 0.0
    #initialise the number of correct predictions to 0
    correct = 0
    #no gradient descent in validation process
    with no_grad():
        for data, targets in validation_DL:
            data.to(gpu)
            predictions = model(flatten(data, start_dim=1).float())
            loss = loss_function(predictions, targets)
            validation_loss += loss.item()
            #update the number of correct predictions using argmax
            correct += sum(argmax(predictions,dim=1)==targets).item()
        #average validation loss
        validation_loss /= len(validation_DL)
        #average number of correct predictions
        correct /= len(validation_DL.dataset)
    
    #for each epoch display the training loss, the validation loss and the precision
    print("Epoch number {} :\n Training loss : {} \n Validation loss : {} \n Precision : {}%\n".format(ep,training_loss, validation_loss, correct*100))


############################################################# testing  ############################################################
test_loss = 0.0
correct = 0.0
with no_grad():
    for data, targets in test_DL:
        data.to(gpu)
        predictions = model(flatten(data,start_dim=1).float())
        loss = loss_function(predictions,targets)
        test_loss += loss.item()
        correct += sum(argmax(predictions,dim=1)==targets).item()
    test_loss /= len(test_DL)
    correct /= len(test_DL.dataset)
print("Test loss : {} \nTest precision : {}%\n".format(test_loss, correct*100))



############################################################# saving model ########################################################
#save(model,'models\\digit_model_4x4.pt')
save(model,'models\\digit_model_7x7.pt')
#save(model,'models\\digit_model_test.pt')
print("Module successfully saved.")