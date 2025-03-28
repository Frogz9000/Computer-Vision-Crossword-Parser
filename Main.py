#references: https://learnopencv.com/contour-detection-using-opencv-python-c/
#            https://stackoverflow.com/questions/55169645/square-detection-in-image

import cv2
import os
import numpy as np
#Define constants/Vars
filesGenerated = []

# Function Definitions
def parseContours(filename):
    # read in test image
    image1 = cv2.imread(filename)
    if image1 is None:
        print("Error: File {filename} was not able to be read")
    # convert the image to grayscale format
    img_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    # draw contours on the original image
    contourImage = np.zeros_like(image1)
    cv2.drawContours(image=contourImage, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    # save the result
    cv2.imwrite(filename+'contours.jpg', contourImage)
    filesGenerated.append(filename+'contours.jpg')
    #get the specific contours that are square
    detectSquareContour(contour=contours,emptyImage = np.zeros_like(image1),name = filename)
    
    
def detectSquareContour(contour,emptyImage,name):
    squares = []
    for cont in contour:
        x, y, w, h = cv2.boundingRect(cont)
        # Calculate aspect ratio
        aspect_ratio = float(w) / h
        cnt_len = cv2.arcLength(cont, True)
        cnt = cv2.approxPolyDP(cont, 0.02*cnt_len, True)
        if len(cnt) == 4 and cv2.contourArea(cnt) > 100 and abs(aspect_ratio-1) < 0.05:
            squares.append(cont)
    cv2.drawContours(image=emptyImage, contours=squares, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite(name+'squares.jpg', emptyImage)
    filesGenerated.append(name+'squares.jpg')
        
    

def cleanUp():
    for file in filesGenerated:
        if os.path.isfile(file):
            os.remove(file)
            
    
#Main program
parseContours('Assets/crossword_Ex1.webp')
parseContours('Assets/crossword_Ex2.png')
parseContours('Assets/crossword_Colorful.jpg')
input()
cleanUp()