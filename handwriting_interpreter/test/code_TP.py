for i in range (10) :
    plt.subplot(1, 10, i+1)
    plt.imshow(mnist_train_downloaded.data[i], cmap='gray_r')
    plt.title(mnist_train_downloaded.targets[i].item())
    plt.axis('off')
plt.show()