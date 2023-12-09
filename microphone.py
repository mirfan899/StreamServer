import pyaudio
import asyncio
import websockets

# Recording parameters
format = pyaudio.paInt16
channels = 1
rate = 16000
chunk = 1048

# Websocket server address and port
websocket_server_address = 'localhost'
websocket_server_port = 8765


async def send_audio_to_websocket(recorded_data):
    async with websockets.connect(f'ws://{websocket_server_address}:{websocket_server_port}') as websocket:
        await websocket.send(recorded_data)
        print(await websocket.recv())
        recorded_data.clear()
        # await asyncio.sleep(0.2) # Sleep for 1 second before recording again


async def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    recorded_data = []

    while True:
        data = stream.read(chunk)
        recorded_data.append(data)

        if len(recorded_data) * chunk >= 2048 * 5: # Send data every n seconds
            await send_audio_to_websocket(recorded_data.copy())
            recorded_data.clear()


    stream.stop_stream()
    stream.close()
    p.terminate()


async def main():
    await asyncio.gather(record_audio())

asyncio.run(main())
