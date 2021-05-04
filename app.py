from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import time
from PIL import ImageTk, Image

Font = ("Comic Sans MS", "10", "normal")
file_path = ''

def Path(path):
    global file_path
    file_path = path

def Open():
    path = askopenfilename(filetypes = [('C++ Files', '*.cpp')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        Path(path)
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
    if file_path != '':
        lb.config(text = file_path)

def Compile():
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

def Run():
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

# def multiple_yview(x, y):
#     editor.yview(x, y)
#     code_input.yview(x, y)
#     code_output.yview(x, y)

app = Tk()
app.title('Programmophone')

logo = ImageTk.PhotoImage(Image.open("img/cpp.png").resize((30, 30), Image.ANTIALIAS))

lb = Label(app, justify = RIGHT, compound = LEFT, padx = 10, text = "newfile.cpp",  font = Font, image = logo)
lb.pack() 

header = Menu(app)
header.add_command(label='Open', command=Open)
header.add_command(label='Save', command=Save)
header.add_command(label='Compile', command=Compile)
header.add_command(label='Run', command=Run)
header.add_command(label='Close', command=exit)
app.config(menu=header)

a = Scrollbar(app, orient = 'vertical')
a.pack(side = RIGHT, fill = Y)

# width = 168
editor = Text(height = 20, wrap = NONE, font = Font, yscrollcommand = a.set)
# editor = Text(height = 20, width = 168, font = Font)
editor.pack(side = TOP, fill = X)
a.config(command = editor.yview)

# code_input = Text(height = 6, width = 160, wrap = NONE, font = Font, yscrollcommand = a.set)
code_input = Text(height = 6, font = Font)
code_input.pack(side = TOP, fill = X)

# code_output = Text(height = 8, width = 160, wrap = NONE, font = Font, yscrollcommand = a.set)
code_output = Text(height = 8, font = Font)
code_output.pack(side = TOP, fill = X)

app.mainloop()