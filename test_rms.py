from WF_SDK import device, scope, wavegen, tools # import the devices instruments
import matplotlib.pyplot as plt # import plotting tool
from math import sqrt # used to calculate the rms (root mean square)
from time import sleep # needed for delays

# connect to the device
device_data = device.open()

# variables that can be changed
amplitude = 1
offset = 0.0

# array consisting of different frequencies
freq = [100e01, 200e01, 300e01, 400e01, 500e01, 
        100e02, 200e02, 300e02, 400e02, 500e02, 
        100e03, 200e03, 300e03, 400e03, 500e03, 
        100e04, 200e04, 300e04, 400e04, 500e04, 
        100e05, 200e05, 500e05, 100e06, 200e06
        ]

average = [] # will be used to store rms values of different buffers

def wave_iterations(average):
    scope.open(device_data) # initialize scope 

    for index, value in enumerate(freq):

        sleep(0.1) # wait for offset to stabilize after previous iteration

        # set up trigger on scope channel 1
        scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=1, level=0)

        # generate a sine signal with set amplitude on channel 1
        wavegen.generate(device_data, channel=1, function=wavegen.function.sine, offset=offset, frequency=value, amplitude=amplitude)
        
        # record data with the scopeon channel 1
        buffer = scope.record(device_data, channel=1)
        
        # generate buffer for time moments
        time = []
        for indx in range(len(buffer)):
            time.append(indx * 10e03 / scope.data.sampling_frequency) # converting time - ms

        '''
        # plot
        plt.plot(time, buffer)
        plt.xlabel("time [ms]")
        plt.ylabel("voltage [V]")
        plt.show()
        '''

        buff_val_rms = [] # store rms of all buffer values

        # raising all values in the buffer to the power of 2 
        for x in buffer:
            buff_val_rms.append(sqrt((x**2) / len(time)))

        mean = (sum(buff_val_rms) / len(buff_val_rms))
        #print(mean)

        average.append(mean) # appending rms to a list so the mean of all results can be found

        # decide to pereform more iterations or not
        '''
        end = input('continue iterations? (y/n)')

        if end == 'n':
            return average # returns all rms values of all iterations performed

        else:
            print('iteration:',index +1) # keeping track of iteration number
            pass
        '''
        
        print('iteration:',index +1) # keeping track of iteration number
    return average # returns all rms values collected


wave_iterations(average) # starting iterations

mean = (sum(average) / len(average)) # calculating mean

plt.plot(average)
plt.xlabel('Points')
plt.ylabel('dB')
plt.show()

print('mean:',mean, '\nmean (2dp):', round(mean,2)) # display mean 



# reset scope and wavegen
scope.close(device_data)
wavegen.close(device_data)

# close device
device.close(device.data)