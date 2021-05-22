'''This file contains function for updation of logo and activity log, basically general utilities'''


from tkinter import *
from threading import *
from editor import *
from sr import *
import beepy
from PIL import ImageTk, Image
import speech_recognition as sr
import time
import subprocess

def UpdateActivity(edit, activity_log):
    '''
    For updating the activity log each time there is a change on editor while the voice mode is on
    '''
    #Beep is helpful for making the user realize that the change has been made on the editor
    beepy.beep(sound=3)
    activity_log.config(state='normal')
    activity_log.insert(END, edit)
    activity_log.config(state='disabled')

def UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo):
    '''    
    Update the file name and file type in the label when new file is opened or saved
    '''
    lb.config(text = file_path)
    filetype = file_path.split('.')
    if 'cpp' in filetype[1]:
        lb.config(image=logo_cp)
    elif 'txt' in filetype[1]:
        lb.config(image=logo_t)
    elif 'py' in filetype[1]:
        lb.config(image=logo_p)
    elif 'java' in filetype[1]:
        lb.config(image=logo_j)
    elif 'c' in filetype[1]:
        lb.config(image=logo_c)
    else:
        lb.config(image=logo)

def RemovePrev():
    '''
    For removing the executable created during the previous execution
    '''
    cmd = 'rm -frv a.exe'
    p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    _ = p.stdout.read()

def GiveInput(command, editor, count, activity_log, code_input):
    '''
    For giving input to the program
    '''
    #Adding a pause between 2 consecutive commands
    time.sleep(0.5)
    #Everything after the chime will be the input to the program
    beepy.beep(sound=4)
    Input = Listen(activity_log)
    if Input is not None:
        code_input.insert(INSERT, Input)       
        edit = str(count)+ '::' + 'Added ' +  Input + ' to input block\n'
        UpdateActivity(edit, activity_log)