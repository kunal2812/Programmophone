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
from LineNum import *
from sr import *

Font = ("Comic Sans MS", "10", "normal")
Bfont = ("Comic Sans MS", "10", "bold")
file_path = ''
recognizer = sr.Recognizer()
is_on = False
count = 1

def Path(path):
    global file_path
    file_path = path

def MistyMode():
    global is_on
    while is_on==False:
        # print(is_on)
        command = Listen()
        if command is not None:
            if 'hey' and 'misty' in command:
                command = command.replace('hey', '')
                command = command.replace('misty', '')
                Action(command)
        if is_on:
            sys.exit()
    return

def VoiceMode():
    global is_on
    while is_on==True:
        # print(is_on)
        command = Listen()
        if command is not None:
            Action(command)
        if is_on==False:
            sys.exit()
    return

def UpdateActivity(edit):
    global count    
    activity_log.config(state='normal')
    activity_log.insert(END, edit)
    activity_log.config(state='disabled')
    count+=1

def Activate():
    global is_on
    Speak('Voice Mode on')
    is_on = True
    switch.config(image = on)
    multi_thread(VoiceMode)

def Deactivate():
    global is_on
    is_on = False      
    Speak('Deactivated voice mode')
    switch.config(image=off)
    multi_thread(MistyMode)

def Close():    
    Speak('Exiting....')
    sys.exit()

def TellPos():
    pos = "at line "
    pos = pos + editor.index(INSERT)
    pos = pos.replace('.', ' and column ')
    multi_thread(Speak,pos)

def DeletePosLeft(index):
    index = 'insert-'+index
    deleted = editor.get(index, INSERT)
    pos = editor.index(INSERT)
    editor.delete(index, INSERT)
    edit = str(count)+ '::' + pos + '->' + 'Deleted ' + index[0] + ' characters towards left ' + deleted + '\n'
    UpdateActivity(edit)

def DeletePosRight(index):
    index = 'insert+'+index
    pos = editor.index(INSERT)
    deleted = editor.get(INSERT, index)
    editor.delete(INSERT, index)
    edit = str(count)+ '::' + pos + '->' + 'Deleted ' + index[0]+ ' characters towards right ' + deleted + '\n'
    UpdateActivity(edit)

def DeletePosAll(index):
    pos = editor.index(INSERT)
    editor.delete('1.0',END)
    edit = str(count)+ '::' + pos + '->' + 'Cleared editor\n'
    UpdateActivity(edit)

def DeletePos(command):
    words = command.split(' ')
    t = len(words)
    if t==3:
        pos = 1
    else:
        pos = words[t-2]
    index = str(pos) + 'c'
    dict = {'left':DeletePosLeft, 'right':DeletePosRight, 'all':DeletePosAll}
    for item in dict.keys():
        if item in command:
            dict[item](index)

def MovePosUp(command,pos):
    index = 'insert-' + str(pos) + 'l'
    editor.mark_set(INSERT, index)

def MovePosTo(command,pos):
    print('Here')
    words = command.split(' ')
    # print(words)
    pos = []
    for word in words:
        if word.isdigit()==True:
            pos+=word
    # print(pos)
    if 'line' not in command:
        ind = editor.index(INSERT)
        index = ind.split('.')
        index = index[0] + pos[0]
    elif 'column' not in command:
        index = pos[0]+'.'+'0'
    else:
        index = pos[0]+'.'+pos[1]
        # print(index)
    editor.mark_set(INSERT, index)

def MovePosLeft(command, pos):
    index = 'insert-' + str(pos) + 'c'
    editor.mark_set(INSERT, index)

def MovePosRight(command, pos):
    index = 'insert+' + str(pos) + 'c'
    editor.mark_set(INSERT, index)

def MovePosDown(command, pos):
    index = 'insert+' + str(pos) + 'l'
    editor.mark_set(INSERT, index)

def MovePos(command):
    words = command.split(' ')
    t = len(words)
    if t==3:
        pos = 1
    else:
        pos = words[t-2]
    dict = {'up':MovePosUp, 'line':MovePosTo, 'column':MovePosTo, 'left':MovePosLeft,'right':MovePosRight,'down':MovePosDown}
    for item in dict.keys():
        if item in command:
            dict[item](command,pos)
            break

