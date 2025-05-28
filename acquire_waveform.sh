#!/bin/bash

# Set the oscilloscope IP and port
OSCILLOSCOPE_IP="120.10.10.247"
TELNET_PORT="4024"

# Output files
RAW_TXT="wf_data.txt"
CSV_FILE="wf_data.csv"

# Function to send commands via Telnet
send_command() {
    echo "$1"
    sleep 1
}

echo "Connecting to oscilloscope at $OSCILLOSCOPE_IP:$TELNET_PORT..."

# Open Telnet session, send commands, and store response
{
    send_command "*RST"           # Reset the oscilloscope
    send_command "CHAN1:STAT ON"  # Turn on CHAN1
    send_command "CHAN1:DATA?"    # Get waveform data
} | telnet $OSCILLOSCOPE_IP $TELNET_PORT | tail -n +4 | tee $RAW_TXT

echo "Waveform data saved to $RAW_TXT"

# Ensure wf_data.txt exists before processing
if [[ ! -s $RAW_TXT ]]; then
    echo "Error: Waveform data file is empty!"
    exit 1
fi

# Extract only numerical data and format as CSV (Ensure two-column structure)
awk 'NR>1 {printf "%s,%s\n", $1, $2}' $RAW_TXT > $CSV_FILE

if [[ ! -s $CSV_FILE ]]; then
    echo "Error: CSV file generation failed!"
    exit 1
fi

echo "Converted data saved as $CSV_FILE"

# Run Python script for real-time plotting
python3 plot_waveform.py
	




