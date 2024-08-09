from WF_SDK import device # device instruments

#import matplotlib.pyplot as plt #### could be needed for plotting

#from time import sleep ### could be needed for delays

#import math ### could be needed for calculations


device_data = device.open() # connecting to the device
#scope.open(device_data) #initialize the scope

'''-----function to set up device and send signals-----

    sets up trigger on channel 1 of the connected device
    ### scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=1, level=0)
    
    used to generate a sine signal on channel 1
    ### wavegen.generate(device_data, channel=1, function=wavegen.function.sine, offset=0, frequency=10e03, amplitude=2)
    
    record the data on scopean channel 1
    ### buffer = scope.record(device_data, channel=1)'''

'''-----Write main program here-----'''










'''-----Closing/resetting instruments used-----'''

#scope.close(device_data)
#wavegen.close(device_data)

# close device
device.close(device.data)