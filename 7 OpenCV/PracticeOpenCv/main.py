import numpy as np
import cv2
print(f'cargar imagen(1) \nvideo(2)\npaint(3)\nbasic options(4)\naritmetic(5)\n')
print(f'exit any number\n')
while (1):
    i= int(input('Ingrese opcion : '))
    if  i==1:
        import LoadImage
        LoadImage
    elif i==2:
        import LoadVideo
        LoadVideo.run()
    elif i==3:
        import MouseFun
    elif i==4:
        import BasicOptions
    elif i==5:
        import aritmetic
    else:
        break
    