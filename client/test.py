#!/usr/bin/env python
from threading import Thread
from Queue import Queue, Empty
import subrecord
import math
import io

RECORD_KHZ = 8
INPUT_BUF_SIZE = RECORD_KHZ * 1000 * 16 / 8 # 8kHz 16 bit
with open('test.raw', 'wb') as f:
    voice_data_queue = Queue()
    voice_capture_thread = Thread(target=subrecord.voice_capture, args=[math.floor(RECORD_KHZ * 1000), INPUT_BUF_SIZE, voice_data_queue])
    voice_capture_thread.start()
    while True:
        data = voice_data_queue.get()
        n = len(data)
        if n < len(data):
            print('write short')
            f.write(data)
        else:
            print('write full')
            f.write(data)

