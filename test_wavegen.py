from WF_SDK import device, scope, wavegen, tools, error       # import instruments
import matplotlib.pyplot as plt

try:    # connect to device
    device_data = device.open()


    if device_data.name != "Digital Discovery":
        scope.open(device_data)

        # generate a 10KHz sine signal with 2V amplitude on channel 1
        wavegen.generate(device_data, channel=1, function=wavegen.function.sine, offset=0, frequency=10e03, amplitude=2)

        # record data with the scope channel 1
        buffer = scope.record(device_data, channel=1)
        
        # used to compute the spectrum (MHz)
        start_frequency = 0 
        stop_frequency = 100e03
        spectrum = tools.spectrum(buffer, tools.window.flat_top, scope.data.sampling_frequency, start_frequency, stop_frequency)

        # calculate how it changed over time
        frequency = []
        length = len(spectrum)
        step = (stop_frequency - start_frequency) / (length -1)
        for index in range(length):
            frequency.append((start_frequency + index * step) / 1e06)


# Display the data 
        plt.plot(frequency, spectrum)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Magnitude (dBv)')
        plt.legend()
        plt.show()

        
        # reset scope and wavegen
        scope.close(device_data)
        wavegen.close(device_data)
        
    device.close(device.data)

except error as e:
    print(e)
    device.close(device.data) # close device connection
