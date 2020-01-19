from app import App


if __name__ == "__main__":
    app=App()
    root="c"
    scale="ionain"

    note="c#"
    noteNum=app.notesToNum[note]
    print(app.intervalGivenNum(scale,root,noteNum))
    
    #intervals=range(1,100)
    #for interval in intervals:
    #    app.noteGivenInterval(scale,root,interval)