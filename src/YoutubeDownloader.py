from tkinter import *
from tkinter import filedialog
from tkinter import ttk 
from pytube import YouTube
import threading
import os

########################Classes########################
class videoItem:
    def __init__(self, video, onlyAudio):
        self.video = video
        self.onlyAudio = onlyAudio

    
########################Functions########################
def entryRightClickPopup(event):
    menu.post(event.x_root, event.y_root)

def refreshListbox():
    lb.delete('0','end')
    for item in queue:
        lb.insert('end',item.video.title)

def removeSelectedFromQueue():
    selections = lb.curselection()
    if selections:
        for index in selections:
            queue.pop(index)
    refreshListbox()

def addVideo():
    threading.Thread(target=addVideoToQueue).start()

def addVideoToQueue():
    try:
        addButton["state"] = DISABLED
        notification['text'] = "Adding Video To Queue..."
        audio = checkboxOutput.get()
        url = YouTube(str(link.get()))
        video = url.streams.filter(only_audio=audio).first()
        queue.append(videoItem(video,audio))
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
        video = queue[0].video
        videopath = video.download(output_path=filename)
        if(queue[0].onlyAudio):
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
root.geometry('800x500')
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

link_enter = Entry(root, width = 70,textvariable = link,)
link_enter.place(x=250, y=90,anchor= CENTER)

checkboxOutput = IntVar()
checkbox = Checkbutton(root, text="Audio Only", variable=checkboxOutput)
checkbox.place(x=250, y=120,anchor= CENTER)

addButton = Button(root,text = 'Add Video To Queue', font = 'arial 15 bold' ,bg = 'blue', command = addVideo)
addButton.place(x=250, y=200,anchor= CENTER)

lb = Listbox(root,font = 'arial 12 bold')
lb.place(x=620,y=195,anchor=CENTER)

progress = ttk.Progressbar(root,length=300)
progress.place(x=250,y=280,anchor=CENTER)

startButton = Button(root,text = 'Start Download', font = 'arial 15 bold' ,bg = 'blue', command = startDownload)
startButton.place(x=620,y=330,anchor= CENTER)
startButton["state"] = DISABLED

deleteButton = Button(root,text = 'Remove Selection From Queue', font = 'arial 12 bold' ,bg = 'red', command = removeSelectedFromQueue)
deleteButton.place(x=620,y=60,anchor= CENTER)

menu = Menu(root, tearoff=0)
menu.add_command(label="Cut", command=lambda: link_enter.event_generate("<<Cut>>"))
menu.add_command(label="Copy", command=lambda: link_enter.event_generate("<<Copy>>"))
menu.add_command(label="Paste", command=lambda: link_enter.event_generate("<<Paste>>"))
menu.add_separator()
menu.add_command(label="Select all", command=lambda: link_enter.select_range(0, 'end'))

link_enter.bind("<Button-3>", entryRightClickPopup)

root.mainloop()