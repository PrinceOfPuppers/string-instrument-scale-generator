class Config:
    def __init__(self):
        self.defaultTuning="E A D G B E"
        self.tkinterWinSize="400x150"
        self.tkinterFont="Arial 13"
        self.debug=True
        #must be atleast 1
        self.numFrets=24
        self.nonIntervalNum=9
        
        #self.colorMap="viridis_r"
        self.colorMap="inferno_r"

        self.autoClosePlot=False