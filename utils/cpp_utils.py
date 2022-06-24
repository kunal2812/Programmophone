'''This file contains some utilities common to both c and c++, and some specific only to c++ and associated with the editor'''

from tkinter import *
from threading import *
from utils.editor import *
from utils.speech_utils import *
import time
import beepy
from utils.general_utils import *

def IncludeHeader(command, editor, count, activity_log, activity_lb):
    '''
    For including header file, just say include followed by header file one wants to include
    '''
    command = command.replace('include', '')
    command = command.replace(' ', '')
    command = command.replace('com', 'h')
    header = "#include<"+command+'>\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, header)
    edit = str(count)+ '::' + pos + '-> '  + 'Included ' + command + ' header file\n'
    UpdateActivity(edit, activity_log)

def Namespace(command, editor, count, activity_log):
    '''
    For adding namespace
    '''
    words = command.split(' ')
    # print(words)
    namespace = 'using namespace ' + words[len(words)-2] + ';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, namespace)
    edit = str(count)+ '::' + pos + '-> ' + 'You are now using namespace ' + words[len(words)-2] + ' \n'
    UpdateActivity(edit, activity_log)

def Main(command, editor, count, activity_log, activity_lb):
    '''
    For adding main function
    '''
    command = command + '(){\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, command)
    edit = str(count)+ '::' + pos + '-> ' + 'Added main function ' +  '\n'
    editor.mark_set('insert', 'insert-1l')
    UpdateActivity(edit, activity_log)

def DeclareVar(command, editor, count, activity_log, activity_lb):
    '''
    For declaring variable
    '''
    words = command.split(' ')
    code = command.replace(words[0], '')
    edit = code
    code = code+';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Declared variable of data type ' + code + ' \n'
    UpdateActivity(edit, activity_log)

def Print(command, editor, count, activity_log):
    '''
    For printing the variables or strings or numbers
    '''
    command = command.replace('print ','')
    arg = command.split(' ')    
    code = 'std::cout '
    edit = ''
    pos = editor.index(INSERT)
    for item in arg:
        if item != '':
            edit = edit + item + ' '
            code = code + ' << ' + item
    code += ';\n'
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Printing ' + edit + ' \n'
    UpdateActivity(edit, activity_log)

def Input(command, editor, count, activity_log):
    '''
    For taking input in the program
    '''
    command = command.replace('input ','')
    arg = command.split(' ')
    print(arg) 
    edit = ''
    code = 'std::cin '
    for item in arg:
        if item != '':
            edit = edit + item + ' '
            code = code + ' >> ' +item
    code += ';\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Inputting ' + edit +  '\n'
    UpdateActivity(edit, activity_log)

def Newline(command, editor, count, activity_log):
    '''
    For adding a newline in the output stream
    '''
    code = 'std::cout << endl;\n'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    edit = str(count)+ '::' + pos + '-> ' + 'Added a newline ' + '\n'
    UpdateActivity(edit, activity_log)

def If(command, editor, count, activity_log, activity_lb):
    '''
    For initializing an else if block
    '''
    time.sleep(1)      
    beepy.beep(sound=4)
    #After the chime speak condition for the if statement
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
        UpdateActivity(edit, activity_log)
    else:
        return

def ElseIf(command, editor, count, activity_log, activity_lb):
    '''
    For initializing an else if block
    '''
    time.sleep(1)      
    beepy.beep(sound=4)
    #After the chime speak condition for the else if statement
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
        UpdateActivity(edit, activity_log)

def Else(command, editor, count, activity_log, activity_lb):
    '''
    For initializing an else block
    '''
    code = 'else{\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)
    editor.mark_set('insert', 'insert-1l')
    edit = str(count)+ '::' + pos + '-> ' + 'Added a else block' +  '\n'
    UpdateActivity(edit, activity_log)

def While(command, editor, count, activity_log, activity_lb):
    '''
    For initializing a while loop
    '''
    time.sleep(1)      
    beepy.beep(sound=4)
    #After the chime speak condition for the else if statement
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
        UpdateActivity(edit, activity_log)

def For(command, editor, count, activity_log, activity_lb):
    '''
    For adding for loop which has 3 parts, Initialization, Condition and Updation
    '''
    time.sleep(0.5)
    Speak('Initialization')
    #After initialization is said speak how you want to initialize
    p1 = Listen()
    if p1 is None:
        return    
    p1 = p1.replace(' ', '')
    time.sleep(0.5)
    Speak('Condition')
    #After condition is said speak how you want to add the condition
    p2 = Listen()
    if p2 is None:
        return
    p2 = p2.replace(' ', '')
    time.sleep(0.5)
    Speak('Updation')
    #After updation is said speak how you want to update the variable
    p3 = Listen()
    if p3 is None:
        return
    p3 = p3.replace(' ', '')
    p1 = p1.replace('none','')
    p2 = p2.replace('none','')
    p3 = p3.replace('none','')
    code = 'for(' + p1 + '; ' + p2 + '; ' + p3 + '){\n\n}'
    pos = editor.index(INSERT)
    editor.insert(INSERT, code)            
    editor.mark_set('insert', 'insert-1l')
    edit = str(count)+ '::' + pos + '-> ' + 'Added a for loop while ' + p2 +  '\n'
    UpdateActivity(edit, activity_log)

def DoWhile(command, editor, count, activity_log, activity_lb):
    '''
    For initializing a do while loop
    '''
    time.sleep(1)      
    beepy.beep(sound=4)
    #After the chime speak condition for the else if statement
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
        UpdateActivity(edit, activity_log)
    else:
        return 