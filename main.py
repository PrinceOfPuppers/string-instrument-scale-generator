import tkinter as tk
import sys
from app import App

from gui import Gui
from plotting import Plotter
from eventHandling import EventHandler



if __name__ == "__main__":
    #interactivity loop works on recursion
    sys.setrecursionlimit(10**6)

    app=App()

    eventHand=EventHandler()
    
    plotter=Plotter()

    tkRoot=tk.Tk()
    gui=Gui(app,eventHand,plotter,tkRoot)

    gui.mainLoop(tkRoot)