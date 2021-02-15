import cv2
import numpy

pressed=False
exit=False
ix,iy=-1,-1
rx,ry=-1,-1
#funcion de llamada del mouse
def getPortion(event,x,y,flags,param):
    global ix,iy,pressed,exit,rx,ry
    #Getting points from mouse
     
    if event == cv2.EVENT_LBUTTONDOWN:
        if pressed==False:
            ix,iy=x,y
        pressed=True
        
            
    elif event == cv2.EVENT_LBUTTONUP:
        if pressed == True:
            rx,ry=x,y
            pressed=False
            exit=True
            cv2.destroyAllWindows()
            
#Cargando imagen
img = cv2.imread('LWA.jpg')
#Selecciona 1 pixel de la imagen
px=img[100,100]
#print(f'Imprime el vector de color en formato rbg : ',px)
#Seleccionando 1 solo valor 
blue=img[100,100,0]
#print(f'Imprime el color seleccionado rbg[0] : ',blue)
#Modifiacndo color
img[100,100]=[0,0,0]

#Otra forma de  acceder a los pixeles
img.item(100,100,0)
#print(f'Otra forma de acceder : ',img.item(10,10,1))
#Otra forma de modificar los pixeles
img.itemset((100,100,1),100)

##Accediendo a propiedades de imagenes
print('Filas,Columnas,Chanales ',img.shape) #returns rows, columns,  an channels (if it's a color)
print('Numero de pixeles',img.size)
print('Datatype de imagen',img.dtype)

#Obtener puntos de imagen
cv2.namedWindow('Prueba mouse')
#Bind a function to the window
cv2.setMouseCallback('Prueba mouse',getPortion)
#Copying a section of an image
while(1):
    cv2.imshow('Prueba mouse',img)
    
    cv2.waitKey(1)
    if exit:
        break
print(f'Starting point (',ix,',',iy,')', 'Ending point(',rx,',',ry,')')

#Copiando porcion seleccionada
cop=img[iy:ry,ix:rx]
cv2.imshow('Seccion copiada',cop)
#Pegandola en
img2=cv2.imread('LWA.jpg')
img2[iy-100:ry-100,ix-100:rx-100]=cop
cv2.rectangle(img2, (ix,iy), (rx,ry), (0, 255, 0), 3)
cv2.imshow('Prueba Pegando',img2)

cv2.waitKey()
cv2.destroyAllWindows()

#Eliminando porcion seleccionada
cop=img[iy:ry,ix:rx]#cop tipo numpy.array
cop[:,:,:]=0
#Pegandola en
img2=cv2.imread('LWA.jpg')
img2[iy:ry,ix:rx]=cop
cv2.imshow('Prueba Pegando',img2)
cv2.waitKey()
cv2.destroyAllWindows()


#Separar imagen de canal
b,g,r=cv2.split(img) #Tiene un costo de tiempo muy alto mejor filtrar por numpy
#Elimina un color
b[:,:]=0

#Pegar imagen de canal
img2 = cv2.merge((b,g,r))

cv2.imshow('Prueba filtrando color',img2)
cv2.waitKey()
cv2.destroyAllWindows()

#Separar imagen de canal usando  numpy
b=img[:,:,0]
g=img[:,:,1]
r=img[:,:,2]
#Pegar imagen de canal
img2 = cv2.merge((r,b,g))

cv2.imshow('Cambiando colores',img2)
cv2.waitKey()
cv2.destroyAllWindows()

##Making borders
from matplotlib import pyplot as plt

#cv2.copyMakeBorder(obj,top,bottom,left,right,cv2.BORDER_OPTION)
replicate = cv2.copyMakeBorder(img,100,100,100,100,cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img,100,80,100,100,cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img,100,100,80,100,cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img,100,100,100,80,cv2.BORDER_WRAP)
constant= cv2.copyMakeBorder(img,20,10,40,10,cv2.BORDER_CONSTANT,value=[255,0,0])

plt.subplot(231),plt.imshow(img,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
plt.show()