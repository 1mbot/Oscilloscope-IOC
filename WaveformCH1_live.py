import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from epics import PV

# PV name of the waveform record (adjust as needed)
pv_name = "Waveform_CH1"

# Create PV object
waveform_pv = PV(pv_name)

# Wait for connection
if not waveform_pv.wait_for_connection(timeout=5.0):
    raise RuntimeError(f"Could not connect to PV: {pv_name}")

# --- Live Plotting Setup ---

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 4))
line, = ax.plot([], [], lw=1)

ax.set_title("Live Oscilloscope - CH1")
ax.set_xlabel("Sample Index")
ax.set_ylabel("Voltage (V)")
ax.grid(True)

# Set initial limits (can be auto-scaled later)
ax.set_xlim(0, 1024)
ax.set_ylim(-5, 5)  # Adjust based on expected signal

# Update function for animation
def update(frame):
    waveform_data = waveform_pv.get()

    if waveform_data is None or len(waveform_data) == 0:
        return line,

    waveform_data = np.array(waveform_data)
    waveform_data = waveform_data[waveform_data != 0.0]  # Optional cleanup

    x = np.arange(len(waveform_data))
    line.set_data(x, waveform_data)

    ax.set_xlim(0, len(waveform_data))
    ax.set_ylim(np.min(waveform_data)-0.5, np.max(waveform_data)+0.5)

    return line,

# Create animation (update every 100 ms)
ani = animation.FuncAnimation(fig, update, interval=100, blit=True)

# Show plot
plt.tight_layout()
plt.show()
