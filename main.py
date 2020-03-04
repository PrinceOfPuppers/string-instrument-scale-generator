from app import App
from config import Config
from gui import Gui,EventHandler,Plotter
import tkinter as tk


if __name__ == "__main__":
    cfg=Config()
    app=App(cfg)

    eventHand=EventHandler()
    plotter=Plotter()

    tkRoot=tk.Tk()
    gui=Gui(app,cfg,eventHand,plotter,tkRoot)

    gui.mainLoop(tkRoot)