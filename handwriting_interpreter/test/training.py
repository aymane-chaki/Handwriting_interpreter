import numpy as np
from skimage.feature import hog
from sklearn import preprocessing
from collections import Counter
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import joblib
import cv2

mnist = fetch_openml('mnist_784')
X, y = mnist['data'], mnist['target']
data = np.array(X, 'int16')
target = np.array(y, 'int')
list_hog = []

#feature extraction
for feature in data:
 fd = hog(feature.reshape((28,28)), orientations=9, pixels_per_cell=(14,14),cells_per_block=(1,1),visualize=False )
 list_hog.append(fd)
hog_features = np.array(list_hog, 'float64')
preProcess = preprocessing.MaxAbsScaler().fit(hog_features)
hog_features_transformed = preProcess.transform(hog_features)

#training
X_train, X_test, y_train, y_test = train_test_split(hog_features_transformed,target , random_state = 0)
Model = MLPClassifier(activation='relu', hidden_layer_sizes=(200, 200), alpha = 0.3)
Model.fit(X_train, y_train)
print("Training Score :: {}\n".format(Model.score(X_train, y_train)))
print("Testing Score :: {}\n".format(Model.score(X_test, y_test)))

#saving the model
joblib.dump((Model, preProcess), "ModelDigit42.pkl", compress=3)