#!/usr/bin/env python3

import asyncio
import websockets
import sys
import wave


async def run_test(uri):
    async with websockets.connect(uri) as websocket:
        wf = wave.open("data/1.wav", "rb")
        await websocket.send('{"config" : { "max_alternatives" : 0, "sample_rate" : %d } }' % (wf.getframerate()))
        buffer_size = int(wf.getframerate() * 0.2) # 0.2 seconds of audio
        while True:
            data = wf.readframes(buffer_size)

            if len(data) == 0:
                break

            await websocket.send(data)
            print(await websocket.recv())

        await websocket.send('{"eof" : 1}')
        print(await websocket.recv())

asyncio.run(run_test('ws://0.0.0.0:2700'))
