from tkinter import *
from tkinter import filedialog

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = filedialog.askdirectory()# show an "Open" dialog box and return the path to the selected file
print(filename)