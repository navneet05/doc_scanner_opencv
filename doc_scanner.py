# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:38:07 2020

@author: Navneet Yadav
"""
import cv2
import numpy as np
#%% image print function
def imagepr(img):
    cv2.imshow('image', img) 
    k = cv2.waitKey(0) & 0xFF
  
    # # wait for 's' key to save and exit
    if k == ord('s'):  
        cv2.imwrite('copy.png',img) 
        cv2.destroyAllWindows()  
    # any key to exit 
    else :
        cv2.destroyAllWindows()
#%% resize function
def resize(img,w):
    h_org, w_org = img.shape[:2]
    # Calculating the ratio 
    ratio = w / w_org
    # Creating a tuple containing width and height 
    dim = (w, int(h_org * ratio)) 
    # Resizing the image 
    return cv2.resize(img, dim)
#%%
def canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged
# %% taking pic
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("NewPicture.jpg",frame)
            break
    else:
        break
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
#%%image preprocessing
img = cv2.imread("rgpv_smart_card.jpg")
img=resize(img, 400)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(gray, 75, 200)

#morphological dilation
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(edges,kernel,iterations = 1)
imagepr(edges)
#%% finding contours 
contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		pCnt = approx
		break
#%%
#cv2.drawContours(img, [pCnt], -1, (0, 255, 0), 2)
#imagepr(img)
#%%
x, y, width, height = cv2.boundingRect(pCnt)
roi = img[y:y+height, x:x+width]
cv2.imwrite("result_doc.png", roi)