# main.py
import matplotlib.pyplot as plt
from audio_engine import AudioEngine
import ui

def main():
    fig_w, fig_h = 14, 8.5
    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('white')

    engine = AudioEngine()

    ui.init_ui(engine, fig)
    ui.show_home()

    try:
        plt.show()
    finally:
        engine.close()

if __name__ == '__main__':
    main()