from app import App
from config import Config
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

def getTuningList(tuningStrVar):
    tuningString=tuningStrVar.get().strip()
    return [note.capitalize() for note in tuningString.split(" ")]

def generateTkinterObjs(app,cfg,tkRoot):
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
    generateButton=tk.Button(window,text="Generate",command=lambda: generateAndShow(app,cfg,getTuningList(tuningStrVar),root.get(),scale.get()))
    generateButton.configure(background= 'red',activebackground='#404040')
    

    

    return(window,rootLabel,root,rootDropDown,scaleLabel,scale,scaleDropDown,tuningLabel,tuningStrVar,tuningTextBox,generateButton)

def getPlotSize(fretLabels,stringLabels):
    width=(len(fretLabels)-2)/2.5
    height=(len(stringLabels))/2.5

    if width<4.5:
        width=4.5

    if height<1:
        height=1
    
    return(width,height)

def makeGraphText(app,tuning,root,scale):
    note= lambda interval : app.noteGivenInterval(scale,root,interval)
    scaleNotes=[note(interval) for interval in range(1,8)]

    #capitalizes text and converts lists of notes to strings
    rootText=root
    scaleNameText=scale
    scaleNoteText=" ".join(tone for tone in scaleNotes)
    tuningText=" ".join(tone for tone in tuning)

    intervalArrayTitle="{} {} ({}) with Tuning {} ".format(rootText,scaleNameText,scaleNoteText,tuningText)
    
    stringLabels=[tone.capitalize() for tone in tuning]
    fretLabels=["open"]+[i for i in range(1,app.numFrets)]

    return(intervalArrayTitle,stringLabels,fretLabels)

def showIntervalArray(cfg,intervalArray,title,stringLabels,fretLabels):
    if cfg.autoClosePlot:
        plt.close()

    fig=plt.figure(figsize=getPlotSize(fretLabels,stringLabels))
    ax=fig.add_subplot(111)
    fig.patch.set_facecolor('#404040')
    
    
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

def generateAndShow(app,cfg,tuning,root,scale):
    intervalArray=app.makeIntervalArray(tuning,scale,root)
    title,stringLabels,fretLabels=makeGraphText(app,tuning,root,scale)
    showIntervalArray(cfg,intervalArray,title,stringLabels,fretLabels)


if __name__ == "__main__":
    cfg=Config()
    app=App(cfg)

    tkRoot=tk.Tk()

    window,rootLabel,root,rootDropDown,scaleLabel,scale,scaleDropDown,tuningLabel,tuningStrVar,tuningTextBox,generateButton=generateTkinterObjs(app,cfg,tkRoot)

    #layout organization
    rootLabel.grid(row=0,column=0)
    rootDropDown.grid(row=0,column=1,sticky=tk.NSEW)

    scaleLabel.grid(row=1,column=0)
    scaleDropDown.grid(row=1,column=1,sticky=tk.NSEW)

    tuningLabel.grid(row=2,column=0,sticky=tk.NSEW)
    tuningTextBox.grid(row=2,column=1,sticky=tk.NSEW)

    generateButton.grid(row=3, columnspan=2,sticky=tk.NSEW)
    

    for row in range(0,4):
        for column in range(0,2):
            window.columnconfigure(column, weight=1)
            window.rowconfigure(row,weight=1)
    
    tkRoot.mainloop()