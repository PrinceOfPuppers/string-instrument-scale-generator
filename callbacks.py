import numpy as np
import config as cfg
from helperFuncs import makeGraphText

#callbacks
def onGenerateButton(app,plotter,gui,tuning,root,scale):
    gui.root.withdraw()
    plotter.generateNew(app,tuning,root,scale)
    gui.root.deiconify()


def onArrowKeys(event,app,plotter):
    if event.key=="down":
        app.keyDownFifth()
    elif event.key=="up":
        app.keyUpForth()
    elif event.key=="right":
        app.changeMode(2)
    elif event.key=="left":
        app.changeMode(7)
    else:
        return
    newTitle,stringLabels,fretLabels=makeGraphText(app)
    plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)


#callback fucntions 
def onScroll(event,app,plotter):
    if event.button=="down":
        app.keyDownFifth()
    elif event.button=="up":
        app.keyUpForth()
    else:
        return
    newTitle,stringLabels,fretLabels=makeGraphText(app)
    plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)

def onClick(event,app,plotter):
    if event.button == cfg.mouseButton:

        clickedOnScreen=type(event.ydata)==np.float64 and type(event.xdata)==np.float64
        if clickedOnScreen:
            #coordinates are flipped
            boxClicked=(int(event.ydata+0.5),int(event.xdata+0.5))
            interval=app.intervalArray[boxClicked[0]][boxClicked[1]]

            #ensures interval is a scaletone and isnt root
            if interval!=app.nonIntervalNum and interval!=1.0:
                app.changeMode(interval)
                newTitle,stringLabels,fretLabels=makeGraphText(app)
                plotter.plotAndDraw(app,newTitle,stringLabels,fretLabels)


