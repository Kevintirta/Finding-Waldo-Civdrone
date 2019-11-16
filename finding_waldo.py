import cv2
import matplotlib
import numpy as np
import image
import os
import time
from tkinter import *
from PIL import ImageTk,Image
from zoom_advance import MainWindow

def forward(image_number):
    """
    function to go to the next page

    :param
        image_number: represents the image sequence (first image, second,image, etc)
    """
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = MainWindow(root,path=image_list[image_number-1])
    button_forward = Button(root,text=">>", command = lambda:forward(image_number+1))
    button_back = Button(root,text="<<",command = lambda:back(image_number-1))

    if image_number == 2:
        button_forward = Button(root, text=">>",state=DISABLED)

    my_label.grid(row=0,column=0,columnspan=4, rowspan=2)
    button_back.grid(row=0,column = 1)
    button_forward.grid(row=0,column = 3)


def back(image_number):
    """
    function to go to the previous image

    :param
        image_number: represents the image sequence (first image, second,image, etc)
    """
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = MainWindow(root,path=image_list[image_number-1])
    button_forward = Button(root,text=">>", command = lambda:forward(image_number+1))
    button_back = Button(root,text="<<",command = lambda:back(image_number-1))

    if image_number == 1:
        button_back = Button(root, text="<<",state=DISABLED)

    my_label.grid(row=0,column=0,columnspan=4, rowspan=2)
    button_back.grid(row=0,column = 1)
    button_forward.grid(row=0,column = 3)


root = Tk()
root.title('Finding Waldo')

img_rgb = cv2.imread('wheres-waldo-2.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('waldo.png',0)

#saves the width and height of the template into 'w' and 'h'
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.7

# finding the values where it exceeds the threshold
count = 0
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    #draw rectangle on places where it exceeds threshold
    count += 1
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)

# print out in the console whether waldo is found or not
if (count <= 0):
    print('Waldo is not found in the Image')
else:
    print('Waldo is found in the Image')

cv2.imwrite('found_waldo.png',img_rgb)

image_list = ['wheres-waldo-2.jpg', 'found_waldo.png']

my_label = MainWindow(root,path='wheres-waldo-2.jpg')
my_label.grid(row=0,column=0,columnspan=4, rowspan=2)

button_back = Button(root,text="<<",command = back,state=DISABLED)
button_exit = Button(root,text="Exit Program",command = root.quit)
button_forward = Button(root,text=">>", command = lambda:forward(2))

button_back.grid(row=0,column = 1)
button_exit.grid(row=0,column = 2)
button_forward.grid(row=0,column = 3)

root.mainloop()
