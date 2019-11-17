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

def mark_person(loc,person):
    """
    function to mark the target person location in the image

    :param
        loc: represents the location of the target person
        person: the person name

    :return
        number of occurences target found in the image
    """
    count = 0
    for pt in zip(*loc[::-1]):
        count += 1
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
        cv2.putText(img_rgb,person, pt, cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2)
    return count

def show_exist(count,person):
    """
    function to print in the console whether the target person is found or not

    :param
        count: number of occurences the person found
        person: the person name
    """
    if (count <= 0):
        print('{} is not found in the Image'.format(person))
    else:
        print('{} is found in the Image'.format(person))

root = Tk()
root.title('Finding Waldo')

img_rgb = cv2.imread('wheres-waldo-2.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template_waldo = cv2.imread('waldo.png',0)
template_wenda = cv2.imread('wenda.png',0)

#saves the width and height of the template into 'w' and 'h'
w, h = template_waldo.shape[::-1]

res_waldo = cv2.matchTemplate(img_gray,template_waldo,cv2.TM_CCOEFF_NORMED)
res_wenda = cv2.matchTemplate(img_gray,template_wenda,cv2.TM_CCOEFF_NORMED)
threshold = 0.7

# finding the values where it exceeds the threshold
loc_waldo = np.where(res_waldo >= threshold)
loc_wenda = np.where(res_wenda >= threshold)

# mark location of target person as well as count the number of occurences target found
count_waldo=mark_person(loc_waldo,'waldo')
count_wenda=mark_person(loc_wenda,'wenda')

# print out in the console whether target person is found or not
show_exist(count_waldo,'waldo')
show_exist(count_wenda,'waldo')

cv2.imwrite('found_image.png',img_rgb)

image_list = ['wheres-waldo-2.jpg', 'found_image.png']

my_label = MainWindow(root,path='wheres-waldo-2.jpg')
my_label.grid(row=0,column=0,columnspan=4, rowspan=2)

button_back = Button(root,text="<<",command = back,state=DISABLED)
button_exit = Button(root,text="Exit Program",command = root.quit)
button_forward = Button(root,text=">>", command = lambda:forward(2))

button_back.grid(row=0,column = 1)
button_exit.grid(row=0,column = 2)
button_forward.grid(row=0,column = 3)

root.mainloop()
