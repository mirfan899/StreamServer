import pyaudio
import time
import asyncio
import websockets

# Recording parameters
format = pyaudio.paInt16
channels = 1
rate = 16000
chunk = 1024

# Websocket server address and port
websocket_server_address = 'localhost'
websocket_server_port = 8765

# Duration
record_seconds = 5

p = pyaudio.PyAudio()


async def send_audio_to_websocket(recorded_data):
    async with websockets.connect(f'ws://{websocket_server_address}:{websocket_server_port}') as websocket:
        await websocket.send(recorded_data)
        print(await websocket.recv())


async def main():
    print(f"Start recording for {record_seconds} seconds....")
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    recorded_data = []
    start_time = time.time()

    while time.time() - start_time < record_seconds:
        data = stream.read(chunk)
        recorded_data.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    await send_audio_to_websocket(recorded_data)

asyncio.run(main())
