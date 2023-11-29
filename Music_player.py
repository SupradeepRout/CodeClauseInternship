import os
from tkinter import Tk, Listbox, Button, filedialog, Label
from pygame import mixer
from PIL import Image, ImageTk

# Initialize Pygame mixer
mixer.init()

def populate_track_list(folder_path):
    tracks = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]
    return tracks

def play_music():
    selected_track = track_listbox.curselection()
    if selected_track:
        track_path = os.path.join(folder_path, track_listbox.get(selected_track))
        mixer.music.load(track_path)
        mixer.music.play()

def pause_music():
    mixer.music.pause()

def next_music():
    current_track = track_listbox.curselection()
    if current_track:
        next_track = (current_track[0] + 1) % track_listbox.size()
        track_listbox.selection_clear(current_track)
        track_listbox.selection_set(next_track)
        play_music()

def prev_music():
    current_track = track_listbox.curselection()
    if current_track:
        prev_track = (current_track[0] - 1) % track_listbox.size()
        track_listbox.selection_clear(current_track)
        track_listbox.selection_set(prev_track)
        play_music()

def insert_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    track_listbox.delete(0, "end")
    tracks = populate_track_list(folder_path)
    for track in tracks:
        track_listbox.insert("end", track)

root = Tk()
root.title("Music Player")
root.geometry("550x400+500+120")
root.resizable(0,0)
root.config(bg='#98F5FF')  # Set background color

# Left side - Music Player Image
image_path = "D:\\python program\\Project_Py\\Tkinter\\image\\unnamed.webp"  # Change this to the path of your music player image
img = Image.open(image_path)
img = img.resize((220, 220),Image.BICUBIC)
photo = ImageTk.PhotoImage(img)

music_player_label = Label(root, image=photo, bg="#e6e6e6",)
music_player_label.image = photo
music_player_label.place(x=50,y=60,)
# Right side - Track list and Buttons
track_listbox = Listbox(root, selectmode="SINGLE", bd=2,relief="solid",bg="white",fg='black', width=40, height=20)
track_listbox.place(x=300,y=60)

play_button = Button(root, text="Play",bg='#CAFF70',activebackground='#DC143C',cursor='hand2', command=play_music)
play_button.place(x=30,y=310) 

pause_button = Button(root, text="Pause",bg='#CAFF70',activebackground='#DC143C',cursor='hand2', command=pause_music)
pause_button.place(x=100,y=310) 

prev_button = Button(root, text="Prev.",bg='#CAFF70',activebackground='#DC143C',cursor='hand2', command=prev_music)
prev_button.place(x=178,y=310) 

next_button = Button(root, text="Next",bg='#CAFF70',activebackground='#DC143C',cursor='hand2', command=next_music)
next_button.place(x=250,y=310) 

insert_button = Button(root, text="Insert",bg='#CAFF70',activebackground='#DC143C',cursor='hand2', command=insert_folder)
insert_button.grid(row=0, column=0, padx=10, pady=10)

title_Lable=Label(root,text=" Py Music ",font=('Goudy Old Style',28,'bold'),bg='#C1CDCD',fg='#000000',padx=10)
title_Lable.place(x=190,y=0) 

root.mainloop()
