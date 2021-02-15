import cv2
import numpy as np
from copy import deepcopy
try:
  cap=cv2.VideoCapture(0)
except:
  a=cv2.destroyAllWindows()
#Activar camara
finally:
   cap=cv2.VideoCapture(0)

while(1):
    #Leemos la camara y tomamos el frame
    _,foto=cap.read()
        
    cv2.imshow('Filtrado',foto)
    k=cv2.waitKey(5)&0xFF
    if k==27:
        cap.release()
        cv2.destroyAllWindows()
        break
[fi,col,ca]=foto.shape
font = cv2.FONT_HERSHEY_SIMPLEX #Cargar tipo de letras
text="Yasuo Maidana A01328427"
a=cv2.getTextSize(text, font, 1, 3)
a=a[0][:]

cv2.putText(foto,text,(col-a[0],a[1]), font, 1,(0,255,0),3,cv2.LINE_AA)
while(1):
    cv2.imshow('Foto tomada',foto)
    k=cv2.waitKey(5)&0xFF
    if k==27:
        cv2.destroyAllWindows()
        break


meme1=cv2.imread('meme1.jpg')
output = cv2.resize(meme1,(col,fi), interpolation = cv2.INTER_AREA)
im_h = cv2.hconcat([foto, output])
cv2.imwrite(r'meme Horizontal.jpg', im_h)

meme2=cv2.imread('meme2.jpg')
output = cv2.resize(meme2,(col,fi), interpolation = cv2.INTER_AREA)
im_v = cv2.vconcat([output, foto])
cv2.imwrite(r'meme Vertical.jpg', im_v)


meme1=cv2.imread('meme Horizontal.jpg')
meme2=cv2.imread('meme Vertical.jpg')
while(1):
    cv2.imshow('Imagen concatenada horizontalmente',meme1)
    k=cv2.waitKey(5)&0xFF
    if k==27:
        cv2.destroyAllWindows()
        break

while(1):
    cv2.imshow('Imagen concatenada verticalemente',meme2)
    k=cv2.waitKey(5)&0xFF
    if k==27:
        cv2.destroyAllWindows()
        break

