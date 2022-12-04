import cv2

imagen = cv2.imread('../train_data/CQ500-CT-0-2-9(1).png')

img1 = imagen.copy()
cv2.rectangle(img1, (181, 203), (240, 260), (0, 255, 0), 2)

cv2.imshow('Imagen', img1)
cv2.waitKey(0)