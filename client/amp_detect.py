#!/usr/bin/env python
import subprocess
import numpy
import time
import os
import sys

inrate=int(8000);
rate_str="-r"+str(inrate)
    
record_proc = subprocess.Popen(["arecord","-fS16_LE","-c1","-traw",rate_str],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

rate=int(inrate/1)

noise=80
open_factor=2.5
gaussain_filter=[0.006,0.061,0.242,0.383,0.242,0.061,0.006]

amp=numpy.zeros((rate,))
#th=numpy.zeros((rate,))
f=open('test4.txt','wb')
#f.write(record_proc.stdout.read(1))
for i in range(0,rate-1):
    data = record_proc.stdout.read(2)
    a = ord(data[0])+ord(data[1])*256
    if a > 32767:
        a = a-65536
    amp[i]=a
amp = numpy.abs(amp)
amp = numpy.convolve(amp,gaussain_filter,'same')
noise = amp.mean()
while 1:
    for i in range(0,rate-1):
        data = record_proc.stdout.read(2)
        a = ord(data[0])+ord(data[1])*256
        if a > 32767:
            a = a-65536
        amp[i] = a
    amp = numpy.abs(amp)
    amp = numpy.convolve(amp,gaussain_filter,'same')
    print("voice{}".format(amp.mean()))
    f.write('%.2f' % amp.mean())
    f.write('\n')
