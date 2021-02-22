from torch.utils.data import Dataset

class MyDataset(Dataset) :
    def __init__(self, data, targets):
        super(MyDataset, self)
        self.data = data
        self.targets = targets
    
    def __getitem__(self, index):
        return self.data[index], self.targets[index]

    def __len__(self):
        return len(self.targets)
