# audio_engine.py
import numpy as np
import sounddevice as sd
from constants import fs, block, VIS_LEN, melodies, amplitude_default, transpose_default, instrument_default
import instruments

class AudioEngine:
    def __init__(self):
        # GUI-controllable
        self.amplitude = amplitude_default
        self.transpose = transpose_default
        self.instrument = instrument_default
        self.audio_running = True

        # playback state
        self.note_index = 0
        self.note_pos = 0
        self.buffer = None
        self.buffer_idx = 0

        # visualization buffer
        self.VIS_LEN = VIS_LEN
        self.vis_buffer = np.zeros(self.VIS_LEN, dtype=np.float32)

        # readouts
        self.last_freq = 0.0
        self.last_rms_raw = 0.0
        self.last_rms_scaled = 0.0

        self.fs = fs
        self.block = block
        self.melodies = melodies

        self.stream = None

    def init_stream(self):
        if not self.stream:
            self.stream = sd.OutputStream(samplerate=self.fs, channels=1, blocksize=self.block, callback=self.callback)

    def start(self):
        self.init_stream()
        if self.stream and not self.stream.active:
            self.stream.start()
        self.audio_running = True

    def stop(self):
        self.audio_running = False
        if self.stream and self.stream.active:
            self.stream.stop()

    def close(self):
        if self.stream:
            try:
                if self.stream.active:
                    self.stream.stop()
            except Exception:
                pass
            try:
                self.stream.close()
            except Exception:
                pass
            self.stream = None

    def callback(self, outdata, frames, time, status):
        # This mirrors the previous monolithic callback but uses instance state
        if not self.audio_running:
            outdata[:] = 0
            return

        melody = self.melodies[self.instrument]
        freq, dur = melody[self.note_index]
        freq *= self.transpose
        total = int(dur * self.fs)

        if self.note_pos == 0 and self.instrument in ("Guitar", "Bass"):
            self.buffer = instruments.pluck(freq)
            self.buffer_idx = 0

        if self.instrument == "Piano":
            sound = instruments.piano_block(freq, frames, self.note_pos, total)
        elif self.instrument in ("Guitar", "Bass"):
            if self.buffer is None:
                self.buffer = instruments.pluck(freq)
                self.buffer_idx = 0
            sound, self.buffer, self.buffer_idx = instruments.karplus_circular(self.buffer, self.buffer_idx, frames)
        elif self.instrument == "Saxophone":
            sound = instruments.sax_block(freq, frames, self.note_pos, total)
        else:
            sound = instruments.flute_block(freq, frames, self.note_pos, total)

        if len(sound) < frames:
            sound = np.pad(sound, (0, frames - len(sound)))
        elif len(sound) > frames:
            sound = sound[:frames]

        self.last_rms_raw = float(np.sqrt(np.mean(sound.astype(np.float64)**2)))
        self.last_rms_scaled = self.last_rms_raw * self.amplitude
        self.last_freq = freq

        # update visualization buffer
        self.vis_buffer = np.roll(self.vis_buffer, -frames)
        if frames >= self.VIS_LEN:
            self.vis_buffer[:] = sound[-self.VIS_LEN:]
        else:
            self.vis_buffer[-frames:] = sound[-frames:]

        outdata[:, 0] = (self.amplitude * sound).astype(np.float32)

        # step note
        self.note_pos += frames
        if self.note_pos >= total:
            self.note_pos = 0
            self.note_index = (self.note_index + 1) % len(melody)