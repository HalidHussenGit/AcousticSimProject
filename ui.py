# ui.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons, Button
from constants import VIS_LEN
import instruments

_engine = None
_fig = None
_ani = None

def init_ui(engine, fig):
    global _engine, _fig
    _engine = engine
    _fig = fig

def clear_fig():
    global _ani
    if _ani:
        _ani.event_source.stop()
    _fig.clf()
    _fig.patch.set_facecolor('white')

def show_home(event=None):
    global _engine
    clear_fig()
    _engine.stop()

    # Title
    _fig.text(0.5, 0.8, "Acoustic Simulation Project", fontsize=32,
             color='#FF8C00', ha='center', fontweight='bold')

    # Buttons
    ax_sim = plt.axes([0.35, 0.50, 0.30, 0.08])
    ax_us = plt.axes([0.35, 0.38, 0.30, 0.08])
    ax_proj = plt.axes([0.35, 0.26, 0.30, 0.08])

    btn_sim = Button(ax_sim, "Go to Simulation", color='#FF8C00', hovercolor='#FFA500')
    btn_us = Button(ax_us, "About Developer", color='#FF8C00', hovercolor='#FFA500')
    btn_proj = Button(ax_proj, "About Project", color='#FF8C00', hovercolor='#FFA500')

    for b in [btn_sim, btn_us, btn_proj]:
        b.label.set_color('white')
        b.label.set_fontweight('bold')

    btn_sim.on_clicked(show_simulation)
    btn_us.on_clicked(show_about_us)
    btn_proj.on_clicked(show_about_project)

    _fig._btns = [btn_sim, btn_us, btn_proj]
    plt.draw()

def show_about_us(event=None):
    clear_fig()
    _fig.text(0.5, 0.85, "About the Developer", fontsize=28, color='#FF8C00', ha='center', fontweight='bold')

    about_text = (
        "Developer: Halid Hussen Yebre\n"
        "Email: halidhussen9@gmail.com\n"
        "Phone: +251976492500"
    )
    _fig.text(0.5, 0.45, about_text, fontsize=16, ha='center', va='center', linespacing=1.8)

    ax_back = plt.axes([0.42, 0.1, 0.16, 0.06])
    btn_back = Button(ax_back, "Back to Home", color='#FF8C00', hovercolor='#FFA500')
    btn_back.label.set_color('white')
    btn_back.on_clicked(show_home)
    _fig._btns = [btn_back]
    plt.draw()

def show_about_project(event=None):
    clear_fig()
    _fig.text(0.5, 0.85, "About the Project & Physics", fontsize=28, color='#FF8C00', ha='center', fontweight='bold')

    physics_text = (
        "The Physics of Sound Synthesis\n\n"
        "This simulation utilizes two primary methods of sound generation:\n\n"
        "1. Additive Synthesis (Piano/Flute): Combines multiple sine waves at harmonic\n"
        "frequencies to build complex timbres, mimicking the natural resonance of strings.\n\n"
        "2. Karplus-Strong Algorithm (Guitar/Bass): A form of physical modeling synthesis.\n"
        "It starts with a burst of white noise (representing a pluck) which is then passed\n"
        "through a filtered delay line. The physics involves a feedback loop where the\n"
        "averaging of adjacent samples acts as a low-pass filter, simulating the natural\n"
        "decay of a vibrating string.\n\n"
        "The 'Oscilloscope' visualizes the resulting longitudinal pressure waves as\n"
        "transverse amplitude displacements over time."
    )
    _fig.text(0.5, 0.45, physics_text, fontsize=14, ha='center', va='center', linespacing=1.5)

    ax_back = plt.axes([0.42, 0.1, 0.16, 0.06])
    btn_back = Button(ax_back, "Back to Home", color='#FF8C00', hovercolor='#FFA500')
    btn_back.label.set_color('white')
    btn_back.on_clicked(show_home)
    _fig._btns = [btn_back]
    plt.draw()

