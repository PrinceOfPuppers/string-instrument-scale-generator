class Config:
    def __init__(self):
        self.defaultTuning="E A D G B E"
        self.tkinterWinSize="400x150"
        self.tkinterFont="Arial 13"
        self.debug=False
        #must be atleast 1
        self.numFrets=24
        self.nonIntervalNum=9
        
        #self.colorMap="viridis_r"
        self.colorMap="inferno_r"
        self.atlasColorMap="inferno"

        #button for interacting 
        self.mouseButton=1

        self.displayMajMin=True

        
        self.invertScrolling=False

        self.up="up"
        self.down="down"
        if self.invertScrolling:
            self.up="down"
            self.down="up"


