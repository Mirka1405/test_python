# this code is the worst i've ever seen, and the worst part is that I MADE THIS SPAGHETTI
import keyboard
import win32con,win32api
from time import sleep
from datetime import datetime   # for future logging features. ignore this line
from os.path import dirname,realpath
run = []
mode = "run" # run, always, repeat
repeat=[]
always=[]
repeatamount=0
def clickxy(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def addtorun(c):
    global run,mode,repeat,always
    if mode == "run":
        run+=[c]
        return
    if mode == "repeat":
        repeat+=[c]
        return
    always+=[c]
    return
    
def main():
    global run,mode,repeat,always
    with open(dirname(realpath(__file__))+"\\"+input("Macro file: ")+".macro") as f:
        # READ
        for line in f.readlines():
            if line.strip() == "":  continue # skip blank lines
            print(mode,end=" ")
            if mode == "script" and not "endscript" in line:
                ml+="\n"+line
            else:
                line = line.strip().split()
                if line[0] == "click":
                    addtorun("clickxy(int("+line[1]+"),int("+line[2]+"))")  # i know there is a much shorter way by using a dictionary. 
                elif line[0] == "clickpos":
                    addtorun("clickxy(*pos)")
                elif line[0] == "press":
                    addtorun("keyboard.send('"+line[1]+"')")
                elif line[0] == "hold":
                    addtorun("keyboard.press('"+line[1]+"')")
                elif line[0] == "release":
                    addtorun('keyboard.release("'+line[1]+'")')
                elif line[0] == "setpos":
                    addtorun("win32api.SetCursorPos((int("+line[1]+"), int("+line[2]+")))")
                elif line[0] == "move":
                    addtorun("win32api.SetCursorPos((pos[0]+int("+line[1]+"), pos[1]+int("+line[2]+")))")
                elif line[0] == "getpos":
                    addtorun("print(pos)")
                elif line[0] == "wait":
                    addtorun("sleep(float("+line[1]+"))")
                elif line[0] == "waitforkey":
                    addtorun(f"while not keyboard.is_pressed('{line[1]}'):    pass")  # for some reason i remembered about f-strings only when it was all done
                elif line[0] == "write":
                    t=""
                    for i in range(1,len(line)):
                        t+=line[i]+" "
                    addtorun(f"keyboard.write('{t}')")
                elif line[0] == "repeat":
                    repeatamount=int(line[1])
                    mode="repeat"
                elif line[0] == "always":
                    mode="always"
                elif line[0] == "end":
                    mode="run"
                    run+=repeat*repeatamount
                    repeat=[]
                elif line[0] == "run":          # TODO: find out about '_io.TextIOWrapper' object is not callable (pls help if some1 sees this)
                    t=""
                    for i in range(1,len(line)):
                        t+=line[i]+" "
                    addtorun(t)
                elif "=" in line[0]:
                    addtorun(line[0])
                elif line[0] == "endscript":    # TODO: this should set mode to "run" (done)
                    mode="run"
                    addtorun(ml)
                    ml=""
                elif line[0] == "script":
                    mode="script"
                    ml=""

        # RUN 
        print(run)
        print(always)
        for line in run:
            if not run or keyboard.is_pressed('f12'): break
            pos = win32api.GetCursorPos()
            try:
                exec(line)
            except Exception as error:
                print(error)
        while True and always and not keyboard.is_pressed('f12'):
            for line in always:
                pos = win32api.GetCursorPos()
                try:
                    exec(line)
                except Exception as e: # yes i know catching any exception is bad, but im lazy to implement each edge case
                    print(e)
        run = []
        mode = "run" # run, always, repeat
        repeat=[]
        always=[]
        repeatamount=0
while True:
    main()
