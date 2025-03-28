#references: https://learnopencv.com/contour-detection-using-opencv-python-c/

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
    detectSquareContour(contour=contours)
    
    
def detectSquareContour(contour):
    print("To do you nasty boo")
    # go through each contour found and use cv2.approxPolyDP(),
    # save the square ones to new list and save that image
    

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