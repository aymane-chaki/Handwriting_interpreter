from my_classes import MyDataset
import matplotlib.pyplot as plt
from torchvision import datasets
import cv2
import torch


mnist_train_downloaded = datasets.MNIST(root='.', train=True, download=True)
mnist_test_downloaded = datasets.MNIST(root='.', train=False, download=True)
ds = MyDataset(mnist_train_downloaded.data, mnist_train_downloaded.targets)
torch.save(ds, 'datasets\\my_dataset.pt')
dataset = torch.load('datasets\\my_dataset.pt', map_location=torch.device('cuda:0'))

""" for i in range (10) :
    plt.subplot(1, 10, i+1)
    plt.imshow(mnist_train_downloaded.data[i], cmap='gray')
    plt.title(mnist_train_downloaded.targets[i].item())
    plt.axis('off')
plt.show() """
image = dataset.data[1]
print(image)
img_binary = cv2.threshold(image.cpu().numpy(), 0, 255, cv2.THRESH_BINARY)[1]
print(img_binary)
plt.imshow(img_binary, cmap='gray')
plt.show()