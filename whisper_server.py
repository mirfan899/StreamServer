import asyncio
import websockets
import faster_whisper

from pydub import AudioSegment
model = faster_whisper.WhisperModel("base.en", device="cpu", compute_type="int8")


def convert_raw2float(byte):
    if isinstance(byte, str):
        return byte
    elif isinstance(byte, bytes):
        chunk_name = 'data/chunk.wav'
        x = AudioSegment(byte, sample_width=2, channels=1, frame_rate=16000)
        x.export(chunk_name, format="wav")
        return chunk_name


async def handle_connection(websocket: websockets.WebSocketClientProtocol):
    """
    Handles new connections and sends initial messages before starting transcription.

    Args:
      websocket: The websocket connection to the client.
    """

    # Process audio chunks received from client
    async for audio_chunk in websocket:
        # Transcribe audio chunk
        print("transcribing......")
        x = convert_raw2float(audio_chunk)
        segments, info = model.transcribe(x, beam_size=5, vad_filter=True)
        text = list(segments)
        out = ""
        for t in text:
            out += t.text
        await websocket.send(out)


async def start_server():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("Server started on ws://0.0.0.0:8765")
        await asyncio.Future()


# Run server
if __name__ == "__main__":
    asyncio.run(start_server())
