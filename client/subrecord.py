#!/usr/bin/env python
import subprocess
import numpy
import time
import os
import sys
import math

record_proc = subprocess.Popen(["arecord","-fS16_LE","-r8000","-c1","-traw"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

rate=math.floor(8000/100)

amp=numpy.zeros((80,))          #rate
th=numpy.zeros((80,))           #rate

f=open('testpy.raw','wb')
f.write(record_proc.stdout.read(1))
while 1:
    for i in range(0,79):                   #rate
        data=record_proc.stdout.read(2)
        a= ord(data[0])*256+ord(data[1])
        if a>32767:
            a=a-65536
        amp[i]=a
    amp = numpy.abs(amp)
    #@print('noise level:',amp.mean(),"\n")
##noise level evaluation endis
    noise = amp.mean()
    while 1:
        for i in range(0,79):               #rate
            data=record_proc.stdout.read(2)
            #record in buffer
            a= ord(data[0])*256+ord(data[1])
            if a>32767:
                a=a-65536
            amp[i]=a
        amp = numpy.abs(amp)
        #@print('noise level:',amp.mean(),';voice:',a)
        if amp.mean()>2.5*noise:
            print('start:noise:',noise,'voice:',amp.mean())
            #write buffer into file
            th=numpy.zeros((80))          #rate
            silent=0
##start capture voice
            while silent<300:    
                for i in range(0,79):       #rate
                    data=record_proc.stdout.read(2)
                    f.write(data)
                    a= ord(data[0])*256+ord(data[1])
                    if a>32767:
                        a=a-65536
                    th[i]=a
                th = numpy.abs(th)
                if th.mean()<3*noise:
                    #@print(silent,':noise:',noise,';','threshold:',th.mean())
                    noise=(noise+th.mean())/2
                    silent=silent+1
                else:
                    silent=0
            print('ends','noise:',noise,';th:',th.mean())
            break
        else:
            break
