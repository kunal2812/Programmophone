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
recognizer = sr.Recognizer()
is_on = False

dict =  {"hash":'#', 'slash':'/', 'hyphen':'-', 'underscore':'_', 'backslash':'\\', 
            'less than':'<', 'greater than':'>', 'asterisk':'*', 'exclamation':'!',
            'ampersand':'&', 'modulo':'%', 'plus':'+', 'minus':'-', 'divide':'/', 'dot':'.',
            'and':'&&', 'or':'||', 'bitwise and':'&', 'bitwise or':'|', 'xor': '^', 'percent':'%',
            'equalto':'=', 'equal to':'=', 'none':'', 'left shift':'<<', 'right shift':'>>', 'single quote':"''",
            'single quotes':"''", "double quote":"\"\"", "double quotes":"\"\"", 'not':'!', 'single coat':"''",
            'single coats':"''", "double coat":"\"\"", "double coats":"\"\"", 'bull':'bool','vivid':'evade', 
            'entmen':'int main', 'see out':'print', 'cout':'print', 'see in':'input', 'cin':'input', 'new line':'newline',
            'ent':'int', 'man':'main', 'men':'main', 'space':' ', 'entertain':'main'
        }

def Path(path):
    global file_path
    file_path = path

def MistyMode():
    global is_on
    while is_on==False:
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
        command = Listen()
        if command is not None:
            Action(command)
        if is_on==False:
            sys.exit()
    return

def Action(command):
    print(command)
    if 'activate' and 'voice' in command:
        Speak('Voice Mode on')
        switch.config(image = on)
        multi_thread(VoiceMode)
    elif 'deactivate' and 'voice' in command:        
        Speak('Deactivated voice mode')
        switch.config(image=off)
        multi_thread(MistyMode)
    elif 'evade' in command:
        editor.mark_set('insert', 'insert+1c')
    elif 'include' in command:
        command = command.replace('include', '')
        command = command.replace(' ', '')
        header = "#include<"
        header = header+command+'>\n'
        editor.insert(INSERT, header)
    elif 'namespace' in command:
        words = command.split(' ')
        print(words)
        namespace = 'using namespace ' + words[len(words)-2] + ';\n'
        editor.insert(INSERT, namespace)
    elif 'declare' in command:
        words = command.split(' ')
        code = command.replace(words[0], '')
        code = code+';\n'
        editor.insert(INSERT, code)
    elif 'print' and 'newline' in command:
        arguments = Listen()
        if arguments is None:
            return
        code = 'std::cout << ' + arguments + '<< endl;\n'
        editor.insert(INSERT, code)
    elif 'print' in command:
        arguments = Listen()
        if arguments is None:
            return
        arguments.replace(' ', '<<')
        code = 'std::cout << ' + arguments + ';\n'
        editor.insert(INSERT, code)
    elif 'input' in command:
        arguments = Listen()
        if arguments is None:
            return
        arguments.replace(' ', '>>')
        code = 'std::cin >> ' + arguments + ';\n'
    elif 'dot' or '.' in command:
        arguments = Listen()
        if arguments is not None:
            command = command + '('
            command = command + arguments + ');\n'
            editor.insert('INSERT', command)
        else:
            sys.exit()
    elif 'else' and 'if' in command:
        condition = Listen()
        if condition is not None:
            code = 'else if('
            code = code + condition
            code = code + '){\n\n}'
            editor.insert(INSERT, code)            
            editor.mark_set('insert', 'insert-1c')
        else:
            sys.exit()
    elif 'else' in command and 'if' not in command:
        code = 'else{\n\n}'
        editor.insert(INSERT, code)
        editor.mark_set('insert', 'insert-1c')
    elif "if" and "statement" in command:
        condition = Listen()
        if condition is not None:
            code = 'if('
            code = code + condition
            code = code + '){\n\n}'
            editor.insert(INSERT, code)            
            editor.mark_set('insert', 'insert-1c')
        else:
            return
    elif 'do' and 'while' in command:
        condition = Listen()
        if condition is not None:
            code = 'do{\n\n}\nwhile('
            code = code + condition
            code = code + ')'
            editor.insert(INSERT, code)            
            editor.mark_set('insert', 'insert-1c')
        else:
            return
    elif 'while' in command:
        condition = Listen()
        if condition is not None:
            code = 'while('
            code = code + condition
            code = code + '){\n\n}'
            editor.insert(INSERT, code)            
            editor.mark_set('insert', 'insert-1c')
        else:
            return
    elif 'for' and 'loop' in command:
        Speak('Initialization')
        p1 = Listen()
        if p1 is None:
            return
        Speak('Condition')
        p2 = Listen()
        if p2 is None:
            return
        Speak('Updation')
        p3 = Listen()
        if p3 is None:
            return
        code = 'for(' + p1 + '; ' + p2 + '; ' + p3 + '){\n\n}'
        editor.insert(INSERT, code)            
        editor.mark_set('insert', 'insert-1c')
    elif 'main' in command:
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
    print(active_count())
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
        multi_thread(Speak, error)
    if output is not None and is_on == True:
        output = output.decode('utf-8')
        multi_thread(Speak, output)

def SaveVoice(file_path, editor, lb):
    if file_path == '':
        p = 'files/'
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
            SaveVoice(file_path, editor, lb)
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        Path(path)    
    if file_path != '':
        lb.config(text = file_path)

def OpenVoice(editor, lb):
    p = 'files/'
    Speak('Which one of the following would you like me to open ?')
    files = os.listdir(p)
    for file in files:
        Speak(file)
        time.sleep(2)
    command = Listen()
    command = command.lower()
    command = command.replace('dot', '.')
    command = command.replace(' ', '')
    path = os.path.join(p, command)
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
        multi_thread(Speak, 'Voice Mode on')
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