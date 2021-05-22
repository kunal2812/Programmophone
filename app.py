'''This file contains all the primary functions in the Programmophone, UI build for it and also acts as a link between all the files'''

from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import sys
import time
from PIL import ImageTk, Image
import speech_recognition as sr
from threading import *
from editor import *
from sr import *
from cpp_utils import *
from utils import *
from common_utils import *

Font = ("Comic Sans MS", "10", "normal") #Default font
Bfont = ("Comic Sans MS", "10", "bold")
file_path = ''
is_on = False #Carries the state of voice mode
count = 1 #Activity count while the voice mode is on

def Path(path):
    '''
    Called upon for changing the current file_path every time a file is opened or saved
    '''                                              
    global file_path
    file_path = path

def multi_thread(target, *args):
    '''
    For starting a new thread parallel to the main thread
    '''
    t = Thread(target = target, args=args)
    print(active_count())
    #If the thread is not daemon it won't exit even if the main function is terminated and cause the system to not respond
    t.daemon=True
    t.start()

def Start():
    MistyMode()

def MistyMode():
    '''
    Default configuration with which Programmophone runs, the commands would still be listened without the voice mode being on
    but inorder for it to perform the desired action one must say 'hey misty' followed by the commands in the documentation.
    This functionality is provided so that one could also work with it even in noise and normal voice mode could be activated with
    the help of voice
    '''                                                  
    global is_on
    global activity_lb
    while is_on==False:
        command = Listen(activity_lb)
        # print(8)
        if command is not None:
            if 'hey' and 'misty' in command:
                command = command.replace('hey', '')
                command = command.replace('misty', '')
                Action(command)
        if is_on:
            sys.exit()

def VoiceMode():
    '''
    Listens and sends the obtained text to 'Action' to find the trigger word and act accordingly
    '''
    global is_on
    global activity_lb
    while is_on==True:
        command = Listen(activity_lb)
        if command is not None:
            Action(command)
        if is_on==False:
            sys.exit()

def Activate():
    '''
    For activating the voice mode
    '''
    global is_on
    Speak('Voice Mode on')
    is_on = True
    switch.config(image = on)
    multi_thread(VoiceMode)

def Deactivate():
    '''
    For deactivating the voice mode
    '''
    global is_on
    global count
    count=1
    is_on = False      
    Speak('Deactivated voice mode')
    switch.config(image=off)
    multi_thread(MistyMode)

def Compile(text, code_input, code_output, file_path, editor, is_on):
    '''
    For compiling the program and creating executable or class file
    '''
    RemovePrev()
    code_output.delete('1.0', END)
    if file_path == '':
        multi_thread(Speak,'Please save your code first')
        return
    filetype = file_path.split('.')
    if 'cpp' in filetype[1]:   
        code_output.insert('1.0', "Compiling...")
        command = ['g++', '-std=gnu++11', file_path]
    elif 'txt' in filetype[1]:
        multi_thread(Speak, "Can't compile .txt files")                
        code_output.insert('1.0', "Can't compile .txt files")
        return
    elif 'py' in filetype[1]:
        multi_thread(Speak, "Python is an interpreted language and not a compiled one, Click on run to run the program")                
        code_output.insert('1.0', 'Python is an interpreted language and not a compiled one\n Click on run to run the program')
        return
    elif 'java' in filetype[1]:
        file_type = file_path.split('.')
        rem = file_type[0] + '.class'
        cmd = 'rm -frv ' + rem
        p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        _ = p.stdout.read() 
        code_output.insert('1.0', "Compiling...")
        command = ['javac', file_path]
    elif 'c' in filetype[1]:        
        code_output.insert('1.0', "Compiling...")
        command = ['gcc', file_path]
    else:
        return
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
    a, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0',  error)
    Speak(text)
    #Most of the times error in the later parts are associated with the initial errors so the user is told the error in the initial part so that user don't has to listen the complete error log
    if error is not None and is_on == True:
        gist = error.split('\n')
        if len(gist)<=4:           
            multi_thread(Speak, error)
        else:
            gist = gist[0]+'\n' + gist[1] + '\n' + gist[2] + '\n' + gist[3]
            multi_thread(Speak, gist)
    return error

