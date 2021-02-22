from tkinter import *
from PIL import Image
import io

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
    myCanvas.create_oval(prev.x,prev.y,move_event.x,move_event.y,width=10,fill=color,outline=color)
    prev=move_event

# delete_all is a function that deletes everything from the canvas
def delete_all():
    myCanvas.delete('all')

# display_result is a function that takes an input and print it in a label widget
def display_result():
    result_label = Label(rightCanvas,text="Vous avez écrit le chiffre : \n "+ str(int(input("Enter a number :"))))
    result_label.config(font=("Calibri",10),bg="white")
    result_label.place(relx=0.5,rely=0.95, anchor='center')

# display_image takes a snapshot of the canvas
def display_image():
    myCanvas.update()
    ps = myCanvas.postscript(colormode='mono')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.show()
    #img.save('result.png')
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
# display image button
result_button=Button(rightCanvas,text="Display Image",padx=20,pady=5,command=display_image)
result_button.place(relx=0.5,rely=0.85, anchor='center')

#####################      Main      #####################
myCanvas.bind('<Button-1>',penClick)
myCanvas.bind('<B1-Motion>',move) 

root.mainloop()