#!/usr/bin/env python
import subprocess
import numpy as np
import time
import os
import sys
from datetime import datetime
import urllib2
from Queue import Queue,Empty
from threading import Thread

AMP_ADD_URL = 'http://edison-api.belugon.com/voiceAmpAdd?device=%s&timestamp=%f&amplitude=%d'
dev_id = 'position1'
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
        return 20*np.log10(s);


inrate=int(8000);
rate_str="-r"+str(inrate)
terminated = False
    
record_proc = subprocess.Popen(["arecord","-fS16_LE","-c1","-twav",rate_str],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

rate=int(inrate/1)

#th=numpy.zeros((rate,))
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

def send_result_queue(device_id, result_queue):
    with open('position3_00.txt','wb') as f:
        while not terminated:
            try:
                d = result_queue.get(timeout=1)
                request_url = AMP_ADD_URL % (device_id, d[0], d[1])
                Thread(target=async_req, args=[request_url]).start()
                #urllib2.urlopen(request_url)
                dt = datetime.utcfromtimestamp(d[0])
                print("%s,%d" % (str(dt),d[1]))
                f.write('%s,%d\n' % (str(dt),d[1]))
            except Empty:
                pass
    print("exit thread")

def async_req(url):
    urllib2.urlopen(url)

noisevector = np.zeros(5)
for i in range(0, 5):
    get_volume()
for i in range(0, 5):
    noisevector[i] = get_volume()
noise = noisevector.mean()
print("Offset noise: {}".format(noise))
amp_result_queue = Queue()
amp_result_thread = Thread(target=send_result_queue, args=[dev_id, amp_result_queue])
amp_result_thread.start()

try:
    while 1:
        v_lower = max((get_volume() - noise), 0)
        v = int(round(min(v_lower, 10) * 255 / 10))
        timestamp = time.time()
        amp_result_queue.put((timestamp, v))

        #f.write('\n')
except (KeyboardInterrupt, SystemExit):
    print("Terminating")
    terminated = True
    amp_result_thread.join()
    sys.exit()
