# SPDX-FileCopyrightText: 2003 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = Oscilloscope
# Oscilloscope.dbd will be created and installed
DBD += Oscilloscope.dbd

# Oscilloscope.dbd will be made up from these files:
Oscilloscope_DBD += base.dbd
Oscilloscope_DBD += asyn.dbd
Oscilloscope_DBD += stream.dbd
Oscilloscope_DBD += drvAsynIPPort.dbd

# Include dbd files from all support applications:
#Oscilloscope_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
Oscilloscope_LIBS += asyn
Oscilloscope_LIBS += stream

# Oscilloscope_registerRecordDeviceDriver.cpp derives from Oscilloscope.dbd
Oscilloscope_SRCS += Oscilloscope_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
Oscilloscope_SRCS_DEFAULT += OscilloscopeMain.cpp
Oscilloscope_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#Oscilloscope_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
Oscilloscope_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

