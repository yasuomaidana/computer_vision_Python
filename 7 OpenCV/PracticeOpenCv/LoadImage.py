
import numpy as np
import cv2

#Cargar imagen de archivo en escala de grises
img = cv2.imread('LWA.jpg')
## Configura el tamano de la pantalla
cv2.namedWindow('Little Witch Academia',cv2.WINDOW_NORMAL)
## shows the image in a windows ('name',var) name=name of the window
cv2.imshow('Little Witch Academia',img)
cv2.waitKey(0)
#Cargar imagen de archivo en escala de grises
img = cv2.imread('LWA.jpg',0)
## Configura el tamano de la pantalla
cv2.namedWindow('Little Witch Academia',cv2.WINDOW_NORMAL)
## shows the image in a windows ('name',var) name=name of the window
cv2.imshow('Little Witch Academia',img)

#Lee una tecla
k=cv2.waitKey(0)&0xFF
if k==27:
    cv2.destroyAllWindows()
elif k==ord('s'):
    cv2.imwrite('LWAG.png',img)
    cv2.destroyAllWindows()

#Using MatplotLib
from matplotlib import pyplot as plt
plt.imshow(img,cmap='gray',interpolation='bicubic') #interpolatio bicubic
plt.xticks([]),plt.yticks([]) #Hides X,Y values
plt.show()
cv2.waitKey(0)&0xFF
cv2.destroyAllWindows()
plt.close('all')