def Run(text, code_input, code_output, file_path, editor, is_on):
    '''
    For both compiling and then running the executable or class file
    ''' 
    inp = code_input.get('1.0', END)
    code_output.delete('1.0', END)
    filetype = file_path.split('.')
    if 'cpp' in filetype[1]:
        Compile(text, code_input, code_output, file_path, editor, is_on)
        p = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        code = editor.get('1.0', END)
        if "cin" or "scanf" in code:
            inp = inp.encode('ascii')   
            p.stdin.write(inp)
        output, _ = p.communicate()
    elif 'txt' in filetype[1]:
        return
    elif 'py' in filetype[1]:
        Speak('Running')
        command = ['python', file_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        code = editor.get('1.0', END)
        if "input" in code:
            inp = inp.encode('ascii')   
            process.stdin.write(inp)
        output, error = process.communicate()
        if error is not None:
            code_output.insert('1.0', error)
            if is_on == True:
                multi_thread(Speak, error)
    elif 'java' in filetype[1]:
        Compile(text, code_input, code_output, file_path, editor, is_on)
        filename = file_path.split('.')
        obj = filename[0]+'.class'
        p = subprocess.Popen([obj], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        code = editor.get('1.0', END)
        if "Scanner" in code:
            inp = inp.encode('ascii')   
            p.stdin.write(inp)
        output, _ = p.communicate()
    elif 'c' in filetype[1]:        
        Compile(text, code_input, code_output, file_path, editor, is_on)
        p = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        code = editor.get('1.0', END)
        if "scanf" in code:
            inp = inp.encode('ascii')   
            p.stdin.write(inp)
        output, _ = p.communicate()
    else:
        return
           
    code_output.insert('1.0', output)
    if output is not None and is_on == True: 
        output = output.decode('utf-8')
        multi_thread(Speak, output)


def Action(command):
    '''
    For finding the trigger word from the text obtained from speech and calling the neccessary function based on the trigger word
    '''
    print(command)
    global editor
    global count
    global activity_log
    global code_input
    global activity_lb

    control = {'deactivate':Deactivate, 'activate':Activate, 'open':OpenVoice,          
                 'save':SaveVoice, 'compile':Compile, 'close':sys.exit, 'exit':sys.exit,
                 'run':Run
                }

    #Common functions for moving the cursor and deleting characters
    common = {'position':TellPos, 'give':GiveInput, 'remove':DeletePos, 'move':MovePos,   
                'read':ReadLine, 'escape':Escape, 'enter':Enter, 'add':Extra, 'brackets':Brackets
                }
    #Common triggers for C and C++ which are checked only if the file type is .c or .cpp, so make sure to save the file before triggering language specific functions
    c_cpp_common_triggers = {'include':IncludeHeader, 'main':Main, 'declare':DeclareVar,  
                             'for':For, 'else if':ElseIf, 'else statement':Else,          
                             'if statement':If, 'do while':DoWhile, 'while':While
                            }
    #C++ specific triggers which are checked only if the file type is .cpp
    cpp_triggers = {'namespace':Namespace, 'print':Print, 'newline':Newline, 'input':Input}                                                                                             

    for item in control.keys():
        if item in command:
            control[item]()
            return
    for item in common.keys():
        if item in command:
            common[item](command, editor, count, activity_log, code_input)
            if item == 'remove':
                count+=1
            #Every time there is change on the editor the user is told the current position of cursor
            TellPos(command, editor, count, activity_log, code_input)
            return
    if '.c'in file_path: #i.e both c and c++ files are targeted
        for item in c_cpp_common_triggers.keys():
            if item in command:
                c_cpp_common_triggers[item](command, editor, count, activity_log, activity_lb)
                count+=1
                TellPos(command, editor, count, activity_log, code_input)
                return

    if '.cpp' in file_path: #only c++ files are targeted
        for item in cpp_triggers.keys():
            if item in command:
                cpp_triggers[item](command, editor, count, activity_log)
                count+=1
                TellPos(command, editor, count, activity_log, code_input)
                return

def Open():
    '''
    Opens a overlaying dialog to choose which file to open
    Triggered when Open button in the header is clicked
    '''
    global file_path
    global lb
    path = askopenfilename(filetypes = [('C++ Files', '*.cpp'), ('Java Files', '*.java'), ('Python Files', '*.py'), ('C Files', '*.c'), ('Text Files', '*.txt'), ('All Files', '*.*')])
    try:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            Path(path)
    except:
        pass
    if file_path != '':
        UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo)
            
def Save():
    '''
    For saving the changes into new file
    Triggered when Save button in the header is clicked
    '''    
    global file_path
    global lb
    if file_path == '':
        path = asksaveasfilename(filetypes = [('C++ Files', '*.cpp'), ('Java Files', '*.java'), ('Python Files', '*.py'), ('C Files', '*.c'), ('Text Files', '*.txt'), ('All Files', '*.*')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)
    UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo)

def SaveAs():    
    global file_path
    global lb
    path = asksaveasfilename(filetypes = [('C++ Files', '*.cpp'), ('Java Files', '*.java'), ('Python Files', '*.py'), ('C Files', '*.c'), ('Text Files', '*.txt'), ('All Files', '*.*')])
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)
    UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo)

