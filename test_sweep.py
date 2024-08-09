from ctypes import *
import time
from WF_SDK import wavegen, dwfconstants as consts, error
import sys
import matplotlib.pyplot as plt
import numpy as np
np.float = float

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

# continue running after device close, prevent temperature drifts
dwf.FDwfParamSet(consts.DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown

#print(DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

#open device
hdwf = c_int()
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == consts.hdwfNone.value:
    print("failed to open device")
    quit()

# the device will only be configured when FDwf###Configure is called
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) 

hzStart = 1e3
hzStop = 20e3
hzMid = (hzStart+hzStop)/5
secSweep = 5e-3
channel = c_int(0)

dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, consts.AnalogOutNodeCarrier, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, consts.AnalogOutNodeCarrier, wavegen.function.sine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, consts.AnalogOutNodeCarrier, c_double(hzMid))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, consts.AnalogOutNodeCarrier, c_double(1.0))
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, consts.AnalogOutNodeCarrier, c_double(0.0))

dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, consts.AnalogOutNodeFM, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, consts.AnalogOutNodeFM, wavegen.function.ramp_up)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, consts.AnalogOutNodeFM, c_double(1.0/secSweep))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, consts.AnalogOutNodeFM, c_double(100.0*(hzStop-hzMid)/hzMid))
dwf.FDwfAnalogOutNodeSymmetrySet(hdwf, channel, consts.AnalogOutNodeFM, c_double(100.0))

dwf.FDwfAnalogOutRunSet(hdwf, channel, c_double(secSweep))
dwf.FDwfAnalogOutRepeatSet(hdwf, channel, c_int(1))


hzRate = 1e6 
cSamples = 8*1024
rgdSamples1 = (c_double*cSamples)()
rgdSamples2 = (c_double*cSamples)()
sts = c_int()

print("Configure analog in")
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzRate))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(4))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(cSamples))
dwf.FDwfAnalogInTriggerSourceSet(hdwf, consts.trigsrcAnalogOut1) 
dwf.FDwfAnalogInTriggerPositionSet(hdwf, c_double(0.3*cSamples/hzRate)) # trigger position at 20%, 0.5-0.3

print("Starting acquisition...")
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))

while True:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    if sts.value == consts.DwfStateArmed.value :
        break
    time.sleep(0.1)
print("   armed")

time.sleep(2.0) # wait for the offsets to stabilize

dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))

while True:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    if sts.value == consts.DwfStateDone.value :
        break
    time.sleep(0.1)
print("   done")

dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rgdSamples1, len(rgdSamples1)) # get channel 1 data
dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rgdSamples2, len(rgdSamples2)) # get channel 2 data


dwf.FDwfDeviceCloseAll()

plt.plot(np.linspace(0, cSamples-1, cSamples), np.fromiter(rgdSamples1, dtype = np.float), np.linspace(0, cSamples-1, cSamples), np.fromiter(rgdSamples2, dtype = np.float))
plt.show()