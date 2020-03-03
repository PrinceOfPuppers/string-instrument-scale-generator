import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from helperFuncs import getTuningList,getPlotSize

def makeGraphText(app):
    note= lambda interval : app.noteGivenInterval(app.scale,app.root,interval)
    scaleNotes=[note(interval) for interval in range(1,8)]

    #capitalizes text and converts lists of notes to strings
    rootText=app.root
    scaleNameText=app.scale
    scaleNoteText=" ".join(tone for tone in scaleNotes)
    tuningText=" ".join(tone for tone in app.tuning)

    intervalArrayTitle="{} {} ({}) with Tuning {} ".format(rootText,scaleNameText,scaleNoteText,tuningText)
    
    stringLabels=[tone.capitalize() for tone in app.tuning]
    fretLabels=["open"]+[i for i in range(1,app.numFrets)]

    return(intervalArrayTitle,stringLabels,fretLabels)

def onClick(event,cfg,app,fig,ax):
    if event.button==1:
        if cfg.debug:
            print("click type {}".format(event.button))
        #coordinates are flipped
        boxClicked=(int(event.ydata+0.5),int(event.xdata+0.5))
        try:
            newRootInterval=app.intervalArray[boxClicked[0]][boxClicked[1]]
            if newRootInterval!=app.nonIntervalNum:
                print("Setting {} as new root".format(int(newRootInterval)))
                intervalArray=app.changeMode(newRootInterval)

                newTitle,stringLabels,fretLabels=makeGraphText(app)

                ax.clear()
                ax.imshow(intervalArray,cmap=cfg.colorMap)
                for i in range(len(stringLabels)):  
                    for j in range(len(fretLabels)):
                        if intervalArray[i, j]==app.nonIntervalNum:
                            label=" "
                        else:
                            label=int(intervalArray[i, j])
                        ax.text(j ,i , label, ha="center", va="center", color="black")
                
                ax.set_xticks(np.arange(len(fretLabels)))
                ax.set_yticks(np.arange(len(stringLabels)))
                ax.set_xticklabels(fretLabels,color='white')
                ax.set_yticklabels(stringLabels,color='white')
                plt.gca().invert_yaxis()
                
                plt.title(newTitle,color="white")
                plt.show()
        except:
            if cfg.debug:
                print("clicked offscreen")




def showIntervalArray(app,cfg,intervalArray,title,stringLabels,fretLabels):
    if cfg.autoClosePlot:
        plt.close()

    fig=plt.figure(figsize=getPlotSize(fretLabels,stringLabels),num="Click To Change Root")
    ax=fig.add_subplot(111)
    fig.patch.set_facecolor('#404040')
    fig.canvas.mpl_connect('button_press_event', lambda event: onClick(event,cfg,app,fig,ax))
    
    
    ax.imshow(intervalArray,cmap=cfg.colorMap)

    ax.set_xticks(np.arange(len(fretLabels)))
    ax.set_yticks(np.arange(len(stringLabels)))
    
    for i in range(len(stringLabels)):  
        for j in range(len(fretLabels)):
            if intervalArray[i, j]==app.nonIntervalNum:
                label=" "
            else:
                label=int(intervalArray[i, j])
            ax.text(j, i, label, ha="center", va="center", color="black")

    plt.title(title,color='white')
    
    ax.set_xticklabels(fretLabels,color='white')
    ax.set_yticklabels(stringLabels,color='white')
    plt.gcf().tight_layout()
    
    plt.gca().invert_yaxis()

    plt.show()

def generateAndShowPlot(app,cfg,tuning,root,scale):
    app.update(scale,root,tuning)
    intervalArray=app.makeIntervalArray()
    title,stringLabels,fretLabels=makeGraphText(app)
    showIntervalArray(app,cfg,intervalArray,title,stringLabels,fretLabels)




class Gui:
    def __init__(self,app,cfg,tkRoot):
        self.generateTkinterObjs(app,cfg,tkRoot)
        self.makeLayout()

    def generateTkinterObjs(self,app,cfg,tkRoot):
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
        generateButton=tk.Button(window,text="Generate",command=lambda: generateAndShowPlot(app,cfg,getTuningList(tuningStrVar),root.get(),scale.get()))
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