import telnetlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

# Oscilloscope connection details
HOST = "120.10.10.247"
PORT = 4024  # Ensure correct port

# Connect to oscilloscope via Telnet
tn = telnetlib.Telnet(HOST, PORT)

# User selects which channels to turn ON
enabled_channels = []
for i in range(1, 5):
    choice = input(f"Enable CHAN{i}? (y/n): ").strip().lower()
    if choice == 'y':
        tn.write(f"CHAN{i}:STAT ON\n".encode())
        enabled_channels.append(i)

if not enabled_channels:
    print("No channels enabled. Exiting.")
    tn.close()
    exit()

print(f"Enabled channels: {enabled_channels}")

# === New Addition: Set Trigger Source ===
# Prompt user for trigger source
trigger_source = input(
    "Enter trigger source (CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1 | SBUS2 | D0..D15): "
).strip().upper()

# Send trigger source command to oscilloscope
tn.write(f"TRIGger:A:SOURce {trigger_source}\n".encode())

def get_waveform(channel):
    """Fetch waveform data from the selected channel via Telnet."""
    command = f"CHAN{channel}:DATA?\n".encode()
    tn.write(command)  # Request data
    raw_data = tn.read_until(b"\n").decode().strip()  # Read response
   
    try:
        data_points = np.array([float(i) for i in raw_data.split(',')])  # Convert to float array
    except ValueError:
        print(f"Invalid data received from CHAN{channel}. Skipping frame.")
        data_points = np.zeros(1000)  # Return zero array if parsing fails
   
    return data_points

# Initialize plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))  # Two subplots (Time & Frequency)
fig.suptitle(f"Real-Time Oscilloscope Waveform & FFT (Channels: {enabled_channels})")

# Time-domain plot
time_lines = {}  # Store line objects for each channel
for ch in enabled_channels:
    y_data = get_waveform(ch)
    x_data = np.linspace(0, len(y_data), len(y_data))
    line, = ax1.plot(x_data, y_data, label=f"Waveform (CHAN{ch})")
    time_lines[ch] = line

ax1.set_ylabel("Amplitude")
ax1.set_xlabel("Sample Index")
ax1.set_title("Time-Domain Waveform")
ax1.grid()
ax1.legend()

# Frequency-domain plot (FFT)
fft_lines = {}  # Store line objects for each channel
for ch in enabled_channels:
    y_data = get_waveform(ch)
    fft_data = np.fft.fft(y_data)
    freqs = np.fft.fftfreq(len(fft_data))
    line, = ax2.plot(freqs, np.abs(fft_data), label=f"FFT (CHAN{ch})")
    fft_lines[ch] = line

ax2.set_ylabel("Magnitude")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_title("Frequency Spectrum")
ax2.grid()
ax2.legend()

def update(frame):
    for ch in enabled_channels:
        new_y_data = get_waveform(ch)
       
        # Update time-domain plot
        x_data = np.linspace(0, len(new_y_data), len(new_y_data))
        time_lines[ch].set_xdata(x_data)
        time_lines[ch].set_ydata(new_y_data)
       
        # Update frequency-domain plot
        fft_data = np.fft.fft(new_y_data)
        freqs = np.fft.fftfreq(len(fft_data))
        fft_lines[ch].set_xdata(freqs)
        fft_lines[ch].set_ydata(np.abs(fft_data))
   
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    return list(time_lines.values()) + list(fft_lines.values())

def save_waveform():
    """Save waveform data for a selected channel to CSV."""
    try:
        ch_to_save = int(input(f"Enter channel to save {enabled_channels}: "))
        if ch_to_save not in enabled_channels:
            print("Invalid channel. Try again.")
            return

        y_data = get_waveform(ch_to_save)
        x_data = np.linspace(0, len(y_data), len(y_data))
        filename = f"waveform_CHAN{ch_to_save}.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Sample Index", "Amplitude"])
            writer.writerows(zip(x_data, y_data))

        print(f"Waveform from CHAN{ch_to_save} saved to {filename}")
   
    except ValueError:
        print("Invalid input. Please enter a valid channel number.")

def on_key(event):
    """Handle key presses for saving waveform data."""
    if event.key == 's':
        save_waveform()

fig.canvas.mpl_connect('key_press_event', on_key)

ani = FuncAnimation(fig, update, interval=50)  # Update every 50ms
plt.tight_layout()
plt.show()
