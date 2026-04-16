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
wakeword = 'computer'
agentname = 'ava'
############## WAKE WORD ###################
print(sd.query_devices())
try:
    devid = 'pulse'
except:
    devid = 'default'
q = queue.Queue()
model = Model(r"vosk-model-en-us-0.42-gigaspeech")
tts = TTS_RVC(model_path="model.pth",
              index_path="model.index",
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
    os.system("paplay temp/final.wav &")

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
    model = Model(r"vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model, 8000)
    
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))
    

    with sd.RawInputStream(samplerate=16000, blocksize = 8000, device=devid,dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            anything = False # change this to have a convo with the ai or dont [as]
            if rec.AcceptWaveform(data):
                result = rec.Result()
                cleanresult = result[14:-3]
                print(cleanresult)
                print(cleanresult[0:-4])
                print(f' result is {len(cleanresult)}')
                print(f' wakeword is {len(wakeword)}')
                if 'alexa' in result:
                    say(f'who are you calling alexa? my name is {agentname} and I will only respond to {wakeword}')
                if wakeword in result:
                    if f'{wakeword} stop' in result: 
                        command('playerctl pause &')
                        try:
                            command('kill $(pgrep -f timer.py)')
                        except:
                            pass
                    elif f'{wakeword} play' in result:
                        if 'music' in result:
                            command('spotify-launcher &')
                            say('playing music')
                            es = os.system('playerctl play &')
                        else:
                            command('playerctl play &')

                    elif f'{wakeword} what time is it' in result:
                        gettime()
                    elif f"{wakeword} what's the time" in result:
                        gettime()
                    elif f'{wakeword} what is the time' in result:
                        gettime()
                    elif f'{wakeword} resume' in result:
                        command('playerctl play &')
                    elif f'{wakeword} what is the weather in' in result:
                        weath_req = (f'{cleanresult.split('what is the')[1]}')
                        print(weath_req)
                        sp.check_output([f'python3 TOOLS/weather.py --prompt "{weath_req}"'], shell=True, text=True)
                        say(f'the {weath_req} is {temp}degrees fahrenheit')
                        time.sleep(5)
                    elif f'{wakeword} set a timer for' in result:
                        command(f'python TOOLS/timer.py --prompt "{cleanresult}" &')
                                        ### DONT EDIT THIS UNDER PLS ###
                    elif wakeword in cleanresult:
                        if len(wakeword) == len(cleanresult):
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
                    pass
            else:
                print(rec.PartialResult())
                pass


############# MAIN LOOP #######################

def gotoai(x):
    response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': f'{x}',
  },
])  
    command('clear')
    final = response.message.content
    print(final)
    say(final)


x = False
while True:
    if x == False:
        say(f'test')
    else:
        pass
    main()
