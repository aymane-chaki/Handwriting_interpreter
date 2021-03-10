from torch.utils.data import Dataset
from torch import nn
import torch.nn.functional as F

class MyDataset(Dataset) :
    def __init__(self, data, targets):
        super(MyDataset, self)
        self.data = data
        self.targets = targets
    
    def __getitem__(self, index):
        return self.data[index], self.targets[index]

    def __len__(self):
        return len(self.targets)

#We follow some basic 'rule-of-thumb' to define the number of hidden layers and the number of neurons in each hidden layer
class MyNetwork(nn.Module):
    def __init__(self, n_features, hid1, hid2, out):
        #the parameter n_features implies the total number of features in a single image  
        super(MyNetwork, self).__init__()
        self.hidden1 = nn.Linear(n_features, hid1)
        self.hidden2 = nn.Linear(hid1, hid2)
        self.output = nn.Linear(hid2, out)

    def forward(self, x):
        x = F.relu(self.hidden1(x)) #RELU (Rectified Linear Unit) as activation function
        x = F.relu(self.hidden2(x))
        return self.output(x)