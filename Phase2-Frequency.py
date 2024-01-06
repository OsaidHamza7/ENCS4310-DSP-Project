import numpy as np
import scipy
from scipy.fft import fft
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
import sounddevice as sd
from scipy.io.wavfile import write



global Uploaded_File_Successfully
Uploaded_File_Successfully=False
global File_Path
File_Path=None


SAMPLE_RATE = 44100  # Sample rate in Hz
CHARACTER_DURATION = 0.04  # Duration of each character in seconds
VOLUME = 0.5  # Volume, as a float between 0.0 and 1.0



FREQUENCIES = {
    'a': [100, 1100, 2500],'b': [100, 1100, 3000],'c': [100, 1100, 3500],
    'd': [100, 1300, 2500], 'e': [100, 1300, 3000], 'f': [100, 1300, 3500],
    'g': [100, 1500, 2500], 'h': [100, 1500, 3000], 'i': [100, 1500, 3500],
    'j': [300, 1100, 2500], 'k': [300, 1100, 3000], 'l': [300, 1100, 3500],
    'm': [300, 1300, 2500], 'n': [300, 1300, 3000], 'o': [300, 1300, 3500],
    'p': [300, 1500, 2500], 'q': [300, 1500, 3000], 'r': [300, 1500, 3500],
    's': [500, 1100, 2500], 't': [500, 1100, 3000], 'u': [500, 1100, 3500],
    'v': [500, 1300, 2500], 'w': [500, 1300, 3000], 'x': [500, 1300, 3500],
    'y': [500, 1500, 2500], 'z': [500, 1500, 3000], ' ': [500, 1500, 3500]
}

# Create a reverse mapping from frequencies to characters
REVERSE_FREQUENCIES = {tuple(sorted(values)): key for key, values in FREQUENCIES.items()}

def analyze_segment(segment):
    # Compute the Fourier transform
    frequencies = np.fft.rfftfreq(len(segment), 1 / SAMPLE_RATE)
    magnitudes = np.abs(fft(segment))

    # Find the three highest amplitude frequencies
    highest_freqs = sorted(zip(frequencies, magnitudes), key=lambda x: x[1], reverse=True)[:3]
    return [freq for freq, mag in highest_freqs]

def decode_frequencies(frequencies):
    frequencies = tuple(sorted(frequencies))
    return REVERSE_FREQUENCIES.get(frequencies, '?')  # Return '?' for unknown frequencies


def decode_audio_file(file_path):

    # Read the audio file
    x,data = scipy.io.wavfile.read(file_path)

    # Normalize the data
    data = data / np.max(np.abs(data))

    # Process in 40ms segments
    segment_length = int(0.04 * SAMPLE_RATE)  # 40ms in samples
    decoded_string = ''

    for start in range(0, len(data), segment_length):
        segment = data[start:start + segment_length]
        if len(segment) < segment_length:
            break
        frequencies = analyze_segment(segment)
        character = decode_frequencies(frequencies)
        decoded_string += character

    return decoded_string


def upload_audio_file():
    global File_Path
    File_Path = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if File_Path:
        global Uploaded_File_Successfully
        Uploaded_File_Successfully = True
        messagebox.showinfo("Success", f"File uploaded successfully")

def decode_file():
    global Uploaded_File_Successfully
    if Uploaded_File_Successfully:
        decoded_string = decode_audio_file(File_Path)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, decoded_string)
    else:
        messagebox.showinfo("Error", f"Please upload a file as a (.wav)")



if __name__ == "__main__":

    #Create the main window
    root = tk.Tk()
    root.title("Voice-Frequency Decoder")

    #Create a text of the output result
    result_text = tk.Text(root, height=10, width=50)
    result_text.pack()

    # Add file upload
    upload_button = tk.Button(root, text="upload audio file(.wav)", command=upload_audio_file)
    upload_button.pack()

    # result display widgets to your GUI
    upload_button = tk.Button(root, text="run", command=decode_file)
    upload_button.pack()

    root.mainloop()
