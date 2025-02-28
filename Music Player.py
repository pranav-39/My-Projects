from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer
import os
import random
import time
import threading
from tkinter import ttk
from PIL import Image, ImageTk

mixer.init()

root = Tk()
root.geometry('800x400')
root.title('Music Player')
root.configure(bg='gray20')
root.resizable(0, 0)

current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')
current_time = StringVar(root, value='00:00')
playlist = []
current_index = -1
loop = False
song_length = 0

def load_songs():
    global playlist
    directory = filedialog.askdirectory(title='Select Songs Directory')
    if directory:
        os.chdir(directory)
        playlist = [f for f in os.listdir() if f.endswith(('.mp3', '.wav'))]
        song_listbox.delete(0, END)
        for song in playlist:
            song_listbox.insert(END, song)

def update_seek():
    while True:
        if mixer.music.get_busy():
            position = mixer.music.get_pos() // 1000
            mins, secs = divmod(position, 60)
            current_time.set(f"{mins:02}:{secs:02}")
            seek_slider.config(to=song_length, value=position)
        time.sleep(1)

threading.Thread(target=update_seek, daemon=True).start()

def play_song():
    global current_index, song_length
    if playlist:
        if song_listbox.curselection():
            current_index = song_listbox.curselection()[0]
        mixer.music.load(playlist[current_index])
        mixer.music.play()
        current_song.set(playlist[current_index])
        song_status.set("Playing")
        song_length = mixer.Sound(playlist[current_index]).get_length()
        seek_slider.config(to=song_length)

def stop_song():
    mixer.music.stop()
    song_status.set("Stopped")

def pause_song():
    mixer.music.pause()
    song_status.set("Paused")

def resume_song():
    mixer.music.unpause()
    song_status.set("Resumed")

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_song()

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_song()

def toggle_loop():
    global loop
    loop = not loop
    loop_btn.config(text=f"🔁 {'On' if loop else 'Off'}")

def shuffle_song():
    global current_index
    if playlist:
        current_index = random.randint(0, len(playlist) - 1)
        play_song()

def seek(event):
    position = seek_slider.get()
    mixer.music.play(start=position)

def change_volume(event):
    mixer.music.set_volume(volume_slider.get())

def forward_20s():
    position = mixer.music.get_pos() / 1000 + 20
    mixer.music.play(start=position)

def backward_10s():
    position = max(0, mixer.music.get_pos() / 1000 - 10)
    mixer.music.play(start=position)

song_frame = LabelFrame(root, text='Now Playing', bg='gray30', fg='white', font=('Arial', 12))
song_frame.pack(fill=X, padx=10, pady=5)
Label(song_frame, textvariable=current_song, bg='gray30', fg='gold', font=('Arial', 12)).pack()
Label(song_frame, textvariable=current_time, bg='gray30', fg='white', font=('Arial', 10)).pack()

Button(root, text='📂 Load Directory', command=load_songs, bg='gray40', fg='white').pack(pady=5)

button_frame = Frame(root, bg='gray20')
button_frame.pack()
Button(button_frame, text='▶ Play', command=play_song, bg='green', fg='white').grid(row=0, column=0, padx=5, pady=5)
Button(button_frame, text='⏸ Pause', command=pause_song, bg='orange', fg='white').grid(row=0, column=1, padx=5, pady=5)
Button(button_frame, text='⏯ Resume', command=resume_song, bg='blue', fg='white').grid(row=0, column=2, padx=5, pady=5)
Button(button_frame, text='⏹ Stop', command=stop_song, bg='red', fg='white').grid(row=0, column=3, padx=5, pady=5)
Button(button_frame, text='⏮ Prev', command=prev_song, bg='purple', fg='white').grid(row=0, column=4, padx=5, pady=5)
Button(button_frame, text='⏭ Next', command=next_song, bg='purple', fg='white').grid(row=0, column=5, padx=5, pady=5)
loop_btn = Button(button_frame, text='🔁 Loop: Off', command=toggle_loop, bg='darkgray', fg='white')
loop_btn.grid(row=0, column=6, padx=5, pady=5)
Button(button_frame, text='🔀 Shuffle', command=shuffle_song, bg='darkgray', fg='white').grid(row=0, column=7, padx=5, pady=5)

seek_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=400, command=seek, bg='gray40', fg='white')
seek_slider.pack(pady=5)
volume_slider = Scale(root, from_=0, to=1, resolution=0.1, orient=HORIZONTAL, length=200, command=change_volume, bg='gray40', fg='white')
volume_slider.set(0.5)
volume_slider.pack(pady=5)

control_frame = Frame(root, bg='gray20')
control_frame.pack()
Button(control_frame, text='⏪ << 10s', command=backward_10s, bg='gray40', fg='white').grid(row=0, column=0, padx=5)
Button(control_frame, text='⏩ >> 20s', command=forward_20s, bg='gray40', fg='white').grid(row=0, column=1, padx=5)

song_listbox = Listbox(root, selectbackground='gold', height=10, bg='black', fg='white')
song_listbox.pack(fill=BOTH, padx=10, pady=5)

root.mainloop()
