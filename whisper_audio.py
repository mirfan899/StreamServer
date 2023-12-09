import asyncio
import websockets


from pydub import AudioSegment
from pydub.utils import make_chunks

myaudio = AudioSegment.from_file('data/1.wav', format="wav")
# Make chunks of 2 sec
chunk_length_ms = 2000
chunks = make_chunks(myaudio, chunk_length_ms)
for i, chunk in enumerate(chunks):
    chunk_name = '{0}-chunk.wav'.format(i)
    chunk.export(chunk_name, format='wav')


async def run_test(uri):
    async with websockets.connect(uri) as websocket:
        for i, chunk in enumerate(chunks):
            await websocket.send(chunk.raw_data)
            x = await websocket.recv()
            print(x)
        await websocket.close()


asyncio.run(run_test('ws://0.0.0.0:5000'))
