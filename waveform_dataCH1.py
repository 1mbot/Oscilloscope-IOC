import time
import numpy as np
import matplotlib.pyplot as plt
from epics import PV

# PV name of the waveform record (adjust as needed)
pv_name = "Waveform_CH1"

# Create PV object
waveform_pv = PV(pv_name)

# Wait for connection
if not waveform_pv.wait_for_connection(timeout=5.0):
    raise RuntimeError(f"Could not connect to PV: {pv_name}")

# Wait for data update (optional: trigger acquisition before this)
print("Waiting for waveform data to update...")
time.sleep(2)

# Read the data
waveform_data = waveform_pv.get()

# Ensure data is valid
if waveform_data is None or len(waveform_data) == 0:
    raise RuntimeError("No waveform data received.")

# Convert to NumPy array (if not already)
waveform_data = np.array(waveform_data)

# Optional: truncate trailing zeros if necessary (common in EPICS waveform)
waveform_data = waveform_data[waveform_data != 0.0]

# Plot
plt.figure(figsize=(12, 4))
plt.plot(waveform_data, linewidth=1)
plt.title("Oscilloscope Waveform - CH1")
plt.xlabel("Sample Index")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.tight_layout()
plt.show()