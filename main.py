import pyttsx3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pydub import AudioSegment
import os

def get_voices():
    """Fetches the list of available TTS voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return voices

def text_to_speech():
    """Converts text to speech using the selected voice."""
    text = text_entry.get("1.0", tk.END).strip()
    
    if text:
        engine = pyttsx3.init()
        
        # Get the selected voice from the dropdown
        selected_voice = voice_var.get()
        for voice in voices:
            if voice.name == selected_voice:
                engine.setProperty('voice', voice.id)
        
        # Adjust rate and volume
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showerror("Input Error", "Please enter some text to convert to speech.")

def download_audio():
    """Saves the speech to an mp3 file."""
    text = text_entry.get("1.0", tk.END).strip()
    
    if text:
        engine = pyttsx3.init()
        
        # Get the selected voice
        selected_voice = voice_var.get()
        for voice in voices:
            if voice.name == selected_voice:
                engine.setProperty('voice', voice.id)
        
        # Generate the audio as a temporary WAV file
        temp_wav_file = "temp_audio.wav"
        engine.save_to_file(text, temp_wav_file)
        engine.runAndWait()
        
        # Open a file dialog to save the file as mp3
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            # Convert the WAV file to MP3 using pydub
            audio_segment = AudioSegment.from_wav(temp_wav_file)
            audio_segment.export(file_path, format="mp3")
            
            # Remove the temporary WAV file
            os.remove(temp_wav_file)
            
            messagebox.showinfo("Success", f"Audio saved as {file_path}")
    else:
        messagebox.showerror("Input Error", "Please enter some text to convert to speech.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Text to Speech")
root.geometry("400x400")

# Fetch available voices
voices = get_voices()

# Label for text entry
label = tk.Label(root, text="Enter text to convert to speech:", font=("Arial", 12))
label.pack(pady=10)

# Text entry widget
text_entry = tk.Text(root, wrap="word", height=10, width=40)
text_entry.pack(pady=10)

# Dropdown menu for selecting voice
voice_var = tk.StringVar(root)
voice_var.set(voices[0].name)  # Set default voice

voice_menu = ttk.OptionMenu(root, voice_var, *[voice.name for voice in voices])
voice_menu.pack(pady=10)

# Button to trigger text-to-speech
speak_button = tk.Button(root, text="Speak", command=text_to_speech, font=("Arial", 12))
speak_button.pack(pady=10)

# Button to download audio
download_button = tk.Button(root, text="Download Audio", command=download_audio, font=("Arial", 12))
download_button.pack(pady=10)

# Run the application
root.mainloop()
