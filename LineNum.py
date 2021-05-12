from tkinter import *
import tkinter.ttk as ttk
import tkinter.font
from tkinter.filedialog import asksaveasfilename, askopenfilename
from PIL import ImageTk, Image



Font = ("Comic Sans MS", "10", "normal")
Bfont = ("Comic Sans MS", "10", "bold")


class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=Bfont)
            i = self.textwidget.index("%s+1line" % i)


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
            ):
            self.event_generate("<<Change>>", when="tail")

        return result


class CustomFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self, font=Font, width=120)
        self.label = Label(self, text="Line: 0 | Char: 0", font=Bfont)
        self.vsb = Scrollbar(self, orient="vertical",
                             command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=Bfont)
        self.linenumbers = TextLineNumbers(self, width=33)
        self.linenumbers.attach(self.text)

        self.label.pack(side=BOTTOM, anchor="w")
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill=BOTH, expand=True)
        self.text.pack(side=LEFT, fill="both")
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _config_pos(self, event):
        pos = "Line: "
        pos = pos + self.text.index(INSERT)
        pos = pos.replace('.', ' | Char: ')
        self.label.config(text=pos)

    def _on_change(self, event):
        self._config_pos(event)
        self.linenumbers.redraw()