def IncludeHeader(command):
    command = command.replace('include', '')
    command = command.replace(' ', '')
    header = "#include<"+command+'>\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, header)
    edit = str(count)+ '::' + pos + '-> '  + 'Included ' + command + ' header file\n'
    UpdateActivity(edit)

def Namespace(command):
    words = command.split(' ')
    # print(words)
    namespace = 'using namespace ' + words[len(words)-2] + ';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, namespace)
    edit = str(count)+ '::' + pos + '-> ' + 'You are now using namespace ' + words[len(words)-2] + ' \n'
    UpdateActivity(edit)

def DeclareVar(command):
    words = command.split(' ')
    code = command.replace(words[0], '')
    edit = code
    code = code+';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Declared variable of data type ' + code + ' \n'
    UpdateActivity(edit)

def Print(command):
    command = command.replace('print ','')
    arg = command.split(' ')    
    code = 'std::cout '
    edit = ''
    pos = editor.index(INSERT)
    for item in arg:
        if item is not '':
            edit = edit + item + ' '
            code = code + ' << ' + item
    code += ';\n'
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Printing ' + edit + ' \n'
    UpdateActivity(edit)

def Newline(command):
    code = 'std::cout << endl;\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Added a newline ' + '\n'
    UpdateActivity(edit)

def Input(command):
    command = command.replace('input ','')
    arg = command.split(' ')
    print(arg) 
    edit = ''
    code = 'std::cin '
    for item in arg:
        if item is not '':
            edit = edit + item + ' '
            code = code + ' >> ' +item
    code += ';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Inputting ' + edit +  '\n'
    UpdateActivity(edit)

def For(command):
    Speak('Initialization')
    p1 = Listen()
    p1 = p1.replace(' ', '')
    if p1 is None:
        return
    Speak('Condition')
    p2 = Listen()
    p2 = p2.replace(' ', '')
    if p2 is None:
        return
    Speak('Updation')
    p3 = Listen()
    p3 = p3.replace(' ', '')
    if p3 is None:
        return
    p1 = p1.replace('none','')
    p2 = p2.replace('none','')
    p3 = p3.replace('none','')
    code = 'for(' + p1 + '; ' + p2 + '; ' + p3 + '){\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)            
    editor.mark_set('insert', 'insert-1l')
    edit = str(count)+ '::' + pos + '-> ' + 'Added a for loop while ' + p2 +  '\n'
    UpdateActivity(edit)

def ElseIf(command):
    condition = Listen()
    condition = condition.replace(' ', '')
    if condition is not None:
        code = 'else if('
        code = code + condition
        code = code + '){\n\n}'
        pos = editor.index(INSERT)
        editor.insert(INSERT, code)            
        editor.mark_set('insert', 'insert-1l')
        edit = str(count)+ '::' + pos + '-> ' + 'Added a else if block, where condition is ' + condition +  '\n'
        UpdateActivity(edit)

def Else(command):
    code = 'else{\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    editor.mark_set('insert', 'insert-1l')
    edit = str(count)+ '::' + pos + '-> ' + 'Added a else block' +  '\n'
    UpdateActivity(edit)

def If(command):
    condition = Listen()
    condition = condition.replace(' ', '')
    if condition is not None:
        code = 'if('
        code = code + condition
        code = code + '){\n\n}'
        pos = editor.index(INSERT)
        editor.insert(INSERT, code)            
        editor.mark_set('insert', 'insert-1l')
        edit = str(count)+ '::' + pos + '-> ' + 'Added a else if block, where condition is ' + condition +  '\n'
        UpdateActivity(edit)
    else:
        return

def DoWhile(command):
    condition = Listen()
    condition = condition.replace(' ', '')
    if condition is not None:
        code = 'do{\n\n}\nwhile('
        code = code + condition
        code = code + ')'
        pos = editor.index(INSERT)
        editor.insert(INSERT, code)
        edit = str(count)+ '::' + pos + '-> ' + 'Added a do while loop with condition ' + condition +  '\n'           
        editor.mark_set('insert', 'insert-2l')
        UpdateActivity(edit)
    else:
        return  

def Main(command):
    command = command + '(){\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, command)
    edit = str(count)+ '::' + pos + '-> ' + 'Added main function ' +  '\n'
    editor.mark_set('insert', 'insert-1l')
    UpdateActivity(edit)

