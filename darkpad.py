import os
import sys
import utils
import binary_utils
from tkinter import *
from tkinter.simpledialog import askinteger,askstring
from tkinter import messagebox as msgbox
from tkinter import filedialog as fd

# Constants
BACKGROUND = '#191919'
SECONDARY_BG = '#2d2d2d'
white = 'white'
min_fsize = 2
max_fsize = 100
fonts = ["Arial","Courier","Consolas","Times"]

class DarkPad(Tk):
    """
    The entire application of DarkPad, from its GUI to commands,events,methods all packed in single class
    """
    def __init__(self,geometry) -> None:
        Tk.__init__(self)
        # Initialization
        self.__app_name = "DarkPad"
        self.title(f"Untitled - {self.app_name}")
        self._curr_file = None
        self.font_tuple = ['Consolas',12]
        self.geometry(geometry)
        self.co_ord = StringVar()
        self.wrap_var = IntVar(value=2)
        self.font_rvar = IntVar(value=2)
        self.fsize_svar = StringVar(value=f"Current font size : {self.font_tuple[1]}")
        self.nchar_svar = StringVar()

        # easter-egg -- Misc menu variables
        self.misc_menu = None
        self.ee = 0

        # creating Text widget and binding events to it
        self.main_frame = Frame(master=self,background=BACKGROUND)
        self.main_frame.pack(side=TOP,fill=BOTH,expand=True)
        self.txtarea = Text(master=self.main_frame,background=BACKGROUND,font=self.font_tuple,width=0,height=0,foreground=white,insertbackground=white,wrap=NONE,undo=True,autoseparators=True,maxundo=-1)
        self.txtarea.pack(side=LEFT,anchor=NW,fill=BOTH,expand=True)
        self.scrollbar = Scrollbar(master=self.main_frame,background=BACKGROUND,command=self.txtarea.yview)
        self.scrollbar.pack(side=RIGHT,fill=Y,anchor=E)
        self.txtarea.config(yscrollcommand=self.scrollbar.set)
        self.txtarea.bind("<Control-s>",func=lambda e:self.save_file(show_info=False))
        self.txtarea.bind("<Control-MouseWheel>",func=lambda e: self.incr_decr_fsize(e.delta))
        self.txtarea.bind("<Control-u>",func=lambda e:self.easter_egg())

        # Menus
        self.main_menu = Menu(self,background=SECONDARY_BG,fg=white)

        # File menu to create,open,save files
        self.file_menu = Menu(self.main_menu,background=SECONDARY_BG,fg=white,tearoff=0)
        self.file_menu.add_command(label="New file",command=self.create_file)
        self.file_menu.add_command(label="Open a file",command=self.open_file)
        self.file_menu.add_command(label="Save file",command=self.save_file)
        self.file_menu.add_command(label="Save as..",command=self.save_file_as)
        self.main_menu.add_cascade(label="File",menu=self.file_menu)

        # Font menu to switch between different fonts and to change font size 
        self.font_menu = Menu(self,background=SECONDARY_BG,fg=white,tearoff=0)
        for i,font in enumerate(fonts):
            self.font_menu.add_radiobutton(label=font,font=(font,10),variable=self.font_rvar,value=i,command=self.config_font,selectcolor=white)
        self.font_menu.add_separator()
        self.font_menu.add_command(label="Change font size",command=self.change_fsize)
        self.main_menu.add_cascade(label="Font",menu=self.font_menu)

        # Wrap menu to switch between wrap types : char , word, none
        self.wrap_menu = Menu(self.main_menu,background=SECONDARY_BG,fg=white,tearoff=0)
        self.wrap_menu.add_radiobutton(label="Wrap by words",variable=self.wrap_var,value=0,command=self.config_wrap,selectcolor=white)
        self.wrap_menu.add_radiobutton(label="Wrap by characters",variable=self.wrap_var,value=1,command=self.config_wrap,selectcolor=white)
        self.wrap_menu.add_radiobutton(label="No wrap",variable=self.wrap_var,value=2,command=self.config_wrap,selectcolor=white)
        self.main_menu.add_cascade(label="Wrap",menu=self.wrap_menu)
        self.config(menu=self.main_menu)

        # footer
        self.footer = Frame(master=self,background=SECONDARY_BG)
        self.footer.grid_columnconfigure(1,weight=1)
        self.footer.pack(side=TOP,fill=X,anchor=S)
        self.co_ord_label = Label(master=self.footer,background=SECONDARY_BG,foreground=white,textvariable=self.co_ord)
        self.co_ord_label.pack(side=RIGHT,anchor=E)
        self.fsize_lable = Label(master=self.footer,background=SECONDARY_BG,foreground=white,textvariable=self.fsize_svar)
        self.fsize_lable.pack(side=LEFT,anchor=W)
        self.sep = Label(master=self.footer,background=SECONDARY_BG,foreground=white,text="|",font=('consolas',10,'bold'))
        self.sep.pack(side=LEFT,anchor=W)
        self.nchar_label = Label(master=self.footer,background=SECONDARY_BG,foreground=white,textvariable=self.nchar_svar)
        self.nchar_label.pack(side=LEFT,anchor=W)
        
        # app initialization and configuration / event binding
        self.txtarea.focus()
        self.txtarea.mark_set(INSERT,"1.0")
        self.update_footer()
        self.bind("<Button>",lambda e:self.check_change())
        self.bind("<KeyPress>",lambda e:self.check_change())
        self.protocol("WM_DELETE_WINDOW",self.destroy_event)
        if len(sys.argv)>1:
            self.open_file(sys.argv[-1])
        self.update_footer()

    def easter_egg(self):
        """
        Easter egg feature : creates a new menu where encryption and decryption can be done
        this feature can be triggered by pressing ctrl+u 99 times, anytime when Misc menu is invisible
        """
        self.ee += 1
        if self.ee == 99:
            self.misc_menu = Menu(self.main_menu,background=SECONDARY_BG,fg=white,tearoff=0)
            self.misc_menu.add_command(label="Encrypt",command=self.ee_enc)
            self.misc_menu.add_command(label="Decrypt",command=self.ee_dec)
            self.misc_menu.add_separator()
            self.misc_menu.add_command(label="Text to binary",command=self.ee_t2b)
            self.misc_menu.add_command(label="Binary to text",command=self.ee_b2t)
            self.misc_menu.add_separator()
            self.misc_menu.add_command(label="Destroy!!",command=self.ee_destroy)
            self.main_menu.add_cascade(label="Misc",menu=self.misc_menu)
            self.config(menu=self.main_menu)

    def ee_enc(self):
        """
        Easter egg feature
        Encrypts the existing text using key given by user
        best to not use when text is too long
        """
        key = askstring(title="Key",prompt=f"Note: DO NOT USE THIS FEATURE IF THERE IS LOT OF TEXT,\n{' '*10} THIS MIGHT CRASH OR HANG THE APPLICATION\nEnter encryption key:")
        if key:
            key = utils.get_key(key)
            text = utils.ciph(self.content,key)
            self.content = text
            self.check_change()
    
    def ee_dec(self):
        """
        Easter egg feature
        Decrypts the existing text using key given by user
        """
        key = askstring(title="Key",prompt="Enter decryption key:\t\t\t")
        if key:
            key = utils.get_key(key)
            text = utils.deciph(self.content,key)
            self.content = text
            self.check_change()

    def ee_t2b(self):
        """
        Easter egg feature
        Converts the given text to binary 
        """
        self.content = binary_utils.text_to_binary(self.content)
        self.check_change()

    def ee_b2t(self):
        """
        Easter egg feature
        Converts binary to normal text
        """
        try:
            self.content = binary_utils.binary_to_text(self.content)
            self.check_change()
        except TypeError:
            return msgbox.showerror(title="Error",message="Given text is not binary")

    def ee_destroy(self):
        """
        destroys the Misc menu and resets the easter egg trigger counter to 0 (self.ee = 0)
        """
        self.misc_menu.destroy()
        self.main_menu.delete(4,4)
        self.ee = 0

    def destroy_event(self):
        """
        when user is trying to close the application, then this method will run and ask for confirmation
        """
        if self.fs_changed:
            resp = msgbox.askyesnocancel(title="Warning",message="You have unsaved work, do you want to save before exit?")
            if resp is None:
                return
            elif resp:
                self.save_file()
                self.destroy()
            else:
                self.destroy()
        else:
            self.destroy()
    
    def config_wrap(self):
        """
        wrap configuration, this method is used as command in self.wrap_menu
        """
        wplist = [WORD,CHAR,NONE]
        wp = wplist[self.wrap_var.get()]
        self.txtarea.config(wrap=wp)

    def config_font(self):
        """
        font configuration, this method is used as command in self.font_menu
        """
        font,size = fonts[self.font_rvar.get()], self.font_tuple[1]
        self.font_tuple[0] = font
        self.txtarea.config(font=(font,size))

    def change_fsize(self):
        """
        font size modification, this method is used as command in self.font_menu
        """
        fsize_inp = askinteger(title="Font size",prompt=f"Enter font size:\t\t\t")
        if fsize_inp:
            if fsize_inp<min_fsize:
                fsize_inp = min_fsize
            elif fsize_inp>max_fsize:
                fsize_inp = max_fsize
            else:
                pass
            self.font_tuple[1] = fsize_inp
            self.txtarea.config(font=self.font_tuple)
            self.fsize_svar.set(f"Current font size : {self.font_tuple[1]}")
        
    def check_change(self):
        """
        this method checks if there are any changes in text widget from the saved file, if there is change then '*' will be prefixed to the window title
        this method is used as <KeyPress> event handler for application (self)
        """
        self.update_footer()
        if self.fs_changed:
            if self._curr_file:
                self.title(f"* {self.curr_file} - {self.app_name}")
            else:
                self.title(f"* Untitled - {self.app_name}")
        else:
            self.title(f"{self.curr_file} - {self.app_name}")

    def update_footer(self):
        """
        updates the co-ordinates display of current position of cursor in text widget
        """
        ln,cl  = self.txtarea.index(INSERT).split('.')
        self.co_ord.set(f"Ln {ln}, Col {cl}")
        self.nchar_svar.set(f"Number of characters : {len(self.content)}")

    def update_title(self):
        """
        updates the title of application when opening a file or creating / saving a new file
        """
        if self.curr_file:
            self.title(f"{self.curr_file} - {self.app_name}")
        else:
            self.title(f"Untitled - {self.app_name}")

    def incr_decr_fsize(self,delta):
        """
        increases and decreases the font size in even numbers (with step of 2), 
        this method is used as <Control-MouseWheel> event handler for text widget
        """
        currval = self.font_tuple[1]
        currval = utils.to_even(currval)
        if delta>0:
            if currval != max_fsize:
                self.font_tuple[1] = currval+2
        else:
            if currval != min_fsize:
                self.font_tuple[1] = currval-2
        self.txtarea.config(font=self.font_tuple)
        self.fsize_svar.set(f"Current font size : {self.font_tuple[1]}")

    @property
    def curr_file(self):
        return self._curr_file

    @curr_file.setter
    def curr_file(self,filename):
        """
        sets the given file as self._curr_file and updates the window title of application
        """
        if filename:
            filename = filename.replace('/','\\')
            self._curr_file = os.path.join(os.getcwd(),filename)
        else:
            self._curr_file = filename
        self.update_title()

    @property
    def app_name(self):
        return self.__app_name
    
    @app_name.setter
    def app_name(self,v):
        return

    def create_file(self):
        """
        create a new empty file (unsaved state/Untitled)
        """
        if self.fs_changed:
            if msgbox.askyesno(title="Confirmation",message="Do you want to proceed without saving the currently opened file?"):
                pass
            else:
                return

        self.curr_file = None
        self.txtarea.delete(1.0,END)
        self.nchar_svar.set(f"Number of characters : {len(self.content)}")


    def open_file(self,filename=""):
        """
        Opens a file and writes its content into text widget
        """
        if not filename: # filename not provided, user is asked to open file
            if self.curr_file and self.fs_changed:
                if msgbox.askyesno(title="Confirmation",message="Do you want to proceed without saving the currently opened file?"):
                    pass
                else:
                    return
            else:
                pass
            file = fd.askopenfilename(title="Open a file")
            if file:
                self.curr_file = file
                with open(file,'r') as f:
                    self.content = f.read()
        else: # filename provided, opening file directly
            with open(filename,'r') as f:
                self.content = f.read()
                self.curr_file = filename
        self.nchar_svar.set(f"Number of characters : {len(self.content)}")

    def save_file(self,show_info=True):
        """
        Saves the content of file in file located at self.curr_file 
        """
        if self.fs_changed :
            if not self.curr_file:
                file = fd.asksaveasfilename(title="Save this file")
                if file:
                    self.curr_file = file
                else:
                    return
            with open(self.curr_file,'w') as f:
                f.write(self.content)
            if show_info:
                msgbox.showinfo(title="Success",message=f"Successfully saved file at {self.curr_file}")
    
    def save_file_as(self):
        """
        works similar to popular "Save as" functionality

        asks for a new file name/location and writes the content in the file
        """
        file = fd.asksaveasfilename(title="Save this file as..")
        if file:
            self.curr_file = file
            with open(self.curr_file,'w') as f:
                f.write(self.content)
            msgbox.showinfo(title="Success",message=f"Successfully saved file at {self.curr_file}")


    @property
    def fs_changed(self):
        """
        checks if the current state of text widget is changed from saved file at self.curr_file
        if self.curr_file is None, returns True
        """
        if self.curr_file:
            f_content = ""
            with open(self.curr_file,'r') as f:
                f_content = f.read()
            return not f_content == self.content
        else:
            return True
    
    @fs_changed.setter
    def fs_changed(self,v):
        return

    @property
    def content(self):
        """
        gets the entire content of text widget at the moment when this method is called, and returns it
        """
        txt = self.txtarea.get(1.0,END)
        txt = txt[:-1] if txt[-1] == "\n" else txt
        return txt
    
    @content.setter
    def content(self,strval):
        """
        takes strval : string value and writes it in text widget
        """
        self.txtarea.delete(1.0,END)
        self.txtarea.insert(1.0,strval)
	