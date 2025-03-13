#!../../bin/linux-x86_64/Oscilloscope

#- SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#-
#- SPDX-License-Identifier: EPICS

#- You may have to change Oscilloscope to something else
#- everywhere it appears in this file

< envPaths
epicsEnvSet("IOC","iocOscilloscope")
epicsEnvSet("TOP","/home/tifr/Self_IOC/Oscilloscope")
epicsEnvSet("EPICS_BASE","/home/tifr/EPICS/epics-base")
epicsEnvSet("ASYN", "/home/tifr/EPICS/support/asyn")
epicsEnvSet("STREAM", "/home/tifr/EPICS/support/stream/StreamDevice")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")
cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/Oscilloscope.dbd"
Oscilloscope_registerRecordDeviceDriver pdbbase
drvAsynSerialPortConfigure("OSCILLOSCOPE", "/dev/ttyUSB0")
dbLoadRecords("db/oscilloscope.db", "PORT = OSCILLOSCOPE")
## Load record instances
#dbLoadRecords("db/Oscilloscope.db","user=tifr")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=tifr"
