from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import sys
import time
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr
from threading import *
from LineNum import *

# Create an instance of window of frame
win =Tk()

# set Title
win.title('On/Off Demonstration')

# Set the Geometry
win.geometry("600x400")
win.resizable(0,0)
#Create a variable to turn on the button initially
is_on = True

# Create Label to display the message
label = Label(win,text = "Night Mode is On",bg= "white",fg ="black",font =("Poppins bold", 22))
label.pack(pady = 20)

# Define our switch function
def button_mode():
   global is_on
   
   #Determine it is on or off
   if is_on:
      on_.config(image=off)
      label.config(text ="Day Mode is On",bg ="white", fg= "black")
      is_on = False
   else:
      on_.config(image = on)
      label.config(text ="Night Mode is On", fg="black")
      is_on = True

# Define Our Images
on = ImageTk.PhotoImage(Image.open("img/on.png").resize((60, 20), Image.ANTIALIAS))
off = ImageTk.PhotoImage(Image.open("img/off.png").resize((60, 20), Image.ANTIALIAS))

# Create A Button
on_= Button(win,image =on,bd =0,command = button_mode)
on_.pack(pady = 50)

#Keep Running the window
win.mainloop()