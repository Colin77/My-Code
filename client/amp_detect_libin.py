#!/usr/bin/env python
import subprocess
import numpy as np
import time
import os
import sys

gaussain_filter=[0.006,0.061,0.242,0.383,0.242,0.061,0.006]
class RingFilter():
    def __init__(self):
        self.data = np.zeros(7, dtype='f')
        self.index = 0

    def roll(self, x):
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def filter(self, filt):
        s = 0
        for i in range(0,7):
            x_index = (self.index + (7 - i)) % 7
            s += self.data[x_index] * filt[i]
        return s;


inrate=int(8000);
rate_str="-r"+str(inrate)
    
record_proc = subprocess.Popen(["arecord","-fS16_LE","-c1","-twav",rate_str],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

rate=int(inrate/1)

#th=numpy.zeros((rate,))
f=open('test1.txt','wb')
#f.write(record_proc.stdout.read(1))

ring_filter = RingFilter()
def get_volume():
    amp = np.zeros(rate)
    for i in range(0,rate/5 - 1):
        data = record_proc.stdout.read(2)
        a = ord(data[0])+ord(data[1])*256
        if a > 32767:
            a = a-65536
        amp[i] = a
    amp = np.abs(amp)
    vol = amp.mean()
    ring_filter.roll(vol)
    return ring_filter.filter(gaussain_filter)

noisevector = np.zeros(5)
for i in range(0, 5):
    get_volume()
for i in range(0, 5):
    noisevector[i] = get_volume()
noise = noisevector.mean()
print("Offset noise: {}".format(noise))

while 1:
    v_lower = max((get_volume() - noise), 0)
    v = int(round(min(v_lower, 100) * 255 / 100))
    print("voice{}".format(v))
    #f.write('%.2f' % amp.mean())
    #f.write('\n')
