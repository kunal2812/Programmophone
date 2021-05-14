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
from SR import *

Font = ("Comic Sans MS", "10", "normal")
Bfont = ("Comic Sans MS", "10", "bold")
file_path = ''
engine = pyttsx3.init()
engine.setProperty('rate', 100)
recognizer = sr.Recognizer()
is_on = False

dict =  {"hash":'#', 'slash':'/', 'hyphen':'-', 'underscore':'_', 'backslash':'\\', 
            'left angular':'<', 'right-angular':'>', 'asterisk':'*', 'exclamation':'!',
             'ampersand':'&', 'modulo':'%', 'plus':'+', 'minus':'-', 'divide':'/', 'dot':'.',
              'and':'&&', 'or':'||', 'bitwise and':'&', 'bitwise or':'|', 'xor': '^', 'percent':'%'
        }
vocab = ['int', 'long long', 'unordered', 'map', 'set', 'pair', 'include', 'stdio',
            'bits/stdc++.h', 'unordered_map', 'tree', 'node', 'list', 'stack', 'queue', 
            'double', 'float', 'enum', 'unsigned', 'unordered_set', 'iostream', 'stdlib.h',
            'string', 'char', 'array', 'slash', 'backslash', 'ampersand', 'underscore', 
            'divide', 'plus', 'add', 'substract', 'multiply', 'modulo', 'hyphen', 'double slash',
            'newline', 'tab', 'copy', 'line', 'open', 'save', 'compile', 'hey', 'misty', 'dequeue', 'bool',
            'true', 'false', 'using', 'namespace', 'std', 'stdio.h', 'class', 'public', 'private', 'void', 
            'main', 'pointer', 'cpp', 'py', 'txt', 'npos', 'null', 'substr', 'if', 'else', 'switch', 'case'
            'xor', 'bitwise', 'and', 'or', 'd', 'll'
        ]

def Path(path):
    global file_path
    file_path = path

def MistyMode():
    command = Listen()
    if command is not None:
        command = command.lower()
        if 'hey' and 'misty' in command:
            command = command.replace('hey', '')
            command = command.replace('misty', '')
            Action(command)
        else:
            MistyMode()
    else:
        MistyMode()

def VoiceMode():
    command = Listen()
    if command is not None:
        command = command.lower()
        Action(command)
        VoiceMode()
    else:
        VoiceMode()

def Action(command):
    print(command)
    if 'activate' and 'voice' in command:
        Speak('Voice Mode on')
        switch.config(image = on)
        VoiceMode()
    if 'deactivate' and 'voice' in command:        
        Speak('Deactivated voice mode')
        switch.config(image=off)
        MistyMode()
    elif 'include' in command:
        command = command.replace('include', '')
        command = command.replace(' ', '')
        header = "#include<"
        header = header+command+'>\n'
        editor.insert(INSERT, header)
    elif 'namespace' in command:
        namespace = command + ';\n'
        editor.insert(INSERT, namespace)
    elif 'main' or 'men' in command:
        command = command + '(){\n\n}'
        editor.insert(INSERT, command)
        editor.mark_set('insert', 'insert-1c')
    elif 'open' in command:
        OpenVoice(editor, lb)
    elif 'save' in command:
        SaveVoice(file_path, editor, lb)
    elif 'compile' in command:
        Compile()
        Speak('Compiled successfully')
    elif 'close' or 'exit' in command:
        Speak('Exiting....')
        sys.exit()
    elif 'run' or ('compile' and 'run') in command:
        Run()
        Speak('Compiled and Ran successfully')
    else:
        return

    
def multi_thread(target, *args):
    t = Thread(target = target, args=args)
    t.daemon=True
    t.start()


def Start():
    MistyMode()

def Open():
    path = askopenfilename(filetypes = [('C++ Files', '*.cpp')])
    try:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            Path(path)
    except:
        pass
    if file_path != '':
        lb.config(text = file_path)

def Save():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('C++ Files', '*.cpp')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)
    lb.config(text = file_path)

def SaveAs():
    path = asksaveasfilename(filetypes=[('C++ Files', '*.cpp')])
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)
    lb.config(text = file_path)

def Compile():
    RemovePrev()
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    code_output.insert('1.0', "Compiling...")
    command = ['g++', file_path]
    inp = code_input.get('1.0', END)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
    a, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0',  error)
    if error is not None and is_on == True:
        # i = error.index(':')
        # err = error[i-3:]
        # for t in range(0,3):
        #     if err[:t].isdigit()==False:
        #         err.replace(err[:t],'')
        multi_thread(Speak, error)
        # Speak(error)

