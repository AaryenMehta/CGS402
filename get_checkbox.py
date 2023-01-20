import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

prtscr = pyautogui.screenshot()
prtscr.save("screenshot.png")

im = cv2.imread("screenshot.png")
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
mask = cv2.inRange(gray, 192.9, 193.1)
cnts , _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for contour in cnts:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(im, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        cx, cy = x + w/2, y + h/2
        im = cv2.circle(im, (int(cx),int(cy)), radius=0, color=(0, 0, 255), thickness=-1)
        #cv2.imshow("im", im)
        #cv2.waitKey()

def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            move_mouse(current_x:=move_x,current_y:=move_y)
    return current_x,current_y

fig = plt.figure(figsize=[13,13])
plt.axis('off')
x1, y1 = pyautogui.position()
x2, y2 = int(cx), int(cy)
for y in np.linspace(-200,200,25):
    points = []
    wind_mouse(x1,y1,x2,y2,move_mouse=lambda x,y: points.append([x,y]))
    points = np.asarray(points)
    plt.plot(*points.T)
#print(points)
plt.xlim(-50,550)
plt.ylim(-250,250)
#plt.show()
t = 1.0
#print(len(points))
dur = t / len(points)
pyautogui.PAUSE = dur
for i in range(len(points)) :
    pyautogui.moveTo(points[i][0], points[i][1])
pyautogui.click()