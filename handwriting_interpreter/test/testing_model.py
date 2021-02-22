import numpy as np
from skimage.feature import hog
import joblib
import cv2
from sklearn import preprocessing

Model, preProcess = joblib.load("ModelDigit42.pkl")

#Select directory of image file
img = cv2.imread('C:\\Users\\Aymane CHAKI\\Desktop\\Projets ENSIAS\\Handwriting_interpreter\\handwriting_interpreter\\test\\digit-reco-in.png')
# Convert to grayscale and apply Gaussian filtering
im_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_grey, (5, 5), 0)
#im_grey = cv2.Canny(im_grey, 50, 90, 255)
#ret, im_th = cv2.threshold(im_grey, 90, 255, 0)
ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
# Find contours in the image
ctrs,_ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]
#print(rects[17])
#print(rects[16])
digits = []
i = 0
for rect in rects:
# Draw the rectangles
    cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1]+ rect[3]), (0, 255, 0), 3)
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    print(roi.size)
    if roi.any():
        roi = cv2.resize(roi, (28,28))
        roi = cv2.dilate(roi, (3, 3))
    if roi.size>0:
        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1,1), visualize=False)
        #print(np.shape(roi_hog_fd))
        arr = np.array([roi_hog_fd], 'float64')
        #print(np.shape(arr))
        #print(i)
        i+=1
        roi_hog_fd = preProcess.transform(arr)
        nbr = Model.predict(roi_hog_fd)
        digits.append(str(int(nbr[0])))
        cv2.putText(img, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
print(digits)
cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
cv2.imshow("Resulting Image with Rectangular ROIs",img)
cv2.waitKey()