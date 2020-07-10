#!/usr/bin/env python3

import tkinter as tk
import sys

from string_theory.app import App
from string_theory.gui import Gui
from string_theory.plotting import Plotter




if __name__ == "__main__":
    #interactivity loop works on recursion
    sys.setrecursionlimit(10**6)

    app=App()

    plotter=Plotter()


    gui=Gui(app,plotter)

    gui.mainLoop()