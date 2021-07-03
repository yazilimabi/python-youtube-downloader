from tkinter import *
from tkinter import filedialog
import tkinter
from pytube import YouTube
import threading
import os

########################Functions########################
def refreshListbox():
    lb.delete('0','end')
    for video in queue:
        lb.insert('end',video.title)

def addVideo():
    threading.Thread(target=addVideoToQueue).start()

def addVideoToQueue():
    try:
        addButton["state"] = DISABLED
        notification['text'] = "Adding Video To Queue..."
        url = YouTube(str(link.get()))
        video = url.streams.filter(only_audio=bool(checkboxOutput.get())).first()
        queue.append(video)
        refreshListbox()
        notification['text'] = video.title + "\nSuccessfully Added To Queue"
        if not downloading:
            startButton["state"] = NORMAL
    except:
        notification['text'] = "An Error Occured Adding Video To Queue"
    
    addButton["state"] = NORMAL

def startDownload():
    startButton["state"] = DISABLED
    try:
        global filename
        filename = filedialog.askdirectory()
        if not filename:
            notification['text'] = "An Error Occured Selecting Directory"
        else:
            threading.Thread(target=downloadVideo).start()
    except:
        notification['text'] = "An Error Occured"

def downloadVideo():
    if len(queue)==0:
        startButton["state"] = DISABLED
        return
    try:
        global downloading
        downloading = True
        video = queue[0]
        videopath = video.download(output_path=filename)
        if(checkboxOutput.get()):
            base, ext = os.path.splitext(videopath)
            new_file = base + '.mp3'
            os.rename(videopath, new_file)
        notification['text'] = video.title + "\nDownload Finished Successfully"
        queue.pop(0)
        refreshListbox()
        if len(queue)>0:
            downloadVideo()
        else:
            downloading = False
            startButton["state"] = DISABLED
    except:
        notification['text'] = "An Error Occured"
        startButton["state"] = NORMAL
        downloading = False


########################TKinter Widgets########################
root = Tk()
root.geometry('800x400')
root.resizable(0,0)
root.title("Youtube Downloader")

queue = []
link = StringVar()
downloading = False

Label(root,text = 'Youtube Video Downloader', font ='arial 20 bold').pack()
notification = Label(root, text = '', font = 'arial 15')
notification.place(relx=.5 , rely=.9,anchor= CENTER)

label1 = Label(root, text = 'Paste Link Here:', font = 'arial 15 bold')
label1.place(x=250 , y = 60,anchor= CENTER)

link_enter = Entry(root, width = 70,textvariable = link)
link_enter.place(x=250, y=90,anchor= CENTER)

checkboxOutput = IntVar()
checkbox = Checkbutton(root, text="Audio Only", variable=checkboxOutput)
checkbox.place(x=250, y=120,anchor= CENTER)

addButton = Button(root,text = 'Add Video', font = 'arial 15 bold' ,bg = 'blue', command = addVideo)
addButton.place(x=250, rely=.5,anchor= CENTER)

lb = Listbox(root,font = 'arial 12 bold')
lb.place(x=600,y=150,anchor=CENTER)

startButton = Button(root,text = 'Start Download', font = 'arial 15 bold' ,bg = 'blue', command = startDownload)
startButton.place(x=600,y=285,anchor= CENTER)
startButton["state"] = DISABLED

root.mainloop()