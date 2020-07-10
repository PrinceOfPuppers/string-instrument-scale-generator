import tkinter as tk
import sys
from app import App

from gui import Gui
from plotting import Plotter



if __name__ == "__main__":
    #interactivity loop works on recursion
    sys.setrecursionlimit(10**6)

    app=App()

    plotter=Plotter()


    gui=Gui(app,plotter)

    gui.mainLoop()