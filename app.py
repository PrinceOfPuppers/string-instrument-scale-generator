import numpy as np
from helperFuncs import wrappedInterval

class App:
    def __init__(self,cfg):
        
        self.spacing=[1,1,0.5,1,1,1,0.5]
        self.diatonic={
            "Ionian": 0, 
            "Dorian": 1,
            "Phrygian": 2,
            "Lydian": 3,
            "Mixolydian": 4,
            "Aeolian": 5,
            "Locrian": 6
        }
        self.diatonicList=[
            "Ionian",
            "Dorian",
            "Phrygian",
            "Lydian",
            "Mixolydian",
            "Aeolian",
            "Locrian"
        ]

        self.numToNotes={0:"C" ,0.5: "C#" ,1:"D" ,1.5: "D#" ,2:"E" ,2.5: "F" ,3:"F#" ,3.5: "G" ,4:"G#" ,4.5: "A" ,5:"A#" ,5.5: "B"}
        self.notesToNum={"C":0 ,"C#":0.5 ,"D":1 ,"D#":1.5 ,"E":2 ,"F":2.5 ,"F#":3 ,"G":3.5 ,"G#":4 ,"A":4.5 ,"A#":5 ,"B":5.5}
        self.noteList=["C" ,"C#" ,"D" ,"D#" ,"E" ,"F" ,"F#" ,"G" ,"G#" ,"A" ,"A#" ,"B"]

        #interanally, open is considered a fret
        self.numFrets=cfg.numFrets+1
        self.nonIntervalNum=cfg.nonIntervalNum

    def numGivenInterval(self,scale,rootLetter,interval):
        #interval is 1,2,3,4,5,6,7 major/minor/diminished is determined by what scale your in
        #root is in terms of letter

        #allows for intervals greater than 8
        interval=wrappedInterval(interval)
        
        rootNum=self.notesToNum[rootLetter]
        scaleNum=self.diatonic[scale]

        intervalSpace=0

        for i in range(1,interval):
            spacingIndex=(i-1+scaleNum)%len(self.spacing)
            intervalSpace+=self.spacing[spacingIndex]
        
        intervalNum=(intervalSpace+rootNum)%6

        #returns number corrisponding to note in numToNotesDict
        return(intervalNum)

    def noteGivenInterval(self,scale,rootLetter,interval):
        #interval is 1,2,3,4,5,6,7 major/minor/diminished is determined by what scale your in
        #root is in terms of letter

        intervalNum=self.numGivenInterval(scale,rootLetter,interval)

        intervalNote=self.numToNotes[intervalNum]
        return(intervalNote)
    
    def intervalGivenNum(self,scale,rootLetter,noteNum):
        #returns self.nonIntervalNum if not a scale interval
        rootNum=self.notesToNum[rootLetter]
        scaleNum=self.diatonic[scale]
        
        checkingNum=rootNum
        for interval in range(1,9):
            if checkingNum==noteNum:
                break
            else:
                spacingIndex=(interval-1+scaleNum)%len(self.spacing)
                
                checkingNum+=self.spacing[spacingIndex]
                checkingNum%=6


        #if no match is found interval is set to self.nonIntervalNum
        if interval==8:
            interval=self.nonIntervalNum
        return(interval)

    def generateNoteNumArray(self,tuning):
        numStrings=len(tuning)
        noteNumArray=np.ndarray((numStrings,self.numFrets),dtype=float)

        for stringNum in range(0,numStrings):
            openNote=tuning[stringNum]
            openNoteNum=self.notesToNum[openNote]

            for fretNum in range(0,self.numFrets):
                noteNumArray[stringNum][fretNum]=(openNoteNum+0.5*fretNum)%6
        
        return(noteNumArray)

    def makeIntervalArray(self,tuning,scale,rootLetter):

        intervalArray=self.generateNoteNumArray(tuning)
        
        numStrings=len(tuning)
        for stringNum in range(0,numStrings):

            for fretNum in range(0,self.numFrets):
                noteNum=intervalArray[stringNum][fretNum]
                intervalArray[stringNum][fretNum]=self.intervalGivenNum(scale,rootLetter,noteNum)
        
        return(intervalArray)
