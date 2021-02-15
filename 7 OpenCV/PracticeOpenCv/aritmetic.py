import cv2
import numpy as np

img1 = cv2.imread('logo1.png')
img2 = cv2.imread('logo2.png')


#Adition
x = np.uint8([250])
y = np.uint8([10])
print(cv2.add(x,y)) #Saturated operation
print(x+y)#Modulo operation if exceed returns reminder
x = np.uint8([230])

print(x+y)#Modulo operation

#Image blending ("superposition")
dst = cv2.addWeighted(img1,0.5,img2,0.5,0)

cv2.imshow('Superpuestas',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

#######################################################################################################

#Bitwise operations
lwa=cv2.imread('LWA.jpg')
rows,cols,channels = img1.shape #obtener filas y columnas del logo
roi = lwa[0:rows, 0:cols ]


# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html
#cv2.cvtColor(obj,Color conversion ode)

cv2.imshow('Mascara gris',img2gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
#cv2.threshold(src, thresholdValue, maxVal, thresholdingTechnique)
#src debe estar en grayscale
#https://java2blog.com/cv2-threshold-python/
mask_inv = cv2.bitwise_not(mask)

cv2.imshow('Mascara gris',img2gray)
cv2.imshow('Mascara antes de bitwise',mask)
cv2.imshow('Mascara invertida',mask_inv)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
cv2.imshow('Poner en negro el area dentro del logo',img1_bg)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img1,img1,mask = mask)
#r=img1(i)^img1(i) if mask(i)!=0
cv2.imshow('Region tomada',img2_fg)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
cv2.imshow('Combina roi y logo solo',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

lwa[0:rows, 0:cols ] = dst

cv2.imshow('Resultado',lwa)
cv2.waitKey(0)
cv2.destroyAllWindows()