def SaveVoice():
    '''
    Triggered when save command is called, provides completely hands free experience while saving the file
    '''     
    global file_path
    global lb
    global activity_lb
    if file_path == '':
        p = os.getcwd()+'/'
        Speak('What name would you like me to give to the file ?')
        time.sleep(0.5)
        beepy.beep(4)
        try:
            command = Listen(activity_lb)
            Speak('What is the format of this file ? Say 0 for C++ 1 for Python 2 for Java 3 for c and 4 for text')
            time.sleep(0.5)
            beepy.beep(4)
            format = Listen(activity_lb)
            if '0' in format:
                command = command+'.cpp'
            elif '1' in format:
                command = command+'.cpp'
            elif '2' in format:
                command = command+'.java'
            elif '3' in format:
                command = command+'.c'
            elif '4' in format:
                command = command+'.txt'
            else:
                return    

            command = command.replace(' ', '')
            Speak('I am saving it as ')
            for char in command:
                Speak(char)
            Speak('Say yes to confirm and no to try again')
            cmd = Listen(activity_lb)
            if 'yes' in cmd:
                path = os.path.join(p, command)
        except:
            SaveVoice()

    else:
        path = file_path
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            Path(path)    
    if file_path != '':
        UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo)

def OpenVoice():
    '''
    Triggered when open command is called, provides completely hands free experience while opening the file
    '''  
    global file_path
    global lb
    global activity_lb
    p = 'files/'
    Speak('Which one of the following would you like me to open ?')
    files = os.listdir(p)
    for file in files:
        Speak(file)
        command = Listen(activity_lb)
        if command is not None and 'this' in command:
            path = os.path.join(p, file)
            break

    if os.path.isfile(path):
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            Path(path)
        if file_path != '':
            UpdateLogo(file_path, lb, logo_j, logo_cp, logo_p, logo_t, logo_c, logo)
    else:
        Speak('Try Again')

def button_mode():
    '''
    For activating or deactivating voice mode with the button on the top right corner of layout
    '''  
    global is_on
    global count

    if is_on:
        count=1
        switch.config(image=off)        
        is_on = False
        activity_log.delete('1.0', END)    
        multi_thread(Speak, 'Deactivated voice mode')
        multi_thread(MistyMode)
    else:
        switch.config(image = on)         
        is_on = True     
        multi_thread(Speak, 'Activated Voice Mode')
        multi_thread(VoiceMode)

app = Tk()
app.geometry("1200x670-100-38")
app.title('Programmophone')
app.minsize(1200, 670)

#All logos corresponding to the file type
logo_j = ImageTk.PhotoImage(Image.open("assets/java.png").resize((40, 22), Image.ANTIALIAS))
logo_cp = ImageTk.PhotoImage(Image.open("assets/cpp.png").resize((30, 30), Image.ANTIALIAS))
logo_p = ImageTk.PhotoImage(Image.open("assets/python.png").resize((25, 20), Image.ANTIALIAS))
logo_t = ImageTk.PhotoImage(Image.open("assets/text.png").resize((25, 23), Image.ANTIALIAS))
logo_c = ImageTk.PhotoImage(Image.open("assets/c.png").resize((25, 23), Image.ANTIALIAS))
logo = ImageTk.PhotoImage(Image.open("assets/unknown.png").resize((25, 23), Image.ANTIALIAS))

