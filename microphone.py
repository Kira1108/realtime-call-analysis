import asyncio
import pyaudio
import json


class MicrophoneClient:
    def __init__(self,
        audio_input_queue: asyncio.Queue = None,
        sampling_rate: int = 8000, 
        chunk_ms: int = 40, 
        channels: int = 1):
        
        self.audio_input_queue = audio_input_queue if audio_input_queue is not None else asyncio.Queue()
        self.sampling_rate = sampling_rate
        self.chunk_size = int(sampling_rate * (chunk_ms / 1000))
        self.channels = channels
            
        self.port_audio = pyaudio.PyAudio()
        self.stream = self.port_audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sampling_rate,
            input=True,
            frames_per_buffer=self.chunk_size)
        print("Initialization down, stream opened")
        
    async def record(self):
        print("Starting to send audio")
        while self.stream.is_active():

            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            await self.audio_input_queue.put(data)
            await asyncio.sleep(0.01)
        await self.audio_input_queue.put(json.dumps({"type": "end"}))
        
        
            
        