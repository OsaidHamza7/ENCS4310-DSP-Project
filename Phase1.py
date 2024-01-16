import numpy as np
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.fftpack import fft
from scipy.io.wavfile import write
import time
from tkinter.simpledialog import askstring
from matplotlib import pyplot as plt


# Constants
SAMPLE_RATE = 8000  # Sample rate in Hz
CHARACTER_DURATION = 0.04  # Duration of each character in seconds
NUMBER_SAMPLES = int(SAMPLE_RATE * CHARACTER_DURATION)

# Encoding frequencies for each English character
FREQUENCIES = {
    'a': [100, 1100, 2500], 'b': [100, 1100, 3000], 'c': [100, 1100, 3500],
    'd': [100, 1300, 2500], 'e': [100, 1300, 3000], 'f': [100, 1300, 3500],
    'g': [100, 1500, 2500], 'h': [100, 1500, 3000], 'i': [100, 1500, 3500],
    'j': [300, 1100, 2500], 'k': [300, 1100, 3000], 'l': [300, 1100, 3500],
    'm': [300, 1300, 2500], 'n': [300, 1300, 3000], 'o': [300, 1300, 3500],
    'p': [300, 1500, 2500], 'q': [300, 1500, 3000], 'r': [300, 1500, 3500],
    's': [500, 1100, 2500], 't': [500, 1100, 3000], 'u': [500, 1100, 3500],
    'v': [500, 1300, 2500], 'w': [500, 1300, 3000], 'x': [500, 1300, 3500],
    'y': [500, 1500, 2500], 'z': [500, 1500, 3000], ' ': [500, 1500, 3500]
}

def generate_character_signal(frequencies):
    character_signal = []
    for n in range(NUMBER_SAMPLES):
        character_signal.append (  np.cos(frequencies[0] * 2 * np.pi * n / SAMPLE_RATE)
                                 + np.cos(frequencies[1] * 2 * np.pi * n / SAMPLE_RATE)
                                 + np.cos(frequencies[2] * 2 * np.pi * n / SAMPLE_RATE)
                                )
    return character_signal

def encode_string_to_signal(input_string):
    signal = []
    for char in input_string:
        signal = np.concatenate( (signal,generate_character_signal(FREQUENCIES[char]) ) , axis=None )
    return signal

def getInputString():
    input_text = text_entry.get("1.0", tk.END).strip().lower()
    if not input_text:
        messagebox.showerror("Error", "Please enter some text to encode.")
        return
    return input_text

def encode():
    input_text=getInputString()
    encoded_signal = encode_string_to_signal(input_text)
    return encoded_signal

def save_generated_signal():
    encoded_signal = encode()
    file_path = askstring('Name', 'Enter a name of file to save the generated signal:')

    if file_path[-4:]!=".wav":
        file_path+=".wav"

    if file_path:
        normalized_signal = np.int16((encoded_signal / encoded_signal.max()) * 32767)
        write(file_path, SAMPLE_RATE, normalized_signal)
        messagebox.showinfo("Success", f"File saved as {file_path} .")

def play_generated_signal():
    # Generate the encoded signal
    encoded_signal = encode()
    # Normalize the signal to the range -1.0 to 1.0
    #encoded_signal = encoded_signal / np.max(np.abs(encoded_signal))
    # Play the sound
    sd.play(encoded_signal, SAMPLE_RATE)
    # Wait until sound has finished playing
    time.sleep(1)
    plot_signal(encoded_signal)

def plot_signal(signal):

    # Plotting
    plt.figure(figsize=(10, 6))

    # Time domain plot
    plt.subplot(2, 1, 1)  # 2 rows, 1 column, first plot
    time = np.linspace(0, len(signal) / SAMPLE_RATE, num=len(signal))

    plt.plot(time, signal)
    plt.title(f"Time Domain: Encoded Signal ")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Frequency domain plot
    plt.subplot(2, 1, 2)

    N = len(signal)
    freq = np.fft.fftfreq(N, 1 / SAMPLE_RATE)
    freq = freq[:N // 2]

    magnitude = np.abs(fft(signal))
    magnitude = magnitude[:N // 2]

    plt.plot(freq, magnitude)  # Plot only the positive frequencies
    plt.title("Frequency Domain: Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    #Create the main window
    root = tk.Tk()
    root.title("Voice-Frequency Encoder")

    # Create a text entry widget
    text_entry = tk.Text(root, height=10, width=50)
    text_entry.pack()

    # Create a button to trigger the encoding and saving
    save_button = tk.Button(root, text="save the generated signal as (.wav)", command=save_generated_signal)
    save_button.pack()

    # Create a button to trigger the play sound
    play_button = tk.Button(root, text="play the generated signal", command=play_generated_signal)
    play_button.pack()

    # Run the GUI event loop
    root.mainloop()