def show_simulation(event=None):
    global _engine, _ani
    clear_fig()
    _engine.start()

    # Re-setup the simulation axes
    ax = _fig.add_axes([0.15, 0.38, 0.80, 0.52])
    x = np.arange(VIS_LEN)
    line, = ax.plot(x, np.zeros_like(x), linewidth=1.0, color='#FF8C00')
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlim(0, VIS_LEN)
    ax.set_title("Live Amplitude Waveform (Oscilloscope)", fontsize=16, color='#FF8C00', fontweight='bold')

    txt_freq = _fig.text(0.15, 0.30, "Frequency (Hz): --", fontsize=11,
                        bbox=dict(facecolor='white', edgecolor='#FF8C00', alpha=0.7, boxstyle='round,pad=0.5'))
    txt_rms_raw = _fig.text(0.42, 0.30, "Amplitude (RMS, raw): --", fontsize=11,
                           bbox=dict(facecolor='white', edgecolor='#FF8C00', alpha=0.7, boxstyle='round,pad=0.5'))
    txt_rms_scaled = _fig.text(0.70, 0.30, "Amplitude (RMS, scaled): --", fontsize=11,
                              bbox=dict(facecolor='white', edgecolor='#FF8C00', alpha=0.7, boxstyle='round,pad=0.5'))

    def update_sim(frame):
        if _engine is None:
            return line, txt_freq, txt_rms_raw, txt_rms_scaled
        y = _engine.vis_buffer * 1.0
        smooth_y = np.convolve(y, np.ones(7)/7, mode='same')
        line.set_ydata(smooth_y)
        txt_freq.set_text(f"Frequency (Hz): {_engine.last_freq:.1f}")
        txt_rms_raw.set_text(f"Amplitude (RMS, raw): {_engine.last_rms_raw:.5f}")
        txt_rms_scaled.set_text(f"Amplitude (RMS, scaled): {_engine.last_rms_scaled:.5f}")
        return line, txt_freq, txt_rms_raw, txt_rms_scaled

    # Sliders
    ax_amp = plt.axes([0.15, 0.20, 0.30, 0.03])
    amp_slider = Slider(ax_amp, "Amplitude", 0.0, 1.0, valinit=_engine.amplitude, color='#FF8C00')
    ax_freq = plt.axes([0.55, 0.20, 0.30, 0.03])
    freq_slider = Slider(ax_freq, "Frequency (x)", 0.5, 2.0, valinit=_engine.transpose, color='#FF8C00')

    def slider_update(val):
        _engine.amplitude = amp_slider.val
        _engine.transpose = freq_slider.val
    amp_slider.on_changed(slider_update)
    freq_slider.on_changed(slider_update)

    # Radio
    ax_radio = plt.axes([0.02, 0.45, 0.10, 0.25])
    radio = RadioButtons(ax_radio, ("Guitar", "Piano", "Saxophone", "Bass", "Flute"), activecolor='#FF8C00')
    def change_instrument(label):
        _engine.instrument = label
        _engine.note_index = 0
        _engine.note_pos = 0
        _engine.vis_buffer[:] = 0.0
        if _engine.instrument in ("Guitar", "Bass"):
            _engine.buffer = instruments.pluck(_engine.melodies[_engine.instrument][0][0])
        else:
            _engine.buffer = None
    radio.on_clicked(change_instrument)

    # Buttons
    ax_start = plt.axes([0.70, 0.08, 0.10, 0.05])
    ax_stop  = plt.axes([0.82, 0.08, 0.10, 0.05])
    ax_home  = plt.axes([0.02, 0.08, 0.10, 0.05])

    btn_start = Button(ax_start, "Start ▶", color='#FF8C00', hovercolor='#FFA500')
    btn_stop  = Button(ax_stop,  "Stop ⏹", color='#FF8C00', hovercolor='#FFA500')
    btn_home  = Button(ax_home,  "Home 🏠", color='#FF8C00', hovercolor='#FFA500')

    for b in [btn_start, btn_stop, btn_home]:
        b.label.set_color('white')
        b.label.set_fontweight('bold')

    def start_audio_action(event):
        _engine.start()

    def stop_audio_action(event):
        _engine.stop()

    btn_start.on_clicked(start_audio_action)
    btn_stop.on_clicked(stop_audio_action)
    btn_home.on_clicked(show_home)

    # Store references to prevent GC
    _fig._sim_elements = [amp_slider, freq_slider, radio, btn_start, btn_stop, btn_home]

    # Re-init animation
    _ani = FuncAnimation(_fig, update_sim, interval=30, blit=False)
    plt.draw()