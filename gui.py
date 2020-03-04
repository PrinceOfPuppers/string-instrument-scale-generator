import tkinter as tk
import numpy as np

from helperFuncs import getTuningList


class Gui:
    def __init__(self,app,cfg,eventHand,plotter,tkRoot):
        self.generateTkinterObjs(app,cfg,eventHand,plotter,tkRoot)
        self.makeLayout()

    def generateTkinterObjs(self,app,cfg,eventHand,plotter,tkRoot):
        tkRoot.geometry(cfg.tkinterWinSize)
        tkRoot.option_add( "*font", cfg.tkinterFont)
        window=tk.Frame(tkRoot)
        window.pack(fill='both',expand=True)
        window.configure(background= '#404040')


        #root note selection
        rootLabel=tk.Label(window,text="Root:")
        rootLabel.configure(background= '#404040',foreground="white",borderwidth=2)
        root = tk.StringVar(window)
        root.set(app.noteList[0])

        rootDropDown = tk.OptionMenu(window, root, *app.noteList)
        rootDropDown.configure(background= '#808080',highlightthickness=0)
        rootDropDown["menu"].configure(background= '#808080')


        #scale selection
        scaleLabel=tk.Label(window,text="Scale:")
        scaleLabel.configure(background= '#404040',foreground="white")

        scale = tk.StringVar(window)
        scale.set(app.diatonicList[0])

        scaleDropDown = tk.OptionMenu(window, scale, *app.diatonicList)
        scaleDropDown.configure(background= '#808080',highlightthickness=0)
        scaleDropDown["menu"].configure(background= '#808080')

        #tuning
        tuningLabel=tk.Label(window,text="Tuning:")
        tuningLabel.configure(background= '#404040',foreground="white")

        tuningStrVar=tk.StringVar(window)
        tuningStrVar.set(cfg.defaultTuning)
        tuningTextBox=tk.Entry(window,textvariable=tuningStrVar, justify="center")
        tuningTextBox.configure(background= '#808080',highlightthickness=0)


        #generate button
        generateButton=tk.Button(window,text="Generate",command=lambda: eventHand.generateButton(app,cfg,plotter,getTuningList(tuningStrVar),root.get(),scale.get()))
        generateButton.configure(background= 'red',activebackground='#404040')

    
        self.window=window
        self.rootLabel=rootLabel
        self.rootDropDown=rootDropDown
        self.scaleLabel=scaleLabel
        self.scaleDropDown=scaleDropDown
        self.tuningLabel=tuningLabel
        self.tuningTextBox=tuningTextBox
        self.generateButton=generateButton
    
    def makeLayout(self):
        self.rootLabel.grid(row=0,column=0)
        self.rootDropDown.grid(row=0,column=1,sticky=tk.NSEW)

        self.scaleLabel.grid(row=1,column=0)
        self.scaleDropDown.grid(row=1,column=1,sticky=tk.NSEW)

        self.tuningLabel.grid(row=2,column=0,sticky=tk.NSEW)
        self.tuningTextBox.grid(row=2,column=1,sticky=tk.NSEW)

        self.generateButton.grid(row=3, columnspan=2,sticky=tk.NSEW)


        for row in range(0,4):
            for column in range(0,2):
                self.window.columnconfigure(column, weight=1)
                self.window.rowconfigure(row,weight=1)
    
    def mainLoop(self,tkRoot):
        tkRoot.mainloop()