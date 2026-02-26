# Acoustic Simulation Project

A **Python-based interactive acoustic simulation tool** that models and visualizes the sounds of various musical instruments in real time. This project demonstrates **digital sound synthesis** and **signal processing techniques** through an educational and interactive platform.

The simulation combines:

- **Additive Synthesis**: For instruments like piano and flute, multiple sine waves at harmonic frequencies are combined to build complex timbres, mimicking natural resonances.
- **Karplus-Strong Algorithm**: For plucked string instruments like guitar and bass, this physical modeling technique generates realistic string vibrations using a noise burst passed through a filtered delay line.

## Features

- **Real-Time Audio Playback**: Generate instrument sounds on the fly with precise timing.
- **Adjustable Parameters**: Control amplitude and pitch using intuitive sliders.
- **Oscilloscope Visualization**: Live waveform display to visualize amplitude variations over time.
- **Instrument Selection**: Choose from Guitar, Piano, Saxophone, Bass, and Flute.
- **Interactive GUI**: Includes start/stop buttons, sliders, radio buttons, and navigation between home, about developer, and simulation screens.
- **Modular Code Structure**: Separated into multiple Python modules for maintainability and ease of extension.

## Technologies Used

- **Python 3**
- **NumPy**: Numerical computations for signal generation and processing
- **Matplotlib**: GUI rendering and real-time waveform visualization
- **SoundDevice**: Low-latency audio output
- **Matplotlib Widgets**: Interactive sliders, buttons, and radio buttons

## Project Structure

| File | Description |
|------|-------------|
| `constants.py` | Stores all constants, note frequencies, and melodies |
| `instruments.py` | Functions to generate instrument-specific audio samples |
| `audio_engine.py` | Core audio engine, handling playback, note timing, and buffer processing |
| `ui.py` | Graphical interface, navigation, and real-time visualization |
| `main.py` | Entry point to launch the application |
| `README.md` | Project documentation |

## About the Developer

**Halid Hussen Yebre**  
- **Email:** halidhussen9@gmail.com  
- **Phone:** +251976492500  

## Installation

Make sure you have Python 3 installed. Then install the required packages:

```bash
pip install numpy matplotlib sounddevice


## Screenshots

### Simulation GUI
![Simulation GUI](screenshots/gui.png)

### Oscilloscope View
![Oscilloscope](D:\_Turkey Burslari\AcousticSimProject\screenshots\Screenshot 2026-02-26 230703.png)
