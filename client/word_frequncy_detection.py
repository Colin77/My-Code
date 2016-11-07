from os import path
import speech_recognition as sr
import subprocess
import threading as Thread
import Queue import Queue, Empty
import subrecord
import sys

INTERVAL = 7000 #7s
RECORD_KHZ = 8
INPUT_BUF_SIZE = (INTERVAL / 1000) * RECORD_KHZ * 1000 * 16 / 8

def main():
    if len(sys.argv) != 2:
        print("Please type in at exactly one word for detection")
        sys.exit(0)
    else:
        word_frequency_detection(sys.argv[1])


def word_frequency_detection(word_to_detect):
    TOTAL_WORD_COUNT = 0  #Count the number of appreance in the text
    voice_data_queue = Queue()
    #Acquire voice clip for speech detection
    voice_capture_thread = Thread(target=subrecord.voice_capture, args=[math.floor(RECORD_KHZ *1000), INPUT_BUF_SIZE, voice_data_queue])
    voice_capture_thread.start()


    while True:
        speech.wav = voice_data_queue.get()
        WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "speech.wav")

        r = sr.Recognizer()

        with sr.WavFile(WAV_FILE) as source:
            audio = r.record(source)
        try:
            result_text = r.recognize_google(audio) #result_text is a string
            print(result_text)
            #convert string to list 
            result_list = result_text.split()
            #word frequency counting
            for word in result_list:
                if word == word_to_detect:
                    TOTAL_WORD_COUNT += 1
            print("Has appreared %d times", TOTAL_WORD_COUNT) 
        except sr.UnknownValueError:
            print("Google Speech Reconition could not uderstand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


