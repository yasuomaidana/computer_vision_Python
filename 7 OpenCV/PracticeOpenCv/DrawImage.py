import numpy as np
import cv2

def run():
    # Crea una imagen negra
    img = np.zeros((512,512,3), np.uint8)

    # Dibuja una linea diagonal azul de un grosor de 5px
    img = cv2.line(img,(0,0),(511,511),(255,0,0),5)
    # Dibuja una linea diagonal azul de un grosor de 5px
    img = cv2.line(img,(0,511),(511,0),(255,100,50),10)# cv2.line(ob,(start),(end),(color),(pxwidth))

    #Dibuja un rectangulo
    img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
    #cv2.rectangle(ob,(startCorner),(endCorner),(color),pxwidth)

    #Dibujar circulo
    img = cv2.circle(img,(447,63), 63, (0,0,255), -1)
    #img = cv2.circle(Obj,(xCenter,yCenter), Radius, (Color), -1)

    #Dibujar elipse
    img = cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)
    #img = cv2.ellipse(img,(xCenter,yCenter),(maxAxisLength,minAxisLength),AngleofRot,StartAngle,FinishAngle,?,?)
    
    #Dibujando poligono
    pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32) #Coordenadas del poligono
    pts = pts.reshape((-1,1,2)) #Arreglo en de 
    img = cv2.polylines(img,[pts],True,(0,255,255))
    #cv2.polylines(object,[pts],True?,color)

    #Dibujando letras
    font = cv2.FONT_HERSHEY_SIMPLEX #Cargar tipo de letras
    cv2.putText(img,'Yasuo OpenCV',(10,500), font, 1,(255,255,255),2,cv2.LINE_AA)
    #cv2.putText(Obj,Text,(x,y), font, size,(color),thickness,optional:lineType,bottomLEftOrigin)
    cv2.imshow('Imagen Generada',img)
    cv2.waitKey()
    cv2.destroyAllWindows()