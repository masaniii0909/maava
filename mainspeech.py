import queue
import sys
import os
from tts_with_rvc import TTS_RVC
import sounddevice as sd
import wave
from vosk import Model, KaldiRecognizer
import threading 
from ollama import chat
from ollama import ChatResponse
import random
import time
import subprocess as sp
############## WAKE WORD ###################
wakeword = 'hey computer'
############## WAKE WORD ###################
devid = 'default'
q = queue.Queue()
model = Model(r"vosk-model-small-en-us-0.15")
tts = TTS_RVC(model_path="urmodel.pth",
              index_path="urindex.index",
              f0_method="rmvpe")
tts.set_voice("en-US-JennyNeural") #FEMALE
#tts.set_voice("en-US-BrianNeural") #MALE


        ############################
        ##### MAIN THINGAMAGIG #####
        ############################

def command(x):
    try:
        os.system(x)
    except: 
        print('###################FAILED#####################')
        pass
def say(x):
    text = x
    path = tts(text=text,
            pitch=2,
            tts_rate=12,
            output_filename="final.wav")
    os.system("paplay ~/py-tests/tts-rvc/temp/final.wav &")

def gettime():
    hour = sp.check_output(["date +%I"], shell=True, text=True)
    min = sp.check_output(["date +%M"], shell=True, text=True)
    if '0' in hour:
        hour = hour[1]
    elif min == '00':
        min = 'o clock'
    else:
        pass
    print(hour + min)
    say(f'The current time is {hour} {min}')

def main():
    q = queue.Queue()
    model = Model(lang="en-us")
    rec = KaldiRecognizer(model, 8000)
    
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))
    

    with sd.RawInputStream(samplerate=16000, blocksize = 8000, device=devid,dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, 16000)
        dosm = False
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                cleanresult = result[14:-3]
                print(cleanresult)
                if wakeword in result:
                    cleanresult = cleanresult[(int(len(wakeword))):-3]
                    print(cleanresult)
                    print(((int(len(wakeword))) + (int(len(result))) - 11))
                    if f'{wakeword} stop' in result: 
                        command('playerctl pause &')
                    elif f'{wakeword} play' in result:
                        command('playerctl play &')
                    elif f'{wakeword} what time is it' in result:
                        gettime()
                    elif f"{wakeword} what's the time" in result:
                        gettime()
                    elif f'{wakeword} what is the time' in result:
                        gettime()
                    elif f'{wakeword} pause' in result:
                        command('playerctl pause &')
                    elif f'{wakeword} resume' in result:
                        command('playerctl play &')
                    ### DONT EDIT THIS UNDER PLS ###
                    elif wakeword in cleanresult and len(wakeword) == len(cleanresult):
                        response = random.randrange(1,5,1)
                        print(len(result))
                        if response == 1:
                            say("Yo!")
                        if response == 2:
                            say("Hey!")
                        if response == 3:
                            say("Hello to you too!")
                        if response == 4:
                            say("Hello!")
                        if response == 5:
                            say("Hiii!")
                        else:
                            pass
                    elif len(cleanresult) > len(wakeword):
                        print(result)
                        response = random.randrange(1,5,1)
                        if response == 1:
                            say("Im not sure I understand!")
                        if response == 2:
                            say("What?")
                        if response == 3:
                            say("Im unsure of what to do")
                        if response == 4:
                            say("Im sorry?")
                        if response == 5:
                            say("I don't know what you said")
                        else:
                            pass
                    else: 
                        pass
            else:
                print(rec.PartialResult())
                pass


############# MAIN LOOP #######################

def gotoai(x):
    response: ChatResponse = chat(model='gemma2:2b', messages=[
  {
    'role': 'user',
    'content': f'{x} (DO NOT USE EMOJIS, RESPOND IN NO LONGER THAN 3 SETENCES, IF THE QUESTION IS MORE COMPLICATED THEN YOU CAN, TRY TO KEEP IT SHORT!!)',
  },
])  
    command('clear')
    final = response.message.content
    print(final)
    say(final)


x = False
while True:
    if x == False:
        say(f'System online. Say {wakeword} before all commands')
    else:
        pass
    main()

    
    
