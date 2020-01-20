from app import App
from config import Config
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    cfg=Config()
    app=App(cfg)
    root="c"
    scale="aeolian"

    #note="b"
    #noteNum=app.notesToNum[note]
    #print(app.intervalGivenNum(scale,root,noteNum))
    
    #intervals=range(1,100)
    #for interval in intervals:
    #    app.noteGivenInterval(scale,root,interval)

    stringLabels=app.tuning.copy()
    print(stringLabels)

    fretLabels=[i for i in range(0,app.numFrets)]
    
    intervalArray=app.makeIntervalArray(scale,root)
    print(intervalArray)
    fig, ax = plt.subplots()
    im = ax.imshow(intervalArray,cmap='viridis_r')

    
    ax.set_xticks(np.arange(len(fretLabels)))
    ax.set_yticks(np.arange(len(stringLabels)))
    
    for i in range(len(stringLabels)):  
        for j in range(len(fretLabels)):
            if intervalArray[i, j]==app.nonIntervalNum:
                label=" "
            else:
                label=int(intervalArray[i, j])
            text = ax.text(j, i, label,
                           ha="center", va="center", color="w")

    ax.set_xticklabels(fretLabels)
    ax.set_yticklabels(stringLabels)
    fig.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()