def Run():
    RemovePrev()
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    code_output.insert('1.0', "Running...")
    command = ['g++', file_path]
    inp = code_input.get('1.0', END)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
    a, error = process.communicate()
    p = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
    code = editor.get('1.0', END)
    if "cin" or "scanf" in code:
        inp = inp.encode('ascii')   
        p.stdin.write(inp)
    output, err = p.communicate()
    # print(type(p.stdout))
    # print(p.stdout)
    # print(output)
    code_output.delete('1.0', END)
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)   
    if error is not None and is_on == True:
        # multi_thread(Speak,error)
        Speak(error)
    if output is not None and is_on == True:
        output = output.decode('utf-8')
        multi_thread(Speak, output)
        # Speak(output)
        # print(type(output))

def button_mode():
   global is_on
   
   #Determine it is on or off
   if is_on:
      switch.config(image=off)      
      multi_thread(Speak,'Deactivated voice mode')
      multi_thread(MistyMode)
    #   Speak('Deactivated voice mode')
    #   MistyMode()
      is_on = False
   else:
      switch.config(image = on)      
      multi_thread(Speak, 'Voice Mode on')
      multi_thread(VoiceMode)
    #   Speak('Voice Mode on')
    #   VoiceMode()
      is_on = True

app = Tk()
app.geometry("1200x670-100-38")
app.title('Programmophone')
app.minsize(1200, 670)

logo = ImageTk.PhotoImage(Image.open("img/cpp.png").resize((30, 30), Image.ANTIALIAS))
on = ImageTk.PhotoImage(Image.open("img/on.png").resize((60, 20), Image.ANTIALIAS))
off = ImageTk.PhotoImage(Image.open("img/off.png").resize((60, 20), Image.ANTIALIAS))

lb = Label(app, justify = RIGHT, compound = LEFT, padx = 10, text = "newfile.cpp",  font = Bfont, image = logo)

lb.pack() 

header = Menu(app)
header.add_command(label='Open', command=Open)
header.add_command(label='Save', command=Save)
header.add_command(label='Save as', command=SaveAs)
header.add_command(label='Compile', command=Compile)
header.add_command(label='Run', command=Run)
header.add_command(label='Close', command=sys.exit)
app.config(menu=header)

F1 = Frame(app, relief=SUNKEN, borderwidth=2)
F1.pack(side=TOP, fill=BOTH)

F1_left = CustomFrame(F1, height=27, relief = SUNKEN, borderwidth=2)
F1_left.pack(side=LEFT, fill = BOTH, padx=(0, 10))

F1_right = Frame(F1, relief=SUNKEN, borderwidth=2)
F1_right.pack(side = RIGHT, fill = BOTH, padx=(20, 0))

activity_lb = Label(F1_right, padx=10, text = "Activity Log", font=Bfont)
activity_lb.pack(anchor=W)

a = Scrollbar(F1_right, orient=VERTICAL)
a.pack(side=RIGHT, fill=Y, pady=(0,25))

activity_log = Text(F1_right, width = 50, height=27, yscrollcommand=a.set, borderwidth=2)
activity_log.pack(fill = BOTH, pady=(0,20))
activity_log.bind("<Key>", lambda e: "break")

a.config(command=activity_log.yview)

switch = Button(lb,image=off,bd =0,command = button_mode, anchor=E)
switch.pack(side=RIGHT, padx=(1070,0), anchor=E, expand=True)

F2 = Frame(relief = SUNKEN, borderwidth=2)
F2.pack(side=BOTTOM, fill=BOTH)

F2_left = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_left.pack(side=LEFT, fill=BOTH)
F2_right = Frame(F2, relief = SUNKEN, borderwidth=2)
F2_right.pack(side=RIGHT, fill=BOTH)

lb_in = Label(F2_left, padx = 10, text = "Input",  font = Bfont)
lb_out = Label(F2_right, padx=10, text = "Output",  font = Bfont)
lb_in.pack(anchor = 'w')
lb_out.pack(anchor='w')

b = Scrollbar(master = F2_left , orient = 'vertical')
b.pack(side=RIGHT, fill = Y)

editor = F1_left.text

code_input = Text(master = F2_left, font = Font, width=50, yscrollcommand = b.set, borderwidth=2)
code_input.pack(fill = BOTH, padx=2)

b.config(command = code_input.yview)

c = Scrollbar(master = F2_right , orient = 'vertical')
c.pack(side=RIGHT, fill = Y)

code_output = Text(master = F2_right, font = Font, width=170, yscrollcommand = c.set, borderwidth=2)
code_output.pack(fill = BOTH, padx=2)
code_output.bind("<Key>", lambda e: "break")

c.config(command = code_output.yview)

multi_thread(Start)
app.mainloop()