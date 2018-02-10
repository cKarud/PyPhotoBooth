import datetime
import os
import tkMessageBox
from Tkinter import *
from PIL import ImageTk, Image
import cv2

root = Tk()
root.title('My Photo Booth')
root.configure(background='black')
root.attributes('-fullscreen', True)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=10)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=10)
root.columnconfigure(4, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=20)
root.rowconfigure(2, weight=1)

img_back_path = "../resources/images/back.jpg"
img_print_path = "../resources/images/print.jpg"
img_potobooth_path = "../resources/images/photobooth.jpg"
img_camera_path = "../resources/images/camera.jpg"
img_exit_path = "../resources/images/exit.jpg"

img_back = ImageTk.PhotoImage(file=img_back_path)
img_print = ImageTk.PhotoImage(file=img_print_path)
img_photobooth = ImageTk.PhotoImage(file=img_potobooth_path)
img_camera = ImageTk.PhotoImage(file=img_camera_path)
img_exit = ImageTk.PhotoImage(file=img_exit_path)

labelPhotobooth = Label(root, bg="black", height=600, width=1200)

def printPhoto():
    print "Printing..."


def showImage(img):
    labelPhotobooth.configure(image=img)
    labelPhotobooth.image = img
    root.update()

def setInitPhoto():
    showImage(img_photobooth)

def goBack():
    setInitPhoto()


def countDown(seconds):
    for second in range(seconds, 0, -1):
        path = "../resources/images/"+str(second)+".jpg"
        img = ImageTk.PhotoImage(file=path)
        showImage(img)
        root.after(1000)


def createImageFolder(today):
    savedImagePath="../../../../PhotoBoothPictures/"+str(today)[:10]+"/"

    directory = os.path.abspath(savedImagePath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return savedImagePath


def saveImage(path, img, name):
    cv2.imwrite(path+name+'.jpg', img)


def takePhoto():
    today=datetime.datetime.now()
    path = createImageFolder(today)
    countDown(5)
    imgName = str(today.time())[:8].replace(":", "")

    cam = cv2.VideoCapture(0)
    img = cam.read()[1]
    saveImage(path, img, imgName)
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    showImage(imgtk)


def exit():
    result = tkMessageBox.askquestion("Warning", "Are you sure you want to quit?", icon='warning')
    if result == 'yes':
        root.destroy()

buttonBack = Button(root, image=img_back, command=lambda: goBack(), height=100, width=100)
buttonPrint = Button(root, image=img_print, command=lambda: printPhoto(), height=100, width=100)
buttonCamera = Button(root, image=img_camera, command=lambda: takePhoto(), height=100, width=100)
buttonExit = Button(root, image=img_exit, command=lambda: exit(), height=50, width=50)
showImage(img_photobooth)


buttonBack.grid(row=0, column=0, sticky=NW)
buttonPrint.grid(row=0, column=4, sticky=NE)
labelPhotobooth.grid(row=1, column=1, columnspan=3)
buttonCamera.grid(row=2, column=2, sticky=S)
buttonExit.grid(row=2, column=0, sticky=SW)

root.mainloop()
