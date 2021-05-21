'''This file contains function for updation of logo and activity log, and run and compile fucntions, basically general utilities'''


from tkinter import *
from threading import *
from editor import *
from sr import *
import beepy
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
    if 'cpp'==filetype[1]:
        lb.config(image=logo_cp)
    elif 'txt'== filetype[1]:
        lb.config(image=logo_t)
    elif 'py'==filetype[1]:
        lb.config(image=logo_p)
    elif 'java'==filetype[1]:
        lb.config(image=logo_j)
    elif 'c'==filetype[1]:
        lb.config(image=logo_c)
    else:
        lb.config(image=logo)

def multi_thread(target, *args):
    '''
    For starting a new thread parallel to the main thread
    '''
    t = Thread(target = target, args=args)
    # print(active_count())
    #If the thread is not daemon it won't exit even if the main function is terminated and cause the system to not respond
    t.daemon=True
    t.start()

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
    Input = Listen()
    if Input is not None:
        code_input.insert(INSERT, Input)       
        edit = str(count)+ '::' + 'Added ' +  Input + ' to input block\n'
        UpdateActivity(edit, activity_log)

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
    if 'cpp'==filetype[1]:   
        code_output.insert('1.0', "Compiling...")
        command = ['g++', '-std=gnu++11', file_path]
    elif 'txt'==filetype[1]:
        multi_thread(Speak, "Can't compile .txt files")                
        code_output.insert('1.0', "Can't compile .txt files")
        return
    elif 'py'==filetype[1]:
        multi_thread(Speak, "Python is an interpreted language and not a compiled one, Click on run to run the program")                
        code_output.insert('1.0', 'Python is an interpreted language and not a compiled one\n Click on run to run the program')
        return
    elif 'java'==filetype[1]:
        file_type = file_path.split('.')
        rem = file_type[0] + '.class'
        cmd = 'rm -frv ' + rem
        p   = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        _ = p.stdout.read() 
        code_output.insert('1.0', "Compiling...")
        command = ['javac', file_path]
    elif 'c'==filetype[1]:        
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
    if 'cpp'==filetype[1]:
        Compile(text, code_input, code_output, file_path, editor, is_on)
        p = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        code = editor.get('1.0', END)
        if "cin" or "scanf" in code:
            inp = inp.encode('ascii')   
            p.stdin.write(inp)
        output, _ = p.communicate()
    elif 'txt'==filetype[1]:
        return
    elif 'py'==filetype[1]:
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
    elif 'java'==filetype[1]:
        Compile(text, code_input, code_output, file_path, editor, is_on)
        filename = file_path.split('.')
        obj = filename[0]+'.class'
        p = subprocess.Popen([obj], stdout=subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        code = editor.get('1.0', END)
        if "Scanner" in code:
            inp = inp.encode('ascii')   
            p.stdin.write(inp)
        output, _ = p.communicate()
    elif 'c'==filetype[1]:        
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