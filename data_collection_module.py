import sys
import numpy
import pylab
import matplotlib
import matplotlib.pyplot as plt
import visa	
import decimal
#visa.log_to_screen()

### edit these lines they are the only thing that cannot be pulled from the spectrum analyzer###
file_name = 'mackenzie_20170717_50000x2c_bandwidth.txt' #names file 
freq_data = 'mackenzie_20170717_50000x2c_bandwidth_freqdata.txt' 
notes = 'cascode detector w/ the cascode in place. looking at bandwidth now, using a power of 1000 uW.'
lsr_pwr = str(1000) #put laser power in uW here
trans = str(.9) #put transmission percent here
###

rm = visa.ResourceManager() #produces list of devices attached to computer
device = ',' .join(rm.list_resources()) #assumes that the only device plugged in is the spectrum analyzer and pulls it out of the list as a sting
spec_analyzer = rm.open_resource(device, write_termination = '\n', read_termination = '\n') 
spec_analyzer.timeout = 10000 
print(spec_analyzer.query('*IDN?')) #makes sure that we are connected to an actual device

#might implement check here? make device selection more elegant. 

start_freq = spec_analyzer.query('SENS:FREQ:STAR?')
stop_freq = spec_analyzer.query('SENS:FREQ:STOP?')
rbw = spec_analyzer.query('SENS:BAND:RES?')
vbw = spec_analyzer.query('SENS:BAND:VID?')
swt = spec_analyzer.query('SENS:SWE:TIME?')
input_attn = spec_analyzer.query('SENS:POW:ATT?')

f = open(file_name, 'w') #cretes & opens file
f.write(notes + '\n')
f.write('start frequency=' + start_freq + ' Hz' + '\n')
f.write('stop frequency=' + stop_freq + ' Hz' + '\n')
f.write('RBW=' + rbw + ' Hz' + '\n')
f.write('VBW=' + vbw + ' Hz' + '\n')
f.write('SWT=' + swt + ' s' + '\n')
f.write('laser power=' + lsr_pwr + ' uW' + '\n')
f.write('transmission=' + trans + '\n')
f.write('input attenuation=' + input_attn + ' dB')
f.close() 

spec_analyzer.write('init:cont OFF') #turns data collection off so that values can be taken
print(spec_analyzer.query('*OPC?')) #opc checks if prev command completed, returns 1 if yes

spec_analyzer.write('TRAC? TRACE1') #pulls data off of the analyzer
rawData = spec_analyzer.read_raw() 
print(spec_analyzer.query('*OPC?'))
a = len(rawData)

rawData = rawData.split()
rawData = rawData[1:a]	

Data=[]
for i in rawData:
	i = str(i)
	for char in '\'b,':
		i = i.replace(char, '')
	Data.append(i)

myData = []
for x in Data:
	y = float(x)
	myData.append(y)
tot_points = len(myData)

freq = numpy.linspace(int(start_freq), int(stop_freq), int(tot_points))

noise_data = file_name[:-4] + '_noisedata.txt'
f = open(noise_data, 'w')
for x in myData:				#added this loop so it lists properly & interacts w/ mathematica
	f.write(str(x) + '\n')
f.close()

f = open(freq_data, 'w')
for x in freq:					#same loop as before
	f.write(str(x) +'\n')
f.close()

spec_analyzer.write('init:cont ON') #turns the spectrum analyzer back on
print(spec_analyzer.query('*OPC?'))