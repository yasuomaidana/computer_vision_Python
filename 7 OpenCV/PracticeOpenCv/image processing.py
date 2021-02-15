#Changing colorspaces
import cv2
import numpy as np
#flags= [i for i in dir(cv2) if i.startswith('COLOR_')]
#print(flags)

#Color conversion
#cv2.cvtColor(obj,flag) flag type of conversion COLOR_*Conversion*
#BGR2GRAY,BGR2HSV
cap=cv2.VideoCapture(0)
while(1):
    #Leemos la camara y tomamos el frame
    _,frame=cap.read()
    #Convertir BGR to HSV
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #Rage of blue on HSV
    lower_blue=np.array([110,50,50])
    upper_blue=np.array([130,255,255])
    
    #Creamos mascara
    mask=cv2.inRange(hsv,lower_blue,upper_blue)

    #Bitwise-AND mask and original image
    res=cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow('Original',frame)
    cv2.imshow('Mascara',mask)
    cv2.imshow('Resultado',res)
    k=cv2.waitKey(5)&0xFF
    if k==27:
        cv2.destroyAllWindows()
        break
#convert bgr color to hsv
green=np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)

################################################################
#Image transformation
cap=cv2.VideoCapture(0)
img=cv2.imread('LWA.jpg',0)
rows,cols=img.shape
##Moving a picture
#Matris transformation
M=np.float32([[1,0,300],[0,1,300]])
dst = cv2.warpAffine(img,M,(cols,rows))
cv2.imshow('Imagen movida blanco y negro',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

img=cv2.imread('LWA.jpg')
blue=img[:,:,0]
green=img[:,:,1]
red=img[:,:,2]

blue = cv2.warpAffine(blue,M,(cols,rows))
red = cv2.warpAffine(red,M,(cols,rows))
green = cv2.warpAffine(green,M,(cols,rows))
dst = cv2.merge((blue,green,red))
cv2.imshow('Imagen movida',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

##Scaling a picture
logo=cv2.imread('logo1.png')

res=cv2.resize(logo,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
#cv2.resize(obj,None,fx=Xfactor,fy=Yfactor,interpolation=cv2."Intepolation method")
cv2.imshow('Imagen escalada proceso 1',res)
cv2.waitKey(0)
cv2.destroyAllWindows()

height,width=img.shape[:2]
res=cv2.resize(logo,(2*width,2*height),interpolation=cv2.INTER_CUBIC)
#cv2.resize(obj,(xF*width,yF*height),interpolation=cv2."Intepolation method")
cv2.imshow('Imagen escalada proceso 2',res)
cv2.waitKey(0)
cv2.destroyAllWindows()

##Rotation
logo=cv2.imread('logo1.png',0)
rows,cols=logo.shape
M=cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
dst=cv2.warpAffine(logo,M,(cols,rows))#La imagen que recibe debe de estar en GRAY
cv2.imshow('Imagen rotada',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

##Affine transformation
#transform maintaining some lines of reference in paralel
pts1=np.float32([[50,50],[200,50],[50,200]])
pts2=np.float32([[10,100],[200,50],[100,250]])

M=cv2.getAffineTransform(pts1,pts2)#Regresa matriz de transformacion 2x3
dst=cv2.warpAffine(logo,M,(cols,rows))#La imagen que recibe debe de estar en GRAY
cv2.imshow('Imagen rotada con M generada con getAffineTransform',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

#transform to generate perspective
pts1=np.float32([[56,65],[368,52],[29,387],[389,390]])
pts2=np.float32([[0,0],[300,0],[0,300],[300,300]])
M=cv2.getPerspectiveTransform(pts1,pts2) #Generates transformation matrix of 3x3

dst=cv2.warpPerspective(logo,M,(300,300))#La imagen que recibe debe de estar en GRAY

cv2.imshow('Imagen con perspectiva con getPerspectiveTransform',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

