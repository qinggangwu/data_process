
import cv2

img = cv2.imread('E:/test.png',)
# img = cv2.imread('E:/1.jpg',)

img = cv2.resize(img,dsize=None,fx=0.5,fy=0.5)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ret, binary = cv2.threshold(img,0,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img,contours,-1,(0,0,255),3)
# cv2.imshow('test',img)
# cv2.waitKey(0)

pentagram = []
for c in contours:
    if len(c) >len(pentagram):
        pentagram = c
print(len(pentagram))

x1 = img.copy()

epsilon = 100
approx = cv2.approxPolyDP(pentagram,epsilon,True)
print(approx)
cv2.polylines(x1, [approx], True, (0, 0, 255), 2)
# cv2.putText(x1, "epsilon:50" , (160,180), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2 )

cv2.imshow('test',x1)
cv2.waitKey(0)



