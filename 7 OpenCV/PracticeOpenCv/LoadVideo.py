import numpy as np
import cv2

def run():
    cap = cv2.VideoCapture(0)#cv2.VideoCapture(num) num=numero de camara
    #en algunas ocasiones cap no se inicializa para revisar esto se puede utilizar
    #cap.isOpened() o en su defecto cap.open() para iniciarla
    while(True):
        #Capturar cuadro por cuadro
        ret,frame=cap.read()#ret boolean que dice si se obtuvo bien o no la imagen

        #Operaciones sore los cuadros
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #cap.get(num) num=[0-18] cada numero es una propiedad del video

        #Mostrar el cuadro tomado
        cv2.imshow('Video Gris',gray)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
    #Desactiva cap
    cap.release()
    cv2.destroyAllWindows()
    
    #Iniciar cap
    cap.open('lol.mp4')
    #Carga video de archivo
    cap = cv2.VideoCapture('lol.mp4')

    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('One Pucnh Man',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    cap.open('Guardar.mp4')
    #Carga video de archivo
    cap = cv2.VideoCapture('Guardar.mp4')

    # Se define el codec a usar 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #Se crea objeto VideoWriter object
    out = cv2.VideoWriter('Video Salida.avi',fourcc, 20.0, (640,480))
    while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                #Cambia los cuadros
                frame = cv2.flip(frame,0)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()