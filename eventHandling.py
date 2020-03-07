import numpy as np
from helperFuncs import makeGraphText

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

        if event.button==cfg.down:
            keyDownFifth(cfg,app,plotter)
        elif event.button==cfg.up:
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