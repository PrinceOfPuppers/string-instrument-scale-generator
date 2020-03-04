import numpy as np
import matplotlib.pyplot as plt
from helperFuncs import makeGraphText,getPlotSize,makeLabel


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