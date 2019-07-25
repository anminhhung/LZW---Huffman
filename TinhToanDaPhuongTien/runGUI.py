import GUI
from tkinter import *

if __name__ == "__main__":
    root = Tk()
    app = GUI.GUI(root)
    app.setWindow()
    app.drawUI()
    root.mainloop()