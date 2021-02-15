import cv2
import numpy as np
from copy import deepcopy
#Color conversion
#cv2.cvtColor(obj,flag) flag type of conversion COLOR_*Conversion*
#BGR2GRAY,BGR2HSV
ix,iy=-1,-1
down=False
act=False
Sensi=50
#prints all events available

#funcion de llamada del mouse
def getColor(event,x,y,flags,param):
    global ix,iy,down
    down=False
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy=x,y
        down=True

def getMinMax(pixC,Sensi):
    down=pixC-Sensi
    up=pixC+Sensi
    if down<0:
        down=0
    if up>255:
        up=255
    return down,up
#Activar camara
cap=cv2.VideoCapture(0)
while(1):
    #Leemos la camara y tomamos el frame
    _,frame=cap.read()
    #Convertir BGR to HSV
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    if down:
        color=frame[iy,ix]
        
        #print(frame[ix,iy])
        
        act=True
        fc=np.uint8([[[color[0],color[1],color[2]]]])
        hsvc= cv2.cvtColor(fc,cv2.COLOR_BGR2HSV)
        lower_blue=deepcopy(hsvc)-20
        upper_blue=deepcopy(hsvc)+20
        

        #lower_blue[0][0][0]-=50
        #upper_blue[0][0][0]+=50
    
    cv2.imshow('Original',frame)
    cv2.setMouseCallback('Original',getColor)

    if act:
        #Separar imagen de canal usando  numpy
        #b=frame[:,:,0]
        #g=frame[:,:,1]
        #r=frame[:,:,2]
        #down,up=getMinMax(color[0],Sensi)
        #_,b = cv2.threshold(b,down,up,cv2.THRESH_TRUNC)
        #down,up=getMinMax(color[1],Sensi)
        #_,g = cv2.threshold(g,down,up,cv2.THRESH_TRUNC)
        #down,up=getMinMax(color[2],Sensi)
        #_,r = cv2.threshold(r,down,up,cv2.THRESH_TRUNC)

        #res = cv2.merge((b,g,r))

        framehsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        ##Creamos mascara
        mask=cv2.inRange(framehsv,lower_blue,upper_blue)
        #Bitwise-AND mask and original image
        res=cv2.bitwise_and(frame,frame,mask=mask)
        cv2.imshow('Filtrado',res)


    k=cv2.waitKey(5)&0xFF
    if k==27:
        cv2.destroyAllWindows()
        break

