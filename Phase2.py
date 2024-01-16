from scipy.fft import fft
from scipy.io.wavfile import write
from tkinter import filedialog, messagebox
import scipy
from scipy.signal import butter, lfilter
import numpy as np
import tkinter as tk
from scipy import fftpack


global Uploaded_File_Successfully
Uploaded_File_Successfully=False
global File_Path
File_Path=None



SAMPLE_RATE = 8000  # Sample rate in Hz
CHARACTER_DURATION = 0.04  # Duration of each character in seconds
NUMBER_SAMPLES = int(SAMPLE_RATE * CHARACTER_DURATION)
FFT_SIZE = 1024  # fft size


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

# Create a reverse mapping from frequencies to characters
REVERSE_FREQUENCIES = {tuple(sorted(values)): key for key, values in FREQUENCIES.items()}

def decode_frequencies(frequencies):
    frequencies = tuple(sorted(frequencies))
    return REVERSE_FREQUENCIES.get(frequencies, '?')  # Return '?' for unknown frequencies


def bandpass_filter(data, lowcut, highcut, order=5):
    nyquist = 0.5 * SAMPLE_RATE
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def analyze_segment_with_filters(segment):
    low=[50,1050,2450]
    high=[550,1550,3550]
    detected_frequencies = []
    for i in range(3):
        x = bandpass_filter(segment, low[i],high[i],order=1)
        detected_frequencies.append( np.argmax(abs(fftpack.fft(x, FFT_SIZE))) * (SAMPLE_RATE / FFT_SIZE) )
        detected_frequencies[i] = int(round(detected_frequencies[i] / 100) * 100)

    return detected_frequencies

def decode_audio_file_with_filters(file_path):
    # Read the audio file
    x, data = scipy.io.wavfile.read(file_path)

    # Process in 40ms segments
    segment_length = NUMBER_SAMPLES
    decoded_string = ''

    for start in range(0, len(data), segment_length):
        segment = data[start:start + segment_length]
        if len(segment) < segment_length:
            break
        frequencies = analyze_segment_with_filters(segment)
        character = decode_frequencies(frequencies)
        decoded_string += character

    return decoded_string


def analyze_segment_with_frequencies(segment):
    # Compute the Fourier transform
    frequencies = np.fft.rfftfreq(len(segment), 1 / SAMPLE_RATE)
    magnitudes = np.abs(fft(segment))

    # Find the three highest amplitude frequencies
    highest_freqs = sorted(zip(frequencies, magnitudes), key=lambda x: x[1], reverse=True)[:3]
    a=[freq for freq, mag in highest_freqs]
    return a

def decode_audio_file_with_frequencies(file_path):
    # Read the audio file
    x,data = scipy.io.wavfile.read(file_path)
    # Normalize the data
    data = data / np.max(np.abs(data))
    # Process in 40ms segments
    segment_length = NUMBER_SAMPLES  # 40ms in samples
    decoded_string = ''

    for start in range(0, len(data), segment_length):
        segment = data[start:start + segment_length]
        if len(segment) < segment_length:
            break
        frequencies = analyze_segment_with_frequencies(segment)
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


def decode_file_frequency():
    global Uploaded_File_Successfully
    if Uploaded_File_Successfully:
        decoded_string = decode_audio_file_with_frequencies(File_Path)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, decoded_string)
    else:
        messagebox.showinfo("Error", f"Please upload a file as a (.wav)")

def decode_file_filters():
    global Uploaded_File_Successfully
    if Uploaded_File_Successfully:
        decoded_string = decode_audio_file_with_filters(File_Path)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, decoded_string)
    else:
        messagebox.showinfo("Error", f"Please upload a file as a (.wav)")


def open_new_window():
    new_window = tk.Toplevel()
    new_window.title("Decoder System")
    new_window.geometry("400x100")
    button1 = tk.Button(new_window, text="Decode using frequency", command=lambda: decode_file_frequency())
    button1.pack()

    button2 = tk.Button(new_window, text="Decode using filter", command=lambda: decode_file_filters())
    button2.pack()


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
    upload_button = tk.Button(root, text="run", command=open_new_window)
    upload_button.pack()

    root.mainloop()
