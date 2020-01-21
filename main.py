from app import App
from config import Config
from gui import Gui
import tkinter as tk


if __name__ == "__main__":
    cfg=Config()
    app=App(cfg)

    tkRoot=tk.Tk()
    gui=Gui(app,cfg,tkRoot)

    gui.mainLoop(tkRoot)