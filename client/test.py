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
    voice_capture_thread = Thread(target=subrecord.voice_capture, args=[math.floor(RECORD_KHZ * 1000), voice_data_queue])
    buf = bytearray(INPUT_BUF_SIZE)
    voice_capture_thread.start()
    while True:
        n = 0;
        data = voice_data_queue.get()
        if len(data) <= 3:
            print('got END')
        n = len(data)
        if n < len(buf):
            print('write short')
            f.write(data)
        else:
            print('write full')
            f.write(data)

