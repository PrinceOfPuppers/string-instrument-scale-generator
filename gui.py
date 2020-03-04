import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

from helperFuncs import getTuningList,getPlotSize,makeLabel,makeGraphText

#wrappers for app methods, used by event handler
def keyDownFifth(cfg,app,plotter):
    if cfg.debug:
        print("Key Change: Up a Fifth")
    app.keyChange(5)

    newTitle,stringLabels,fretLabels=makeGraphText(app)

    plotter.plotAndShow(app,cfg,newTitle,stringLabels,fretLabels)

def keyUpFourth(cfg,app,plotter):
    if cfg.debug:
        print("Key Change; Down a Fourth")
    app.keyChange(4)

    newTitle,stringLabels,fretLabels=makeGraphText(app)

    plotter.plotAndShow(app,cfg,newTitle,stringLabels,fretLabels)

def changeMode(cfg,app,plotter,newRootInterval):
    if newRootInterval!=app.nonIntervalNum:
        if cfg.debug:
            print("Setting {} as new root".format(int(newRootInterval)))
        app.changeMode(newRootInterval)

        newTitle,stringLabels,fretLabels=makeGraphText(app)

        plotter.plotIntervalArray(app,cfg,newTitle,stringLabels,fretLabels)
        plotter.plotAndShow(app,cfg,newTitle,stringLabels,fretLabels)




class Plotter:
    def __init__(self):
        pass
    #generates new plot window, used when generate button is hit in tkinter window
    def generateNew(self,app,cfg,eventHand,tuning,root,scale):
        app.update(scale,root,tuning)
        app.makeIntervalArray()
        title,stringLabels,fretLabels=makeGraphText(app)

        
        plt.close()

        self.fig=plt.figure(figsize=getPlotSize(fretLabels,stringLabels),num="Click To Change Root, Scroll To Change Key")
        self.ax=self.fig.add_subplot(111)
        
        self.fig.patch.set_facecolor('#404040')

        eventHand.enableInteractivity(cfg,app,self)

        plt.tight_layout()
        return(title,stringLabels,fretLabels)
    

    #wrapper for updating plots
    def plotIntervalArray(self,app,cfg,title,stringLabels,fretLabels):
        self.ax.clear()
        
        self.ax.imshow(app.intervalArray,cmap=cfg.colorMap)
        self.ax.set_xticks(np.arange(len(fretLabels)))
        self.ax.set_yticks(np.arange(len(stringLabels)))
        
        for i in range(len(stringLabels)):  
            for j in range(len(fretLabels)):
                interval=int(app.intervalArray[i, j])
                label=makeLabel(app,cfg,interval)
                self.ax.text(j, i, label, ha="center", va="center", color="black")

        plt.title(title,color='white')
        
        self.ax.set_xticklabels(fretLabels,color='white')
        self.ax.set_yticklabels(stringLabels,color='white')
        
        plt.gca().invert_yaxis()

    
    def plotAndShow(self,app,cfg,title,stringLabels,fretLabels):
        self.plotIntervalArray(app,cfg,title,stringLabels,fretLabels)
        plt.show()





class EventHandler:
    def __init__(self):
        pass
    
    def generateButton(self,app,cfg,plotter,tuning,root,scale):
        title,stringLabels,fretLabels=plotter.generateNew(app,cfg,self,tuning,root,scale)
        plotter.plotAndShow(app,cfg,title,stringLabels,fretLabels)
    
    def enableInteractivity(self,cfg,app,plotter):
        self.scrolling=plotter.fig.canvas.mpl_connect('scroll_event',lambda event: self.onScroll(event,cfg,app,plotter))
        self.clicking=plotter.fig.canvas.mpl_connect('button_press_event', lambda event: self.onClick(event,cfg,app,plotter))
        self.keys=plotter.fig.canvas.mpl_connect('key_press_event', lambda event: self.onArrowKeys(event,cfg,app,plotter))

    def disableInteractivity(self,plotter):
        plotter.fig.canvas.mpl_disconnect(self.scrolling)
        plotter.fig.canvas.mpl_disconnect(self.clicking)
        plotter.fig.canvas.mpl_disconnect(self.keys)

    def onArrowKeys(self,event,cfg,app,plotter):
        if event.key=="down":
            keyDownFifth(cfg,app,plotter)
        elif event.key=="up":
            keyUpFourth(cfg,app,plotter)
        elif event.key=="right":
            changeMode(cfg,app,plotter,2)
        elif event.key=="left":
            changeMode(cfg,app,plotter,7)


    #callback fucntions 
    def onScroll(self,event,cfg,app,plotter):
        if event.button=="up":
            keyDownFifth(cfg,app,plotter)
        elif event.button=="down":
            keyUpFourth(cfg,app,plotter)

    def onClick(self,event,cfg,app,plotter):
        if cfg.debug:
            print("clicked on",event.xdata,event.ydata)

        if event.button == cfg.mouseButton:
            #input may be none type
            if type(event.ydata)!=np.float64 or type(event.xdata)!=np.float64:
                if cfg.debug:
                    print("clicked offscreen")
            else:
                #coordinates are flipped
                boxClicked=(int(event.ydata+0.5),int(event.xdata+0.5))
                interval=app.intervalArray[boxClicked[0]][boxClicked[1]]
                changeMode(cfg,app,plotter,interval)


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