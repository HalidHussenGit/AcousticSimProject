# instruments.py
import numpy as np
from constants import fs

def pluck(freq):
    """Create initial noise buffer for Karplus-Strong pluck."""
    N = max(2, int(fs / freq))
    seed = np.random.uniform(-1, 1, int(max(2, int(fs/freq))))
    buf = np.empty(N, dtype=np.float32)
    for i in range(N):
        buf[i] = seed[i % len(seed)]
    return buf

def karplus_circular(buffer, buffer_idx, frames):
    """Advance Karplus-Strong delay line and return (out, new_buffer, new_idx)."""
    N = len(buffer)
    out = np.empty(frames, dtype=np.float32)
    for i in range(frames):
        a = buffer[buffer_idx]
        b = buffer[(buffer_idx + 1) % N]
        out[i] = a
        buffer[buffer_idx] = 0.996 * 0.5 * (a + b)
        buffer_idx = (buffer_idx + 1) % N
    return out, buffer, buffer_idx

def piano_block(freq, frames, pos, total):
    out = np.zeros(frames, dtype=np.float32)
    start = pos
    end = min(pos + frames, total)
    if start < end:
        t = np.arange(start, end) / fs
        wave = (
            0.6 * np.sin(2*np.pi*freq*t) +
            0.3 * np.sin(2*np.pi*2*freq*t) +
            0.15 * np.sin(2*np.pi*3*freq*t) +
            0.05 * np.sin(2*np.pi*4*freq*t)
        )
        env = np.exp(-3 * t)
        out[:end-start] = (wave * env).astype(np.float32)
    return out

def sax_block(freq, frames, pos, total):
    out = np.zeros(frames, dtype=np.float32)
    start = pos
    end = min(pos + frames, total)
    if start >= end:
        return out
    t = np.arange(start, end) / fs
    breath = np.minimum(t / 0.4, 1.0)
    vibrato = np.sin(2*np.pi*5*t) * (0.012 * breath)
    reed = np.tanh(1.5 * np.sin(2*np.pi*freq*t + vibrato))
    wave = (
        0.8 * reed +
        0.15 * np.sin(2*np.pi*2*freq*t) +
        0.05 * np.sin(2*np.pi*3*freq*t)
    ).astype(np.float32)
    env = (np.minimum(t / 0.35, 1.0) * np.exp(-0.7 * t)).astype(np.float32)
    signal = wave * env
    if len(signal) > 1:
        signal[1:] = 0.97 * signal[1:] + 0.03 * signal[:-1]
    out[:end-start] = signal
    return out

def flute_block(freq, frames, pos, total):
    out = np.zeros(frames, dtype=np.float32)
    start = pos
    end = min(pos + frames, total)
    if start < end:
        t = np.arange(start, end) / fs
        env = (1 - np.exp(-5*t)) * np.exp(-2*t)
        out[:end-start] = (env * np.sin(2*np.pi*freq*t)).astype(np.float32)
    return out