'''
Ta se lay vat the dau tien trong danh sach cac vat the lam chuan (co kich thuoc 1cm x 1cm ).
Cac vat the sau se lay ty le nhan len ta se co kich thuoc cua no
'''
import os,sys,cv2
import numpy as np

DEBUG = True

'''
Formating text for showing code on window
'''
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (0, 0) # initialize
# fontScale
fontScale = 0.4
# Line thickness of 2 px
thickness = 1
# text
txt_code = ""
'''
'''
obj_width = 0
obj_height = 0
kernelSize = np.ones((20,20),np.uint8)

webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    sys.exit("Cannot open webcam")

while True:
    # capture frame-by-frame
    ret, frame = webcam.read() # function read() will return a tuple. Frame is like a image

    # if frame is read correctly, ret == True
    if not ret:
        sys.exit("Cannot receive frame. Exiting ...")
        break

    gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # make binary
    ret, thresh = cv2.threshold(gray_img,128,255,cv2.THRESH_BINARY_INV)
    
    # dilate
    dilation = cv2.dilate(thresh,kernelSize)
    # erode
    erosion = cv2.erode(dilation,kernelSize)
    # find contours
    cnts, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # make a list of contour for sorting
    list_cnts = []
    for cnt in cnts:
        list_cnts.append(cv2.boundingRect(cnt))

    sorted_list_cnts = sorted(list_cnts)
    if DEBUG :print(sorted_list_cnts)
    for i in range(len(sorted_list_cnts)):
        # get data of each contour
        x=sorted_list_cnts[i][0]
        y=sorted_list_cnts[i][1]
        w=sorted_list_cnts[i][2]
        h=sorted_list_cnts[i][3]
        # draw contour
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        # draw text
        org = (x, y)
        if i==0 :
            txt_code = str(i)+": "+ str(sorted_list_cnts[i][2]) +" cm + "  + str(sorted_list_cnts[i][2]) + " cm"
        else:
            obj_width = int(round((sorted_list_cnts[i][2] / sorted_list_cnts[0][2]),3)*3)
            obj_height = int(round((sorted_list_cnts[i][3] / sorted_list_cnts[0][2]),3)*3)
            txt_code = str(obj_width) +" cm + "  + str(obj_height) + " cm"

        frame = cv2.putText(frame, txt_code, org, font, fontScale, (255,0,0), thickness, cv2.LINE_AA)

    frame = cv2.putText(frame,"Press: q to exit program - w to capture the result",(15,15),font,fontScale,(255,0,0),thickness,cv2.LINE_AA)
    frame = cv2.putText(frame,"Result: " + str(obj_width) +"cm x "+ str(obj_height) + "cm",(15,30),font,fontScale,(255,0,0),thickness,cv2.LINE_AA)
    
    cv2.imshow("Object Measurement",frame)
    if DEBUG: cv2.imshow("Binary",erosion)
    # Keyboard funtions
    k = cv2.waitKey(1)
    if k == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('w') :
        print("===== "+ str(obj_width) +"cm x "+ str(obj_height) +"cm =====")
