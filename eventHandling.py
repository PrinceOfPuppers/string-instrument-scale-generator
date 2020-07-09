import numpy as np
import config as cfg
from helperFuncs import makeGraphText

#wrappers for app methods, used by event handler
def keyDownFifth(app,plotter):
    if cfg.debug:
        print("Key Change: Up a Fifth")
    app.keyChange(5)

    newTitle,stringLabels,fretLabels=makeGraphText(app)

    plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)

def keyUpFourth(app,plotter):
    if cfg.debug:
        print("Key Change; Down a Fourth")
    app.keyChange(4)

    newTitle,stringLabels,fretLabels=makeGraphText(app)

    plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)

def changeMode(app,plotter,newRootInterval):
    if newRootInterval!=app.nonIntervalNum:
        if cfg.debug:
            print("Setting {} as new root".format(int(newRootInterval)))
        app.changeMode(newRootInterval)

        newTitle,stringLabels,fretLabels=makeGraphText(app)

        plotter.plotIntervalArray(app,newTitle,stringLabels,fretLabels)
        plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)


class EventHandler:
    def __init__(self):
        pass
    
    def generateButton(self,app,plotter,tuning,root,scale):
        plotter.generateNew(app,self,tuning,root,scale)

    def enableInteractivity(self,app,plotter):
        self.scrolling=plotter.fig.canvas.mpl_connect('scroll_event',lambda event: self.onScroll(event,app,plotter))
        self.clicking=plotter.fig.canvas.mpl_connect('button_press_event', lambda event: self.onClick(event,app,plotter))
        self.keys=plotter.fig.canvas.mpl_connect('key_press_event', lambda event: self.onArrowKeys(event,app,plotter))

    def disableInteractivity(self,plotter):
        plotter.fig.canvas.mpl_disconnect(self.scrolling)
        plotter.fig.canvas.mpl_disconnect(self.clicking)
        plotter.fig.canvas.mpl_disconnect(self.keys)

    def onArrowKeys(self,event,app,plotter):
        if event.key=="down":
            keyDownFifth(app,plotter)
        elif event.key=="up":
            keyUpFourth(app,plotter)
        elif event.key=="right":
            changeMode(app,plotter,2)
        elif event.key=="left":
            changeMode(app,plotter,7)


    #callback fucntions 
    def onScroll(self,event,app,plotter):

        if event.button==cfg.down:
            keyDownFifth(app,plotter)
        elif event.button==cfg.up:
            keyUpFourth(app,plotter)

    def onClick(self,event,app,plotter):
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
                changeMode(app,plotter,interval)