
import tkinter as tk
from tkinter import filedialog, Listbox
import speech_recognition as sr
import pyttsx3
import pygame
import os
import random

# Initialize recognizer, TTS engine, and pygame mixer
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()

# Global variables
current_song = None
music_files = {}  

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        speak("Listening for your command.")
        try:
            print("Listening...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized Command: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I could not understand you.")
            return ""
        except sr.RequestError:
            speak("Request error from the speech recognition service.")
            return ""

# Function to handle voice commands
def process_voice_command():
    command = recognize_speech()
    if command:
        if "play" in command:
            play_selected_song()
        elif "pause" in command:
            pause_music()
        elif "resume" in command:
            resume_music()
        elif "stop" in command:
            stop_music()
        elif "shuffle" in command:
            shuffle_music()
        elif "add" in command or "load" in command:
            add_music()
        elif "next" in command:
            play_next_song()
        elif "back" in command:
            play_previous_song()
        else:
            update_song_label("Command not recognized.")
            speak("Command not recognized.")

# Function to play selected music
def play_selected_song():
    global current_song
    try:
        selected_song = playlist.get(tk.ACTIVE)
        if selected_song:
            song_path = music_files.get(selected_song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            current_song = selected_song
            update_song_label(f"Playing: {selected_song}")
            highlight_current_song()
            speak(f"Playing {selected_song}")
        else:
            update_song_label("Please select a song to play.")
            speak("Please select a song to play.")
    except Exception as e:
        update_song_label("Error playing the selected song.")
        speak("Unable to play the selected song.")
        print(e)

# Function to play the next song
def play_next_song():
    try:
        current_index = playlist.curselection()[0]
        next_index = (current_index + 1) % playlist.size()
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(next_index)
        playlist.activate(next_index)
        play_selected_song()
    except IndexError:
        update_song_label("No next song available.")
        speak("No next song available.")

# Function to play the previous song
def play_previous_song():
    try:
        current_index = playlist.curselection()[0]
        previous_index = (current_index - 1) % playlist.size()
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(previous_index)
        playlist.activate(previous_index)
        play_selected_song()
    except IndexError:
        update_song_label("No previous song available.")
        speak("No previous song available.")

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()
    update_song_label("Music stopped")
    clear_highlight()
    speak("Music stopped")

# Function to pause music
def pause_music():
    pygame.mixer.music.pause()
    update_song_label("Music paused")
    speak("Music paused")

# Function to resume music
def resume_music():
    pygame.mixer.music.unpause()
    update_song_label(f"Resumed: {current_song}")
    speak("Music resumed")

# Function to shuffle and play a random song
def shuffle_music():
    try:
        songs = playlist.get(0, tk.END)
        if songs:
            random_song = random.choice(songs)
            song_path = music_files.get(random_song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            global current_song
            current_song = random_song
            update_song_label(f"Playing: {random_song}")
            highlight_current_song(random_song)
            speak(f"Playing {random_song}")
        else:
            update_song_label("No songs to shuffle.")
            speak("No songs to shuffle.")
    except Exception as e:
        update_song_label("Error shuffling songs.")
        speak("Unable to shuffle songs.")
        print(e)

# Function to add music files or a folder of music
def add_music():
    choice = filedialog.askopenfilenames(
        title="Select Music Files or Folder",
        filetypes=[("MP3 Files", "*.mp3")],
    )
    if choice:
        for file in choice:
            if os.path.isfile(file):  # Add individual files
                file_name = os.path.basename(file)
                if file_name not in music_files:
                    music_files[file_name] = file
                    playlist.insert(tk.END, file_name)
        update_song_label("Music added successfully.")
        speak("Music added successfully.")
    else:
        folder = filedialog.askdirectory(title="Select a Folder Containing Music Files")
        if folder:
            for song in os.listdir(folder):
                if song.endswith(".mp3"):
                    song_path = os.path.join(folder, song)
                    if song not in music_files:
                        music_files[song] = song_path
                        playlist.insert(tk.END, song)
            update_song_label("Folder music added successfully.")
            speak("Folder music added successfully.")
        else:
            update_song_label("No files or folder selected.")
            speak("No files or folder selected.")

# Function to update the song label
def update_song_label(message):
    song_label.config(text=message)

# Function to highlight the currently playing song
def highlight_current_song(song=None):
    song = song or current_song
    for i in range(playlist.size()):
        if playlist.get(i) == song:
            playlist.selection_clear(0, tk.END)
            playlist.selection_set(i)
            playlist.activate(i)
            return

# Function to clear song highlights
def clear_highlight():
    playlist.selection_clear(0, tk.END)

# Main application
app = tk.Tk()
app.title("Music Player")
app.geometry("450x600")
app.resizable(False, False)
app.configure(bg="#7852A3")

# Song label
song_label = tk.Label(app, text="No song playing.", font=("Arial", 16), bg="#7852A3", fg="#ffffff", wraplength=400)
song_label.pack(pady=10)

# Playlist (Listbox)
playlist_frame = tk.Frame(app, bg="#7852A3")
playlist_frame.pack(pady=10, fill=tk.BOTH, expand=True)
playlist_scrollbar = tk.Scrollbar(playlist_frame, orient=tk.VERTICAL)
playlist = Listbox(playlist_frame, font=("Arial", 12), selectbackground="#1db954", activestyle="dotbox", selectmode=tk.SINGLE, yscrollcommand=playlist_scrollbar.set, bg="teal", fg="#ffffff")
playlist_scrollbar.config(command=playlist.yview)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(app, bg="#7852A3")
button_frame.pack(pady=10)

add_music_button = tk.Button(button_frame, text="Add Music", command=add_music, width=20, bg="#3f51b5", fg="white", font=("Arial", 12))
add_music_button.grid(row=0, column=0, columnspan=2, pady=5)

play_button = tk.Button(button_frame, text="Play", command=play_selected_song, width=10, bg="#2196f3", fg="white", font=("Arial", 12))
play_button.grid(row=1, column=0, padx=5, pady=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_music, width=10, bg="#f44336", fg="white", font=("Arial", 12))
stop_button.grid(row=1, column=1, padx=5, pady=5)

resume_button = tk.Button(button_frame, text="Resume", command=resume_music, width=10, bg="#4caf50", fg="white", font=("Arial", 12))
resume_button.grid(row=2, column=0, padx=5, pady=5)

shuffle_button = tk.Button(button_frame, text="Shuffle", command=shuffle_music, width=10, bg="#ff9800", fg="white", font=("Arial", 12))
shuffle_button.grid(row=2, column=1, padx=5, pady=5)

next_button = tk.Button(button_frame, text="Next", command=play_next_song, width=10, bg="#4caf50", fg="white", font=("Arial", 12))
next_button.grid(row=3, column=0, padx=5, pady=5)

back_button = tk.Button(button_frame, text="Back", command=play_previous_song, width=10, bg="#ff9800", fg="white", font=("Arial", 12))
back_button.grid(row=3, column=1, padx=5, pady=5)

voice_button = tk.Button(app, text="Voice Command", command=process_voice_command, width=20, bg="#ff5722", fg="white", font=("Arial", 14))
voice_button.pack(pady=20)

# Run the application
app.mainloop()
