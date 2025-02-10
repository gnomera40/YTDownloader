import yt_dlp
from tkinter import *
from tkinter import messagebox, ttk
import threading  # Import threading module
import re
import subprocess
import os
import sys
from PIL import Image, ImageTk
from yt_dlp import YoutubeDL

if TkVersion >= 8.6:
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except ImportError:
            pass
home_directory = os.path.expanduser("~")
download_directory = os.path.join(home_directory, "Downloads", "YouTube", "%(title)s.%(ext)s")
os.makedirs(os.path.dirname(download_directory), exist_ok=True)

current_directory1 = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path1 = os.path.join(current_directory1, 'logo.ico')


root = Tk()



try:
    icon_image = Image.open(ffmpeg_path1)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False,icon_photo)
except:()
root.config(background='#1f1f1f')
root.geometry('370x180')
root.title("YT Downloader v1.4")

root.resizable(False, False)
Label(root, text='GNOMERA', font=('Roboto', 20,'bold'),background="#1f1f1f",foreground="#ed8627").place(x=10, y=0)
Label(root, text='YouTube Downloader ▶', font=('Roboto', 9),background="#1f1f1f",foreground="white").place(x=13, y=34)

url_entry = Entry(root, width=43,font=("Roboto",9))
url_entry.place(x=10, y=60)
url_entry.focus()

selected_option = StringVar(root)
selected_option.set("mp3")
options = OptionMenu(root, selected_option, "video", "mp3")
options.place(x=9, y=95+20)
options.config(width=8, font=('Roboto', 8), cursor='hand2')

# Add a label to display download progress
progress_label = Label(root, text="Enter valid YouTube URL.", font=('Roboto Mono', 7),background="#1f1f1f",foreground='white')
progress_label.place(x=10, y=155)
title_label = Label(root, text='Ready',background="#1f1f1f",foreground='white',font=('Roboto',8))
title_label.place(x=10,y=98,anchor=W)
speed = Label(root,text='0MiB/s',background="#1f1f1f",foreground='gray',font=('Roboto',8))
speed.place(x=370,y=145+20,anchor=E)

def progress_hook(d):
    progress_text = f"Downloading... {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}"

    percent_str = d['_percent_str']  # e.g., "[0;94m 73.3% [0m"
    match = re.search(r'(\d+(\.\d+)?%)', percent_str)  # Looks for a number followed by a percent sign
    if match:
        percentage = match.group(1)  # Gets the matched percentage (e.g., "73.3%")
        progress_text = f"Downloading... {percentage}"
    else:
        progress_text = "Downloading... 0%"
        root.update_idletasks()
    kbps = d['_speed_str']
    match1 = re.search(r'(\d+(\.\d+)?MiB/s)', kbps)

    if match1:
        speed_text = match1.group(1)
    else:
        speed_text = '0MiB/s'

        root.update_idletasks()
        
    speed.config(text=speed_text)

    progress_label.config(text=progress_text)
    global filename
    filename = d['filename']

    
current_directory = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(current_directory, 'ffmpeg.exe')

print(ffmpeg_path)

def download():
    
    url = url_entry.get()
    
    if not url:
        messagebox.showwarning("Warning", "Please enter a YouTube URL.")
        return
    
    progress_label.config(text='Downloading...')
    # Define yt-dlp options
    if selected_option.get() == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': download_directory,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                
            }],
            'ffmpeg_location': ffmpeg_path,

            'progress_hooks': [progress_hook],  
            'nopostoverwrites': True,
        }
        try:
            title_label.config(text=YoutubeDL().extract_info(url, download=False).get('title'))
        except:
            messagebox.showerror("Error", "Invalid URL.")
            title_label.config(text='Ready')
            progress_label.config(text='Enter valid YouTube URL.')
            return
    else:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': download_directory,
            'progress_hooks': [progress_hook],
            'ffmpeg_location': ffmpeg_path,
            'nopostoverwrites': True,
            'merge_output_format': 'mp4',

 
}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            download_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)
            ydl.download([url])
            

        message = filename+ ' (converted) saved successfully.'
        messagebox.showinfo("Done", message)
        progress_label.config(text="Download complete.")
        download_button.config(state=NORMAL)
        stop_button.config(state=DISABLED)
        title_label.config(text='Ready')

        return
    except Exception as e:
        if selected_option.get() == 'mp3':
            ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': download_directory,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                
            }],
            

            'progress_hooks': [progress_hook],  
            'nopostoverwrites': True,
        }

        
        else:
            ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': download_directory,
            'progress_hooks': [progress_hook],
            
            'nopostoverwrites': True,
            'merge_output_format': 'mp4',
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            download_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)
            ydl.download([url])
            
        message = filename+ ' (converted) saved successfully.'
        messagebox.showinfo("Done", message)
        progress_label.config(text="Download complete.")
        download_button.config(state=NORMAL)
        stop_button.config(state=DISABLED)
        title_label.config(text='Ready')

        return
    except:
        download_button.config(state=NORMAL)
        stop_button.config(state=DISABLED)
        progress_label.config(text="Error occurred during download.")
        title_label.config(text='Ready')

        return
    

    

def start_download():
    title_label.config(text='Fetching video information...')
    threading.Thread(target=download).start()
    


def abort():
    stop_button.config(state=DISABLED)
    os.abort()
    

    return

def paste_from_clipboard(event):
    try:
        
        clipboard_content = root.clipboard_get()
        url_entry.insert(0, clipboard_content)
    except TclError:
        # Handle the case where the clipboard is empty or does not contain text
        pass

def opendownloads():
    try:
        subprocess.Popen(f'explorer "{os.path.join(home_directory,"Downloads","YouTube")}"')
    except:
        subprocess.run(['thunar', (os.path.join(home_directory,"Downloads","YouTube"))])

url_entry.bind("<Button-3>", paste_from_clipboard)
root.bind('<Return>',lambda event: download_button.invoke())
download_button = Button(root, cursor='hand2',text='Download', command=start_download,height=1,font=("Roboto",9,'bold'),width=8,background="#ed8627")
download_button.place(x=125, y=95+20)
stop_button = Button(root,cursor='hand2', text='Stop', command=abort,height=1,font=("Roboto",9),width=7,state=DISABLED)
stop_button.place(x=210, y=95+20)
Button(root, text='Clear', cursor='hand2',command=lambda: url_entry.delete(0,'end'),height=1,font=("Roboto",9),width=8).place(x=286,y=95+20)
Button(root, text='Show Downloads', cursor='hand2',command=opendownloads,height=1,font=("Roboto",9)).place(x=232,y=13)

root.mainloop()
