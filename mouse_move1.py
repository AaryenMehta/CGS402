import pyautogui as pag
import scipy.interpolate
import pytweening
import pynput
import time
from time import sleep

pag.MINIMUM_DURATION = 0.01
pag.MINIMUM_SLEEP = 0.01

def moveThrough(points, duration=0.1, neonate=pytweening.easeInOutQuad):
    n = len(points)
    interpkind = "linear"
    if n == 0: raise Exception("No points to move through")
    elif n == 1: moveThrough([pag.position(), points[0]], duration); return
    elif n == 2: interpkind = "linear"
    elif n == 3: interpkind = "quadratic"
    else: interpkind = "cubic"

    ts = [i/(n-1) for i in range(n)]
    interp = scipy.interpolate.interp1d(ts, points, axis=0, kind=interpkind, assume_sorted=True)
    steps = duration / pag.MINIMUM_SLEEP
    for i in range(int(steps)):
        x, y = interp(neonate(i / (steps-1)))
        x, y = (int(round(x)), int(round(y)))
        pag.platformModule._moveTo(x, y)
        sleep(pag.MINIMUM_SLEEP)

class ClickRecorder:
    def __init__(self, num=1, button=pynput.mouse.Button.left):
        self.num = num
        self.count = 0
        self.recorded = []
        self.listener = pynput.mouse.Listener(on_click=self.on_click)
        self.listener.start()
    def on_click(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left and pressed:
            self.recorded.append((x,y))
            self.count += 1
            if self.count >= self.num:
                return False # stop

    def get(self):
        self.listener.join()
        return self.recorded


if __name__ == "__main__":
    #cr = ClickRecorder(num=10)
    #points = cr.get()

    #sleep(0.05)
    #moveThrough(points, duration=4)

    #pag.moveTo(1920//2, 1080//2)
    #pag.mouseDown(button=pag.RIGHT)
    t0 = time.time()
    while (time.time() - t0) < 2:
        startx, starty = pag.position()
        x, y = (startx + 1, starty + 1)
        pag.platformModule._moveTo(x, y)
        sleep(pag.MINIMUM_SLEEP)
    #pag.mouseUp(button=pag.RIGHT)