#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import websockets
import logging
import sounddevice as sd
import queue

from vosk import Model, KaldiRecognizer

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

async def serve_client(websocket):
    clients.add(websocket)
    print ("Client connected from", websocket)
    await websocket.wait_closed()
    clients.remove(websocket)

async def recognize_microphone():
    global audio_queue

    model = Model(r'vosk-model-small-en-us-0.15')
    audio_queue = asyncio.Queue()
    
    with sd.RawInputStream(samplerate=44000, blocksize = 2000, device='pulse', dtype='int16',
                            channels=1, callback=callback) as device:

        logging.info("Running recognition")
        rec = KaldiRecognizer(model, device.samplerate)
        while True:
            data = await audio_queue.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                logging.info(result)
                websockets.broadcast(clients, result)

async def main():

    global args
    global clients
    global loop
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_running_loop()
    clients = set()

    logging.info("Listening on %s:%d", '192.168.0.13', 2700)

    await asyncio.gather(
        websockets.serve(serve_client, '192.168.0.13', 2700),
                         recognize_microphone())

if __name__ == '__main__':
    asyncio.run(main())
