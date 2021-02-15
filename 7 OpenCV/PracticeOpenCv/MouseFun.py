import cv2
import numpy as np

#event=[i for i in dir(cv2) if 'EVENT' in i]
#prints all events available
#print(event)

drawing=False
mode=True
ix,iy=-1,-1

#funcion de llamada del mouse
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy=x,y
    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)
#Create black image
img = np.zeros((512,512,3),np.uint8)
#Create a window
cv2.namedWindow('Imagen negra')
#Bind a function to the window
cv2.setMouseCallback('Imagen negra',draw_circle)

while(1):
    cv2.imshow('Imagen negra',img)
    k=cv2.waitKey(1)
    if k == ord('m'):
        mode = not mode
    elif k== ord('q'):
        break
cv2.destroyAllWindows()

