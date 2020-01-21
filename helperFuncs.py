def getPlotSize(fretLabels,stringLabels):
    width=(len(fretLabels)-2)/2.5
    height=(len(stringLabels))/2.5

    if width<4.5:
        width=4.5

    if height<1:
        height=1
    
    return(width,height)

def getTuningList(tuningStrVar):
    tuningString=tuningStrVar.get().strip()
    return [note.capitalize() for note in tuningString.split(" ")]
    
def wrappedInterval(interval):
    interval-=1
    interval%=7
    interval+=1
    return(interval)