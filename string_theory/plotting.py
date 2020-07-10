import numpy as np
import matplotlib.pyplot as plt

import string_theory.config as cfg
from string_theory.helperFuncs import makeGraphText,getPlotSize,makeLabel
from string_theory.callbacks import onClick,onScroll,onArrowKeys

class Plotter:
    def __init__(self):
        pass
    
    #generates new plot window, used when generate button is hit in tkinter window
    def generateNew(self,app,tuning,root,scale):
        app.update(scale,root,tuning)
        app.makeIntervalArray()
        title,stringLabels,fretLabels=makeGraphText(app)

        plt.close()

        self.fig=plt.figure(figsize=getPlotSize(fretLabels,stringLabels),num="Click To Change Root, Scroll To Change Key")
        self.ax=self.fig.add_subplot(111)
        
        self.fig.patch.set_facecolor('#404040')

        self.enableInteractivity(app)

        plt.tight_layout()
        # note on linux plt.show haults the thread so plotAndDraw must be called before plt.show
        # event handling is multiplexed through tkinter and matplotlib interactivity
        self.plotAndDraw(app,title,stringLabels,fretLabels)
        plt.show()
    
    def enableInteractivity(self,app):
        self.fig.canvas.mpl_connect('scroll_event',lambda event: onScroll(event,app,self))
        self.fig.canvas.mpl_connect('button_press_event', lambda event: onClick(event,app,self))
        self.fig.canvas.mpl_connect('key_press_event', lambda event: onArrowKeys(event,app,self))

    #wrapper for updating plots
    def plotIntervalArray(self,app,title,stringLabels,fretLabels):
        self.ax.clear()
        self.ax.imshow(app.intervalArray,cmap=cfg.colorMap)
        self.ax.set_xticks(np.arange(len(fretLabels)))
        self.ax.set_yticks(np.arange(len(stringLabels)))
        
        for i in range(len(stringLabels)):  
            for j in range(len(fretLabels)):
                interval=int(app.intervalArray[i, j])
                label=makeLabel(app,interval)
                self.ax.text(j, i, label, ha="center", va="center", color="black")

        plt.title(title,color='white')
        
        self.ax.set_xticklabels(fretLabels,color='white')
        self.ax.set_yticklabels(stringLabels,color='white')
        
        plt.gca().invert_yaxis()

    
    def plotAndDraw(self,app,title,stringLabels,fretLabels):
        self.plotIntervalArray(app,title,stringLabels,fretLabels)
        plt.draw()
