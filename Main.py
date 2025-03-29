#references: https://learnopencv.com/contour-detection-using-opencv-python-c/
#            https://stackoverflow.com/questions/55169645/square-detection-in-image
#            https://medium.com/coinmonks/a-box-detection-algorithm-for-any-image-containing-boxes-756c15d7ed26 <-  the box extract in this works very good for Ex1 but fails for all others

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
        return
    h, w, ch = image1.shape
    # convert the image to grayscale format
    img_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    #invert image
    img_gray = 255-img_gray  # Invert the image
    # apply binary thresholding
    ret, thresh = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    # Defining a kernel length
    kernel_length = 1
 
    #A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(thresh, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    img_temp2 = cv2.erode(thresh, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite(filename.split(".")[0]+"_negative_box.png",img_final_bin)
    
    ## detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    #contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    ## draw contours on the original image
    #contourImage = np.zeros_like(image1)
    #cv2.drawContours(image=contourImage, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    ## save the result
    #cv2.imwrite(filename+'contours.jpg', contourImage)
    #filesGenerated.append(filename+'contours.jpg')
    ##get the specific contours that are square
    #detectSquareContour(contour=contours,Image = image1,name = filename)
    
    
def detectSquareContour(contour,Image,name):
    emptyImage = np.zeros_like(Image)
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
    cv2.drawContours(image=Image, contours=squares, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imwrite(name+'origin+squares.jpg', Image)
    filesGenerated.append(name+'origin+squares.jpg')

def cleanUp():
    for file in filesGenerated:
        if os.path.isfile(file):
            os.remove(file)
            
    
#Main program
parseContours('Assets/crossword_Ex1.webp')
parseContours('Assets/crossword_Ex2.png')
parseContours('Assets/crossword_Colorful.jpg')