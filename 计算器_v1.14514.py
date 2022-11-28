import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox as messagebox
import threading
import time

class MyApp(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=1, width=400, height=280)
        self.entryVal = ttk.StringVar(value="")
        self.__setup_widgets()
    
    def __insertEntry(self, n: str):
        self.entryVal.set(self.entryVal.get()+n)
    
    def __parseButton(self, c: str):
        if c in ["+", "-", "x", "/", "."]:
            if not self.entryVal.get()[-1:] in ["+", "-", "x", "/", "."]:
                self.__insertEntry(c)
        elif c == "c":
            self.entryVal.set("")
        elif c == "=":
            self.entryVal.set(eval(self.entryVal.get().replace("x", "*")))
        elif c == "←":
            if len(self.entryVal.get()) != 0: self.entryVal.set(self.entryVal.get()[:-1])
    
    def __aboutMe(self):
        messagebox.show_info(message="计算器 by affggh\nLicense GPLv3", title="关于")

    def __setup_widgets(self):
        column, row = 0, 1
        entry = ttk.Entry(self, textvariable=self.entryVal)
        entry.grid(column=0, row=0, columnspan=4)
        for i in ["x", "/", "c", "←"]:
            b = ttk.Button(self, text=str(i), command=lambda x=i:self.__parseButton(x), width=2)
            b.grid(row=row, column=column, padx=1, pady=1)
            column += 1
        column -= 1
        for i in ["-", "+", "="]:
            row += 1
            b = ttk.Button(self, text=str(i), command=lambda x=i:self.__parseButton(x), width=2)
            b.grid(row=row, column=column, padx=1, pady=1)
        column = 0
        row = 2
        for i in range(1, 10):
            b = ttk.Button(self, text=str(i), command=lambda x=str(i):self.__insertEntry(x), width=2)
            b.grid(row=row, column=column, padx=1, pady=1)
            column += 1
            if i%3 == 0: row += 1
            if column == 3: column = 0
        row += 1
        ttk.Button(self, text=".", command=lambda:self.__parseButton("."), width=2).grid(row=row, column=0, padx=1, pady=1, sticky='nsew')
        ttk.Button(self, text="0", command=lambda:self.__insertEntry("0"), width=2).grid(row=row, column=1, padx=1, pady=1, sticky='nsew')
        ttk.Button(self, text="关于", command=self.__aboutMe).grid(row=row, column=2, columnspan=2, padx=1, pady=1, sticky='nsew')
        
        

class TitleBar(ttk.Frame):
    def __init__(self, parent: ttk.Window, title="My title"):
        super().__init__(master=parent)
        self.title = title
        self.bootstyle = "info"
        self.__clickX, self.__clickY = 0, 0
        self.__setupTitlebar()
        self.bind("<Button-1>", self.__onClick)
        self.bind('<B1-Motion>', self.__onMotion)
    
    def __onClick(self, event):
        self.__clickX = event.x
        self.__clickY = event.y
        
    def __onMotion(self, event):
        self.master.geometry(f'{self.master.winfo_width()}x{self.master.winfo_height()}+'
                      f'{int(self.master.winfo_x() + event.x - self.__clickX)}+'
                      f'{int(self.master.winfo_y() + event.y - self.__clickY)}')
        
    def __setupTitlebar(self):
        self.titlebar = ttk.Label(self, anchor='e', text=self.title, bootstyle=self.bootstyle)
        self.titlebar.pack(side='left', anchor='w', fill='x', padx=2, pady=2)
        self.close = ttk.Button(self, text="×", command=lambda:self.onClosing(self.master), width=1, style="danger")
        self.close.pack(side='right', anchor='w', padx=2, pady=2)

    def __onClosing(self, root: ttk.Window):
        def center_window(root, width, height):  
            screenwidth = root.winfo_screenwidth()  
            screenheight = root.winfo_screenheight()  
            size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  
            root.geometry(size)
        j = 1
        for i in range(root.winfo_height(),10,-4):
            k = 0.9*i
            j *= 0.9
            # size = '%dx%d' % (1000, k)
            center_window(root, root.winfo_width(),k)
            root.wm_attributes("-alpha", j)
            time.sleep(0.001)
        root.destroy()

    def onClosing(self, root: ttk.Window):
        th = threading.Thread(target=self.__onClosing, args=[root])
        th.daemon = True
        th.start()

if __name__ == '__main__':

    root = ttk.Window(themename="darkly")

    root.wm_attributes("-topmost", True)
    root.overrideredirect(True)
    root.wm_attributes("-alpha", 0.85)
    root.wm_attributes("-toolwindow", True)
    # root.wm_attributes("-fullscreen", True)

    titlebar = TitleBar(root, title="计算器")
    # titlebar.configure(bootstyle="info")
    titlebar.pack(side="top", fill='x')

    myapp = MyApp(root)

    myapp.pack()

    root.update()
 
    screenwidth = root.winfo_screenwidth()  
    screenheight = root.winfo_screenheight()  
    size = '%dx%d+%d+%d' %(root.winfo_width(), root.winfo_height(), \
                           (screenwidth - root.winfo_width())/2, (screenheight - root.winfo_height())/2)  
    root.geometry(size)
    root.protocol("WM_DELETE_WINDOW", lambda:titlebar.onClosing(root))

    root.mainloop()