def While(command):
    condition = Listen()
    condition = condition.replace(' ', '')
    if condition is not None:
        code = 'while('
        code = code + condition
        code = code + '){\n\n}'
        pos = editor.index(INSERT)
        editor.insert(INSERT, code)       
        edit = str(count)+ '::' + pos + '-> ' + 'Added a while loop here with condiiton ' +  condition + '\n'     
        editor.mark_set('insert', 'insert-1l')
        UpdateActivity(edit)

def Brackets(command):
    if 'square' in command:
        code = '[]'
    elif 'round' in command:
        code = '()'
    elif 'curly' in command:
        code = '{}'
    editor.insert(INSERT, code)
    editor.mark_set('insert','insert-1c')
def Extra(command):
    pos = editor.index(INSERT)
    editor.insert(INSERT, command)
    edit = str(count)+ '::' + pos + '-> ' + 'Adding ' +  command + '\n'
    UpdateActivity(edit)

def Action(command):
    print(command)
    control = {'deactivate':Deactivate, 'activate':Activate, 'open':OpenVoice, 'save':SaveVoice, 'compile':Compile, 'close':Close, 'exit':Close, 'run':Run}
    cursor = {'position':TellPos, 'remove':DeletePos, 'move':MovePos}
    keywords = {'include':IncludeHeader, 'namespace':Namespace, 'main':Main, 'declare':DeclareVar, 'print':Print, 'newline':Newline, 'input':Input,
                 'for':For, 'else if':ElseIf, 'else statement':Else, 'if statement':If, 'do while':DoWhile, 'while':While, 'brackets':Brackets, '':Extra
                }
    for item in control.keys():
        if item in command:
            print('control')
            control[item]()
            return
    for item in cursor.keys():
        if item in command:
            print('cursor')
            cursor[item](command)
            TellPos()
            return
    for item in keywords.keys():
        if item in command:
            print(item)
            keywords[item](command)
            TellPos()
            return

    if '.' in command:
        arguments = Listen()
        if arguments is not None:
            command = command + '('
            command = command + arguments + ');\n'
            editor.insert('INSERT', command)
    else:
        return
    
def multi_thread(target, *args):
    t = Thread(target = target, args=args)
    # print(active_count())
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
        multi_thread(Speak,'Please save your code first')
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
        Speak('Compiled successfully')
        multi_thread(Speak, error)

def Run():
    RemovePrev()
    if file_path == '':
        multi_thread(Speak,'Please save your code first')
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
        Speak('Compiled and Ran successfully')
        multi_thread(Speak, error)
        
    if output is not None and is_on == True:        
        Speak('Compiled and Ran successfully')
        output = output.decode('utf-8')
        multi_thread(Speak, output)

def SaveVoice():
    if file_path == '':
        p = os.getcwd()+'/'
        Speak('What name would you like me to give to the file ?')
        command = Listen()
        command = command.lower()
        command = command.replace('dot', '.')
        command = command.replace(' ', '')
        
        Speak('I am saving it as ')
        for char in command:
            Speak(char)
        Speak('Say yes to confirm and no to try again')
        cmd = Listen()
        cmd = cmd.lower()
        if 'yes' in cmd:
            path = os.path.join(p, command)
        else:
            SaveVoice()
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)    
    if file_path != '':
        lb.config(text = file_path)

def OpenVoice():
    p = 'files/'
    Speak('Which one of the following would you like me to open ?')
    files = os.listdir(p)
    for file in files:
        Speak(file)
        time.sleep(1)
    command = Listen()
    if command is not None:
        command = command.lower()
        command = command.replace('dot', '.')
        command = command.replace(' ', '')
        path = os.path.join(p, command)
    else:
        return
    if os.path.isfile(path):
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            Path(path)
        if file_path != '':
            lb.config(text = file_path)
    else:
        Speak('Try Again')

def button_mode():
    global is_on

    if is_on:
        switch.config(image=off)        
        is_on = False    
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

logo = ImageTk.PhotoImage(Image.open("assets/cpp.png").resize((30, 30), Image.ANTIALIAS))
on = ImageTk.PhotoImage(Image.open("assets/on.png").resize((60, 20), Image.ANTIALIAS))
off = ImageTk.PhotoImage(Image.open("assets/off.png").resize((60, 20), Image.ANTIALIAS))

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
font = tkinter.font.Font(font=editor['font'])
editor.config(tabs=font.measure('           '))
editor.see(INSERT)

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