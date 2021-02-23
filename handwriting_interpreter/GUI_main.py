from tkinter import *
from PIL import Image
import io
from cv2 import cv2
from torchvision.transforms import ToTensor
import torchvision
import numpy as np
import matplotlib.image as matimg
import matplotlib.pyplot as plt
from torch import from_numpy, load, flatten, max
from my_functions import extract_features

color="black"
#####################      Define Functions      #####################
# eraser is a function that changes the value of the global variable color into "white"
def eraser (event):
    global color
    color = 'white'

# pen is a function that changes the value of the global variable color into "black"
def pen (event):
    global color
    color = 'black'

# penClick is a function that memorize the position of the last click
def penClick(click_event):
    global prev
    prev=click_event

# move is a function that creates an oval on the position of the last click 
#   and move to another click which will be considered as the previous click
def move(move_event):
    global prev
    global color
    myCanvas.create_oval(prev.x,prev.y,move_event.x,move_event.y,width=12,fill=color,outline=color)
    prev=move_event

# delete_all is a function that deletes everything from the canvas
def delete_all():
    myCanvas.delete('all')

# display_result is a function that takes an input and print it in a label widget
def display_result():
    result_label = Label(rightCanvas,text="The written number is : \n "+ str(predict()))
    result_label.config(font=("Calibri",10),bg="white")
    result_label.place(relx=0.5,rely=0.95, anchor='center')
    resized_img = cv2.imread('resized_image.png')
    img_binary = cv2.threshold(resized_img, 0, 255, cv2.THRESH_BINARY_INV)[1]
    plt.imshow(img_binary, cmap='gray')
    plt.show()

# predict() takes a snapshot of the canvas, processes it and predicts which number is it
def predict():
    myCanvas.update()
    ps = myCanvas.postscript(colormode='mono') # takes a snapshot of the whole canva
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    contouring_image(img) # crop this snapshot on the digit's edges
    resizing_image('croppedImage.png') # resize the cropped image to 28x28
    image_tensor = img_to_Tensor('resized_image.png') # transform the resized and cropped image to tensor
    #resized_img = Image.open('resized_image.png')
    image_binary = cv2.threshold(image_tensor.numpy(), 0, 255, cv2.THRESH_BINARY_INV)[1]
    image_binary_tensor = from_numpy(image_binary)
    features = extract_features(image_binary_tensor)
    feature_list = []
    feature_list.append(features)
    data = from_numpy(np.array(feature_list))
    #digit_recognition_model = load('models\\digit_model.pt')
    digit_recognition_model = load('models\\digit_model_7x7.pt')
    test_output = digit_recognition_model(flatten(data, start_dim=1).float())
    prediction = max(test_output, 1)[1].data.numpy().squeeze()
    return prediction 

# contouring_image is a function that takes as an argument an image path and cropped the image on the edges using openCV
def contouring_image(pil_image):
    open_cv_image = np.array(pil_image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR 
    original_image= open_cv_image
    gray= cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2GRAY)
    edges= cv2.Canny(gray, 50,200)
    contours= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)

    for (i,c) in enumerate(sorted_contours):
        x,y,w,h= cv2.boundingRect(c)
        cropped_contour= original_image[y-10:y+h+10, x-10:x+w+10]
        image_name= "croppedImage.png"
        cv2.imwrite(image_name, cropped_contour)
        #readimage= cv2.imread(image_name)
        #cv2.imshow('Image', readimage)
        #cv2.waitKey(0)
        break   #on arrête après une itération pour prendre seulement l'image avec la plus grande surface, c'est l'image qu'on veut
        

def resizing_image(path):
    img = Image.open(path)
    resized_img = img.resize((28, 28))
    resized_img.save("resized_image.png")
    """ resized_img.show()
    img_binary = cv2.threshold(np.array(resized_img), 0, 255, cv2.THRESH_BINARY_INV)[1]
    plt.imshow(img_binary, cmap='gray')
    plt.show() """

def img_to_Tensor(path):
    #image = Image.open(path)
    image = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    # transform Image into the numpy array
    image_2_npArray = np.array(image)

    # transform the numpy array into the tensor
    image_2_npArray_2_tensor = from_numpy(image_2_npArray)
    return image_2_npArray_2_tensor


''' If ever you get this error : OSError: Unable to locate Ghostscript on paths
    just paste this on your cmd : conda install -c conda-forge ghostscript'''


#####################      Prepare the environment      #####################
root= Tk(className=' Handwritten Digits Interpreter GUI')
root.resizable(False,False)
root.geometry("700x500") 

#####################      Make the Layout      #####################
# myCanvas is the main canvas where the user can draw
myCanvas=Canvas(root,width=540,height=500,background='white') 
myCanvas.grid(row=0,column=0)
myCanvas.create_line(1.5,0,1.5,500,fill='cadet blue') #left border

# rightCanvas is the canvas where we will put the buttons, the text label widgets, ... (user cannot draw on)
rightCanvas=Canvas(root,width=155,height=500,background='white', highlightthickness=0)
rightCanvas.place(relx =1.0, rely=0.0, anchor='ne')
rightCanvas.create_line(0,0,0,500,fill='cadet blue') #right border

#####################      Creating a label widget      #####################
myLabel= Label(rightCanvas,text="\n Handwritten \n Digits \n Interpreter",bg="white")
myLabel.config(font=("Calibri",18))
myLabel.place(relx =0.95, rely=0.01, anchor='ne')

#####################      Creating the buttons      #####################
# pen button
penButton = Button(rightCanvas,text="Pen",padx=21,pady=5) #state=DISABLED to disable the button
penButton.place(relx =0.25, rely=0.35, anchor='center')
penButton.bind('<Button-1>',func=pen)
# eraser button
eraserButton = Button(rightCanvas,text="Eraser",padx=15,pady=5) #state=DISABLED to disable the button
eraserButton.place(relx =0.75, rely=0.35, anchor='center')
eraserButton.bind('<Button-1>',func=eraser)
# erase all button
erase_all=Button(rightCanvas,text="Erase all",padx=30,pady=5,command=delete_all)
erase_all.place(relx=0.5,rely=0.55, anchor='center')
# show result button
result_button=Button(rightCanvas,text="Show result",padx=20,pady=5,command=display_result)
result_button.place(relx=0.5,rely=0.65, anchor='center')
""" # display image button
result_button=Button(rightCanvas,text="Display Image",padx=20,pady=5,command=predict)
result_button.place(relx=0.5,rely=0.85, anchor='center')
 """
#####################      Main      #####################
myCanvas.bind('<Button-1>',penClick)
myCanvas.bind('<B1-Motion>',move) 

root.mainloop()