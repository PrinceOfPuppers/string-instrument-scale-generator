import string_theory.config as cfg

def getPlotSize(fretLabels,stringLabels):
    width=(len(fretLabels))/2.5 +1
    height=(len(stringLabels))/2.5 +1

    if width<4.5:
        width=4.5

    if height<1.5:
        height=1.5
    
    return(width,height)

def getTuningList(tuningStrVar):
    tuningString=tuningStrVar.get().strip()
    return [note.capitalize() for note in tuningString.split(" ")]
    
def wrappedInterval(interval):
    interval-=1
    interval%=7
    interval+=1
    return(interval)

#returns labels for the interavals 
def makeLabel(app,interval):
    if interval==app.nonIntervalNum:
        label=" "
    elif cfg.displayMajMin:
        label=app.diatonicMajMin[app.scale][interval-1]
    else:
        label=interval
    
    return(label)

def makeGraphText(app):
    note= lambda interval : app.noteGivenInterval(app.scale,app.root,interval)
    scaleNotes=[note(interval) for interval in range(1,8)]

    #capitalizes text and converts lists of notes to strings
    rootText=app.root
    scaleNameText=app.scale
    scaleNoteText=" ".join(tone for tone in scaleNotes)
    tuningText=" ".join(tone for tone in app.tuning)

    intervalArrayTitle=f"{rootText} {scaleNameText} ({scaleNoteText}) with Tuning {tuningText} "
    
    stringLabels=[tone.capitalize() for tone in app.tuning]
    fretLabels=["open"]+[i for i in range(1,app.numFrets)]

    return(intervalArrayTitle,stringLabels,fretLabels)