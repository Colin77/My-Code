#!/usr/bin/env python
import subprocess
import numpy
import time
import os
import sys
import Queue
import io

def voice_capture(inrate, v_queue):

    inrate=int(8000);
    rate_str="-r"+str(inrate)
    byte_buffer=bytearray(16000)
    j=0
    record_proc = subprocess.Popen(["arecord","-fS16_LE",rate_str,"-c1","-traw"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    rate=int(inrate/100)
    
    open_factor=2.5

    amp=numpy.zeros((rate,))          #rate
    th=numpy.zeros((rate,))           #rate
    
    f=open('testpy.raw','wb')
    #f.write(record_proc.stdout.read(1))
    while 1:
        for i in range(0,rate-1):                   #rate
            data=record_proc.stdout.read(2)
            a= ord(data[0])+ord(data[1])*256
            if a>32767:
                a=a-65536
            amp[i]=a
        amp = numpy.abs(amp)
        #@print('noise level:',amp.mean(),"\n")
    ##noise level evaluation endis
        noise = amp.mean()
        while 1:
            for i in range(0,rate-1):               #rate
                data=record_proc.stdout.read(2)
                #record in buffer
                a= ord(data[0])+ord(data[1])*256
                if a>32767:
                    a=a-65536
                amp[i]=a
            amp = numpy.abs(amp)
            #@print('noise level:',amp.mean(),';voice:',a)
            if amp.mean()>open_factor*noise:                  #threshold
                print('start:noise:',noise,'voice:',amp.mean())
                #write buffer into file
                th=numpy.zeros((rate,))          #rate
                silent=0
    ##start capture voice
                while silent<300:    
                    for i in range(0,rate-1):       #rate
                        data=record_proc.stdout.read(2)
                        byte_buffer[j]=data[0]    #v_queue.write(data) #v_queue.put(data)           #f.write(data)
                        byte_buffer[j+1]=data[1]
                        j=j+2
                        if (j>=16000):
                            j=0
                            v_queue.put(byte_buffer)
                        a= ord(data[0])+ord(data[1])*256
                        if a>32767:
                            a=a-65536
                        th[i]=a
                    th = numpy.abs(th)
                    if th.mean()<(open_factor+1)*noise:           #threshold
                        #@print(silent,':noise:',noise,';','threshold:',th.mean())
                        noise=(noise+th.mean())/2
                        silent=silent+1
                    else:
                        silent=0
                print('ends','noise:',noise,';th:',th.mean())
                j=0
                v_queue.put('END')
                break
            else:
                break
