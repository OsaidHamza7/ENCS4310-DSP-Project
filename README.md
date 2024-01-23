# Voice-Frequency Encoder and Decoder for English Alphabet

## Introduction
This project is an innovative approach to encode and decode English alphabet characters using voice-frequency signals. It is a two-phase project that includes a user-friendly graphical interface for both encoding and decoding processes.

## Technologies
- **Programming Language**: Python
- **Libraries/Frameworks**: numpy, tkinter, scipy, sounddevice, matplotlib
  
## Technical Specifications
- **Sample Rate**: 8000 Hz
- **Character Duration**: 0.04 seconds

## Dependencies
Before running the project, ensure you have the following Python libraries installed:

- `numpy`: Used for numerical computations and signal processing.
- `scipy`: Provides tools for signal processing tasks, including Fourier transforms.
- `matplotlib`: For plotting and visualizing data.
- `sounddevice`: For audio input and output.
- `tkinter`: For building the graphical user interface.

You can install these dependencies using pip:

```bash
pip install numpy scipy matplotlib sounddevice
```

## Usage
This application allows users to encode and decode English strings using voice frequencies. Follow the steps below to use the application:

### To Encode:
1. Open the encoder GUI.
2. Enter the string you wish to encode.
3. The application will convert the string into a voice-frequency signal.

### To Decode:
1. Open the decoder GUI.
2. Upload the .wav file with the encoded signal.
3. The application will decode the signal back into the original text string.

## Phase One: Encoder
The encoder represents each English character by a combination of three voice-band frequency components. This phase involves building a GUI that encodes any English string into a corresponding signal.

### Features:
- GUI for easy interaction.
- Encode strings into voice-frequency signals.
- Play or save the signal as a .wav file.

## Phase Two: Decoder
The decoder recovers text strings from encoded multi-frequency signals using frequency analysis and bandpass filters.

### Features:
- GUI for uploading and decoding audio files.
- Two decoding approaches: frequency analysis and bandpass filters.
- Display the decoded text string.

## Testing
The system was thoroughly tested to ensure accurate encoding and decoding.Here are some of examples:
![](TestCases.mp4)
