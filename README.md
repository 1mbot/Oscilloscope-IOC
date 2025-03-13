# **Oscilloscope-IOC**  
**EPICS IOC for Rohde & Schwarz RTM3000 Oscilloscope**  

## **Overview**  
This repository contains an **EPICS IOC** (Input/Output Controller) for controlling and monitoring the **Rohde & Schwarz RTM3000 Oscilloscope** via **RS232 (Serial) communication**. It allows full remote control of the oscilloscope using **SCPI commands** through **EPICS Channel Access**.  

## **Features**  
- **Remote Control**: Set and read parameters such as voltage, current, frequency, and trigger settings.  
- **SCPI Integration**: Uses **Standard Commands for Programmable Instruments (SCPI)** to communicate with the oscilloscope.  
- **Full EPICS Support**: Implements **EPICS records** (ai, ao, bi, bo, mbbo, waveform) for seamless integration.  
- **Support for Multiple Channels**: Enables control and acquisition from multiple channels.  
- **Waveform Acquisition**: Retrieve waveform data directly from the oscilloscope.  

## **Requirements**  
### **Hardware**  
- **Rohde & Schwarz RTM3000 Oscilloscope**  
- **PC running EPICS**  
- **RS232-to-USB Adapter** *(if needed)*  

### **Software Dependencies**  
Ensure the following EPICS modules are installed:  
- **EPICS Base**  
- **Asyn** (for serial communication)  
- **StreamDevice** (for SCPI command handling)  

## **Installation & Setup**  
### **1. Clone the Repository**  
```bash
git clone https://github.com/1mbot/Oscilloscope-IOC.git
cd Oscilloscope-IOC
```

### **2. Set Environment Variables**  
Modify your `st.cmd` file with the correct **IOC path** and **serial port settings**:  
```bash
epicsEnvSet("IOC", "iocOscilloscope")
epicsEnvSet("TOP", "/path/to/Oscilloscope-IOC")
epicsEnvSet("EPICS_BASE", "/path/to/epics-base")
epicsEnvSet("ASYN", "/path/to/asyn")
epicsEnvSet("STREAM", "/path/to/StreamDevice")
drvAsynSerialPortConfigure("OSCILLOSCOPE", "/dev/ttyUSB0")
```

### **3. Build the IOC**  
```bash
make clean
make
```

### **4. Start the IOC**  
```bash
cd iocBoot/iocOscilloscope
./st.cmd
```

## **SCPI Command Integration**  
The **`oscilloscope.proto`** file maps SCPI commands to EPICS records.  

| EPICS PV Name | SCPI Command | Function |
|--------------|--------------|------------|
| `osc:idn` | `*IDN?` | Get oscilloscope identification |
| `osc:voltage` | `MEAS:VOLT:DC?` | Measure DC voltage |
| `osc:current` | `MEAS:CURR:DC?` | Measure DC current |
| `osc:frequency` | `MEAS:FREQ?` | Measure frequency |
| `osc:period` | `MEAS:PER?` | Measure period |
| `osc:trigger_mode` | `TRIG:MODE?` | Read trigger mode |
| `osc:trigger_level` | `TRIG:LEV?` | Set/get trigger level |
| `osc:waveform` | `WAV:DATA?` | Read waveform data |

## **Troubleshooting**  
### **1. Cannot Connect to Oscilloscope**
- Ensure the **RS232-to-USB adapter** is recognized using:  
  ```bash
  ls /dev/ttyUSB*
  ```
- Check if another process is using the serial port:  
  ```bash
  sudo fuser -v /dev/ttyUSB0
  ```

### **2. EPICS PVs Not Updating**
- Verify **Asyn and StreamDevice** are correctly installed.  
- Check the IOC log for **StreamDevice protocol errors**.  
- Ensure the correct **baud rate and serial settings** are configured.  

### **3. SCPI Commands Not Responding**
- Use a serial terminal like `screen` or `minicom` to manually test SCPI commands:  
  ```bash
  screen /dev/ttyUSB0 19200
  ```

## **Author & Contributions**  
Developed by **[1mbot](https://github.com/1mbot)**.  
