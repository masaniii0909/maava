import queue
import sys
import os
from tts_with_rvc import TTS_RVC
import sounddevice as sd
from ollama import chat, ChatResponse
import random
from word2number import w2n
import subprocess as sp
import websockets
import asyncio
############## WAKE WORD ###################
wakeword = 'morgan'
agentname = 'morgan'
############## WAKE WORD ###################
print(sd.query_devices())
try:
    devid = 'pulse'
except:
    devid = 'default'
q = queue.Queue()
tts = TTS_RVC(model_path="model.pth",
              index_path="model.index",
              f0_method="rmvpe")
#tts.set_voice("en-US-JennyNeural") #FEMALE
tts.set_voice("en-US-BrianNeural") #MALE


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
            pitch=-6,
            tts_rate=-2,
            output_filename="final.wav")
    os.system("paplay temp/final.wav ")
def set_volume(x):
    command(f'pactl set-sink-volume $(pactl get-default-sink) {x}%')
    

def gettime():
    hour = sp.check_output(["date +%I"], shell=True, text=True)
    min = sp.check_output(["date +%M"], shell=True, text=True)
    if min == '00':
        min = 'o clock'
    else:
        pass
    print(hour + min)
    say(f'The current time is {hour} {min}')

async def listen(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            print(await websocket.recv())

def main():
    result = websocket.recv()
    cleanresult = result[14:-3]
    print(cleanresult)
    print(cleanresult[0:-4])
    print(f' result is {len(cleanresult)}')
    print(f' wakeword is {len(wakeword)}')
    if 'alexa' in result:
        say(f'Who is this, Alexa, you speak of. My name is {agentname} and I will only respond to {wakeword}')
    if wakeword in result:
# MUSIC AND PLAYBACK
        if ' stop' in result: 
            command('playerctl pause &')
            try:
                command('kill $(pgrep -f timer.py)')
            except:
                pass
        elif ' play' in result:
            if 'music' in result:
                command('spotify-launcher &')
                say('playing music')
                es = os.system('playerctl play &')
            else:
                command('playerctl play &')
        elif ' resume' in result:
            command('playerctl play &')
        elif ' skip' in result:
            command('playerctl next &')
        elif ' rewind' in result:
            command('playerctl previous &')
        elif ' previous song' in result or ' previous' in result:
            command('playerctl previous &')
            command('playerctl previous &')
        elif ' volume' in result or ' set volume' in result:
            set_volume(w2n.word_to_num(cleanresult.split('volume')[1]))
# IF WAKEWORD + WHAT or WHAT'S
        elif ' what' in result:
# TIME
            if 'time is it' in result:
                gettime()
            elif 'what is' in result or f"{wakeword} what's": # what is or what's
                if 'the' in result:                           #         the
                    if 'time' in result:                      #         time
                        gettime()
# WEATHE
                    elif 'weather' in result:                 # what is the weather / what's the weather
                        weath_req = (f'{cleanresult.split('what is the ')[1]}')
                        print(weath_req)
                        temp = sp.check_output([f'python3 TOOLS/weather.py --prompt "{weath_req}"'], shell=True, text=True)
                        say(f'the {weath_req} is {temp} degrees fahrenheit')
# SEARCH
                    elif ' name of' in result:
                        if 'name of this song' in result:
                            say('idk gang')
                        else:
                            search(cleanresult.split(f'{wakeword}')[1])
                    else:                                    
                        print(cleanresult.split(f'{wakeword}')[1])  # what is the / what's the ____
                        search(cleanresult.split(f'{wakeword}')[1])
# MATH
                elif 'times' in result or 'plus' in result or 'divided by' in result or 'minus' in result:
                    gotoai(cleanresult, "dont explain the answer")
                elif ' your purpose' in result:
                    say("my purpose is to help you")
                else:
                    search(cleanresult.split(f'{wakeword}')[1])
# WHAT D
            elif ' do' in result:
                search(cleanresult.split(f'{wakeword}')[1])
                            
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
        pass


############# MAIN LOOP #######################

def gotoai(x, y):
    response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
            'content': f'{x}. ({y})',
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
    asyncio.run(listen('ws://192.168.0.13:2700'))
    main()  
