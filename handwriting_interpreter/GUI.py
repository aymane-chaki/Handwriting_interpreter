from tkinter import *

#####################      Define Functions      #####################

def eraser (event):
    global color
    color = 'white'
    print(color)

def pen (event):
    global color
    color = 'black'
    print(color)

# penClick is a function that memorize the position of the last click
def penClick(click_event):
    global prev
    prev=click_event

# move is a function that create an oval on the position of the last click 
# and move to another click which will be considered as the previous click
def move(move_event):
    global prev
    global color
    myCanvas.create_oval(prev.x,prev.y,move_event.x,move_event.y,width=10,fill="white")
    prev=move_event

#####################      Prepare the environment      #####################
root= Tk(className=' Handwritten Digits Interpreter GUI')
root.resizable(False,False)
root.geometry("700x500")

#####################      Make the Layout      #####################
# myCanvas is the main canvas where the user can draw
myCanvas=Canvas(root,width=540,height=500,background='white') #myCanvas.pack(expand=YES,fill=BOTH)
myCanvas.grid(row=0,column=0)
#Let's make some borders :)
myCanvas.create_line(540,0,540,500,fill='cadet blue') #right border
myCanvas.create_line(1.5,0,1.5,500,fill='cadet blue') #left border

# rightCanvas is the canvas where we will put the buttons, the text label, ... (user cannot draw on)
rightCanvas=Canvas(root,width=155,height=500,background='white')
rightCanvas.place(relx =1.0, rely=0.0, anchor='ne')


#####################      Creating a label widget      #####################
myLabel= Label(rightCanvas,text="\n Handwritten \n Digits \n Interpreter",bg="white")
myLabel.config(font=("Calibri",20))
myLabel.place(relx =0.99, rely=0.0, anchor='ne')


#####################      Creating the buttons      #####################
# pen button
penButton = Button(rightCanvas,text="Pen",padx=21,pady=5) #state=DISABLED to disable the button
penButton.place(relx =0.25, rely=0.35, anchor='center')
penButton.bind('<Button-1>',func=pen)
# eraser button
eraserButton = Button(rightCanvas,text="Eraser",padx=15,pady=5) #state=DISABLED to disable the button
eraserButton.place(relx =0.75, rely=0.35, anchor='center')
eraserButton.bind('<Button-1>',func=eraser)



#####################      Main      #####################
myCanvas.bind('<Button-1>',penClick) #Sorry, I still don't know how it works :/
myCanvas.bind('<B1-Motion>',move) #Sorry, I still don't know how it works :/

root.mainloop()