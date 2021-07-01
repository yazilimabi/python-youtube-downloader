from tkinter import *
from pytube import YouTube
import threading
from pathlib import Path

root = Tk()
root.geometry('600x400')
root.resizable(0,0)
root.title("Youtube Downloader")

Label(root,text = 'Youtube Video Downloader', font ='arial 20 bold').pack()
notification = Label(root, text = '', font = 'arial 15')
notification.place(relx=.5 , rely=.9,anchor= CENTER)

link = StringVar()

label1 = Label(root, text = 'Paste Link Here:', font = 'arial 15 bold')
label1.place(relx=.5 , y = 60,anchor= CENTER)

link_enter = Entry(root, width = 70,textvariable = link)
link_enter.place(relx=.5, y=90,anchor= CENTER)

checkboxOutput = IntVar()
checkbox = Checkbutton(root, text="Audio Only", variable=checkboxOutput)
checkbox.place(relx=.5, y=120,anchor= CENTER)

def startDownload():
    button["state"] = DISABLED
    threading.Thread(target=downloadVideo).start()
def downloadVideo():
    try:
        url =YouTube(str(link.get()))
        video = url.streams.filter(only_audio=bool(checkboxOutput.get())).first()
        video.download()
        if(checkboxOutput.get()):
            p = Path(video.title+".mp4")
            p.rename(p.with_suffix('.mp3'))
        notification['text'] = video.title + "\nDownload Finished Successfully"
    except:
        notification['text'] = "An Error Occured"

    button["state"] = NORMAL

button = Button(root,text = 'Download', font = 'arial 15 bold' ,bg = 'red', command = startDownload)
button.place(relx=.5, rely=.5,anchor= CENTER)

root.mainloop()