on = ImageTk.PhotoImage(Image.open("assets/on.png").resize((60, 20), Image.ANTIALIAS))
off = ImageTk.PhotoImage(Image.open("assets/off.png").resize((60, 20), Image.ANTIALIAS))

#Main label on the tkinter app window
lb = Label(app, justify = RIGHT, compound = LEFT, padx = 10, text = "newfile",  font = Bfont, image = logo)

lb.pack() 

global code_output
global code_input
global editor

#Main menu on the tkinter window
header = Menu(app)
header.add_command(label='Open', command=Open)
header.add_command(label='Save', command=Save)
header.add_command(label='Save as', command=SaveAs)
header.add_command(label='Compile', command=lambda: multi_thread(Compile, 'Compiled successfully', code_input, code_output, file_path, editor, is_on))
header.add_command(label='Run', command=lambda: multi_thread(Run, 'Executed successfully', code_input, code_output, file_path, editor, is_on))
header.add_command(label='Close', command=sys.exit)
app.config(menu=header)

#Top frame
F1 = Frame(app, relief=SUNKEN, borderwidth=2)
F1.pack(side=TOP, fill=BOTH)

#Frame for the editor
F1_left = CustomFrame(F1, height=27, relief = SUNKEN, borderwidth=2)
F1_left.pack(side=LEFT, fill = BOTH, padx=(0, 10))

#Frame for the activity log
F1_right = Frame(F1, relief=SUNKEN, borderwidth=2)
F1_right.pack(side = RIGHT, fill = BOTH, padx=(20, 0))

activity_lb = Label(F1_right, padx=10, text = "Activity Log", font=Bfont)
activity_lb.pack(anchor=W)

a = Scrollbar(F1_right, orient=VERTICAL)
a.pack(side=RIGHT, fill=Y, pady=(0,25))

#This section would contain all activity performed while the voice mode is on which gets cleared if the voice mode is disabled in between, useful for tracking what operations the person has performed 
activity_log = Text(F1_right, width = 50, height=27, yscrollcommand=a.set, borderwidth=2)
activity_log.pack(fill = BOTH, pady=(0,20))

#Making the activity log non-editable
activity_log.bind("<Key>", lambda e: "break")

a.config(command=activity_log.yview)

#Switch for the voice mode
switch = Button(lb,image=off,bd =0,command = button_mode, anchor=E)
switch.pack(side=RIGHT, padx=(1070,0), anchor=E, expand=True)

#Bottom Frame
F2 = Frame(relief = SUNKEN, borderwidth=2)
F2.pack(side=BOTTOM, fill=BOTH)

#Frame for input section
F2_left = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_left.pack(side=LEFT, fill=BOTH)

#Frame for output section
F2_right = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_right.pack(side=RIGHT, fill=BOTH)

lb_in = Label(F2_left, padx = 10, text = "Input",  font = Bfont)
lb_out = Label(F2_right, padx=10, text = "Output",  font = Bfont)
lb_in.pack(anchor = 'w')
lb_out.pack(anchor='w')

b = Scrollbar(master = F2_left , orient = 'vertical')
b.pack(side=RIGHT, fill = Y)

editor = F1_left.text
font = tkinter.font.Font(font=editor['font'])
editor.config(tabs=font.measure('         '))
editor.see(INSERT)

code_input = Text(master = F2_left, font = Font, width=50, yscrollcommand = b.set, borderwidth=2)
code_input.pack(fill = BOTH, padx=2)

b.config(command = code_input.yview)

c = Scrollbar(master = F2_right , orient = 'vertical')
c.pack(side=RIGHT, fill = Y)

code_output = Text(master = F2_right, font = Font, width=170, yscrollcommand = c.set, borderwidth=2)
code_output.pack(fill = BOTH, padx=2)

#Making the output window non editable
code_output.bind("<Key>", lambda e: "break")

c.config(command = code_output.yview)

#Starting another thread for misty mode before the main thread starts which is a infinite loop
multi_thread(Start)
app.mainloop()