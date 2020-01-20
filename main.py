from app import App
from config import Config
import matplotlib.pyplot as plt
import numpy as np

def makeGraphText(app,root,scale):
    note= lambda interval : app.noteGivenInterval(scale,root,interval)
    scaleNotes=[note(interval) for interval in range(1,8)]

    #capitalizes text and converts lists of notes to strings
    rootText=root.capitalize()
    scaleNameText=scale.capitalize()
    scaleNoteText=" ".join(tone.capitalize() for tone in scaleNotes)
    tuningText=" ".join(tone.capitalize() for tone in app.tuning)

    intervalArrayTitle="{} {} ({}) with Tuning {} ".format(rootText,scaleNameText,scaleNoteText,tuningText)
    
    stringLabels=[tone.capitalize() for tone in app.tuning]
    fretLabels=["open"]+[i for i in range(1,app.numFrets)]

    return(intervalArrayTitle,stringLabels,fretLabels)

def showIntervalArray(intervalArray,title,stringLabels,fretLabels):
    fig, ax = plt.subplots()
    ax.imshow(intervalArray,cmap='viridis_r')

    
    ax.set_xticks(np.arange(len(fretLabels)))
    ax.set_yticks(np.arange(len(stringLabels)))
    
    for i in range(len(stringLabels)):  
        for j in range(len(fretLabels)):
            if intervalArray[i, j]==app.nonIntervalNum:
                label=" "
            else:
                label=int(intervalArray[i, j])
            ax.text(j, i, label, ha="center", va="center", color="black")

    plt.title(title)
    ax.set_xticklabels(fretLabels)
    ax.set_yticklabels(stringLabels)
    fig.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    cfg=Config()
    app=App(cfg)
    root="b"
    scale="locrian"

    intervalArray=app.makeIntervalArray(scale,root)
    title,stringLabels,fretLabels=makeGraphText(app,root,scale)

    showIntervalArray(intervalArray,title,stringLabels,fretLabels)

