import pygame
import os
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# Create window
mp3 = ctk.CTk()
mp3.geometry('400x480')
mp3.resizable(False, False)
mp3.title('MP3 Player')
pygame.mixer.init()

# Initialize variables
music_dir = None
music_files = []
current_song = ''
paused = False


# Define functions
def quitprogram():
    time.sleep(0.1)
    mp3.destroy()
    time.sleep(0.1)
    quit()


def load_music():
    global music_dir, music_files, current_song
    music_dir = load_directory()
    music_files = [music for music in os.listdir(
        music_dir) if music.endswith('.mp3')]
    for music in music_files:
        songlist.insert('end', music)
    songlist.selection_set(0)
    current_song = music_files[songlist.curselection()[0]]


def load_directory():
    root = tk.Tk()
    root.withdraw()
    music_dir = filedialog.askdirectory()
    return music_dir


def play_music():
    global current_song, paused
    if not paused:
        pygame.mixer.music.load(os.path.join(music_dir, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False


def play_selected_song(event):
    global current_song
    current_song = songlist.get(songlist.curselection())
    pygame.mixer_music.load(os.path.join(music_dir, current_song))
    pygame.mixer_music.play()


def skip_forward():
    global current_song, paused
    try:
        songlist.selection_clear(0, tk.END)
        songlist.selection_set(music_files.index(current_song) + 1)
        current_song = music_files[songlist.curselection()[0]]
        play_music()
    except:
        songlist.selection_set(0)
        current_song = music_files[songlist.curselection()[0]]
        play_music()


def skip_back():
    global current_song, paused
    try:
        songlist.selection_clear(0, tk.END)
        songlist.selection_set(music_files.index(current_song) - 1)
        current_song = music_files[songlist.curselection()[0]]
        play_music()
    except:
        songlist.selection_set("end")
        current_song = music_files[songlist.curselection()[0]]
        play_music()


def pause():
    global paused
    pygame.mixer.music.pause()
    paused = True


def volume(value):
    pygame.mixer.music.set_volume(value)


# Buttons
play_button = ctk.CTkButton(master=mp3, text='Play',
                            command=play_music, width=50)
play_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

skip_f = ctk.CTkButton(master=mp3, text='>', command=skip_forward, width=30)
skip_f.place(relx=0.75, rely=0.7, anchor=tk.CENTER)

skip_b = ctk.CTkButton(master=mp3, text='<', command=skip_back, width=30)
skip_b.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

pause_button = ctk.CTkButton(master=mp3, text='Pause', command=pause, width=50)
pause_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

load_button = ctk.CTkButton(master=mp3, text='Load music', command=load_music)
load_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

quit_button = ctk.CTkButton(master=mp3, text='Quit',
                            command=quitprogram, width=100)
quit_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

slider = ctk.CTkSlider(master=mp3, from_=0, to=1, command=volume, width=300)
slider.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

frame = tk.Frame(master=mp3)
frame.pack()

scrollbar = tk.Scrollbar(
    master=frame, orient='vertical', cursor='hand2')

songlist = tk.Listbox(master=frame, bg='black', fg='white',
                      width=60, height=15, yscrollcommand=scrollbar)

songlist.bind("<Double-Button-1>", play_selected_song)


scrollbar.config(command=songlist.yview)
scrollbar.pack(side="right", fill='y')

songlist.pack()

mp3.mainloop()
