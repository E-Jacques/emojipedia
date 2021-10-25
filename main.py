from window import MainFrame
from tkinter import Tk
from sys import argv

root = Tk()
root.title("Emojipedia")
root.geometry("300x450")
MainFrame(root, work_dir=argv[1])
root.focus()
root.mainloop()