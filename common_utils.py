'''This file contains utilities common to all type of files and associated with the editor'''

from tkinter import *
from threading import *
from utils import *

def TellPos(command, editor, count, activity_log, code_input):
    '''
    Tells the current position of the cursor
    '''
    pos = "at line "
    pos = pos + editor.index(INSERT)
    pos = pos.replace('.', ' and column ')
    multi_thread(Speak,pos)

def DeletePosLeft(index, editor, count, activity_log):
    '''
    Deletes <x> characters left of the cursor
    '''
    ind = index.split('c')
    index = 'insert-'+index
    deleted = editor.get(index, INSERT)
    pos = editor.index(INSERT)
    editor.delete(index, INSERT)
    edit = str(count)+ '::' + pos + '->' + 'Deleted ' + ind[0] + ' characters towards left ' + deleted + '\n'
    UpdateActivity(edit, activity_log)

def DeletePosRight(index, editor, count, activity_log):
    '''
    Deletes <x> characters right of the cursor
    '''
    ind = index.split('c')
    index = 'insert+'+index
    pos = editor.index(INSERT)
    deleted = editor.get(INSERT, index)
    editor.delete(INSERT, index)
    edit = str(count)+ '::' + pos + '->' + 'Deleted ' + ind[0]+ ' characters towards right ' + deleted + '\n'
    UpdateActivity(edit, activity_log)

def DeletePosAll(index, editor, count, activity_log):
    '''
    Clears the editor
    '''
    pos = editor.index(INSERT)
    editor.delete('1.0',END)
    edit = str(count)+ '::' + pos + '->' + 'Cleared editor\n'
    UpdateActivity(edit, activity_log)

def MovePosUp(command,pos, editor):
    '''
    Moves <x> lines up from the current position
    '''
    index = 'insert-' + str(pos) + 'l'
    editor.mark_set(INSERT, index)

def MovePosTo(command, pos, editor):
    '''
    Moves the cursor to line <x> and column <y>
    Can be used in 3 ways
    1.Move to line x
    2.Move to column y
    3.Move to line x column y
    '''
    words = command.split(' ')
    pos = []
    for word in words:
        if word.isdigit()==True:
            pos.append(word)
    print(pos)
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

def MovePosLeft(command, pos, editor):
    '''
    Moves <x> positions left of the current position or move left
    '''
    index = 'insert-' + str(pos) + 'c'
    editor.mark_set(INSERT, index)

def MovePosRight(command, pos, editor):
    '''
    Moves <x> characters right of the current position or move right
    '''
    index = 'insert+' + str(pos) + 'c'
    editor.mark_set(INSERT, index)

def MovePosDown(command, pos, editor):
    '''
    Moves <x> lines down or move down
    '''
    index = 'insert+' + str(pos) + 'l'
    editor.mark_set(INSERT, index)

def MovePos(command, editor, count, activity_log, code_input):
    '''
    Common function for invoking specific actions associated with the cursor
    '''
    words = command.split(' ')
    t = len(words)
    if t==3:
        pos = 1
    else:
        pos = words[t-2]
    dict = {'up':MovePosUp, 'line':MovePosTo, 'column':MovePosTo, 'left':MovePosLeft,'right':MovePosRight,'down':MovePosDown}
    for item in dict.keys():
        if item in command:
            dict[item](command, pos, editor)
            break

def DeletePos(command, editor, count, activity_log, code_input):
    '''
    Common function for invoking specific actions associated with the deletion
    '''
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
            dict[item](index, editor, count, activity_log)

def Brackets(command, editor, count, activity_log):
    '''
    For adding the brackets
    '''
    if 'square' in command:
        code = '[]'
    elif 'round' in command:
        code = '()'
    elif 'curly' in command:
        code = '{}'
    editor.insert(INSERT, code)
    editor.mark_set('insert','insert-1c')

def Extra(command, editor, count, activity_log):
    '''
    For adding anything onto the editor, just say 'add' followed by anything you want to add to the editor
    '''
    command = command.replace('add', '')
    pos = editor.index(INSERT)
    editor.insert(INSERT, command)
    edit = str(count)+ '::' + pos + '-> ' + 'Adding ' +  command + '\n'
    UpdateActivity(edit, activity_log)

def Enter(command, editor, count, activity_log, code_input):
    '''
    Just say enter to invoke an action same as pressing enter
    '''
    editor.insert(INSERT, '\n')
    beepy.beep(sound=3)

def Escape(command, editor, count, activity_log, code_input):
    '''
    Utility function for escaping from the local region defined by curly braces
    For example someone added a for loop and added conditions and code to the for block, now he doesn't know (if he can't see) how many positions towards the right he should move to add code below the for block so he can just say escape and get right next to '} - closing brace'
    '''
    code = editor.get(INSERT, END)
    count = 0
    count_char = 0
    for char in code:
        if char=='{':
            count+=1
        elif char=='}' and count==0:
            break
        elif char=='}':
            count-=1
        count_char+=1
    count_char+=1
    ind = 'insert+' + str(count_char) + 'c'
    editor.mark_set('insert',ind)

def ReadLine(command, editor, count, activity_log, code_input):
    '''
    For reading a line normally or character by character if the person isn't able to still understand what's in the line
    1.Read line <x> 
    2.Read line <x> char by char
    '''
    lst = command.split(' ')
    code = editor.get('1.0', END)
    if len(lst) <= 2:
        multi_thread(Speak, code)
    else:
        ind = int(lst[2])
        lines = code.split('\n')
        line = lines[ind-1]
        if 'character' in command:
            for char in line:
                Speak(char)
        else:
            Speak(line)