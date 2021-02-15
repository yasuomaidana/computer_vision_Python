import cv2
import numpy as np
##Image trhesholding
from matplotlib import pyplot as plt

img = cv2.imread('LWA.jpg',0)

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()

########################
import cv2
import numpy as np
from copy import deepcopy
#Color conversion
#cv2.cvtColor(obj,flag) flag type of conversion COLOR_*Conversion*
#BGR2GRAY,BGR2HSV
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