# maava
My Attempt At Voice Assistant

highschool comp sci student's attempt at a hackable linux voice assistant that is aimed at beginner python programmers to make their own or just to use for fun.

# features

### super ez wakeword setting!
- in the 15th line, you are easily able to change the wakeword to anything you want, granted the speech recognizer gets it right.
- NO TRAINING MODELS!! Vosk is really awesome and i just use it for your wakeword to be recognized.
### custom voices!
- through the magic that is tts_with_rvc, you are easily able to use almost any voice you want
- slower with bigger responses however
### make ur own features + commands
- all commands are the elif statements that listen for the wakeword and whatever prompt is in there
- this does come with some caveats, however.
### premade commands 
- some media control commands are already made!
- this can help you get started on adding more commands and features!
### future features
- home assistant like features such as setting timers, telling stories, alarms, reminders, etc. 
- asking for weather
- have version a as a server
- computer vision
- chatbot??


# reqs
requires the following:

- linux x86 (tested on arch only)
- python 3.12
- torch??
- vosk
- ollama
- tts_with_rvc 
- sounddevice

# disclaimer
only has been tested on a pc with ryzen 7 5800x, rtx 3060 12G, and 32G ddr4 ram. i am unsure of the performance on other lower end devices but it is blazingly fast on my mid range pc. i am still learning about python (little to no knowledge on classes, generators, file management modules like numpy or pandas does) so this project will only get better as i have time (and discipline) to learn.
