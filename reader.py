import numpy as np
import librosa
import logging
from typing import Iterator
import asyncio

logger = logging.getLogger(__name__)

def process_wav_file(wav_file_path: str, 
                     target_sr: int = 8000, 
                     chunk_ms: int = 40) -> Iterator[bytes]:
    """
    Read a WAV file, resample to 8kHz if needed, and yield 40ms audio chunks as raw PCM bytes.
    
    Args:
        wav_file_path: Path to WAV file
        target_sr: Target sample rate in Hz (default: 8000)
        chunk_ms: Size of audio chunks in milliseconds (default: 40)
        
    Yields:
        Raw PCM bytes of audio data in 40ms chunks (16-bit PCM)
    """
    logger.info(f"Processing WAV file: {wav_file_path}")
    
    # Load audio file with librosa
    try:
        audio_data, original_sr = librosa.load(wav_file_path, sr=None, mono=True)
        logger.info(f"Loaded audio with sample rate: {original_sr}Hz")
        
        # Resample if necessary
        if original_sr != target_sr:
            logger.info(f"Resampling from {original_sr}Hz to {target_sr}Hz")
            audio_data = librosa.resample(audio_data, orig_sr=original_sr, target_sr=target_sr)
        
        # Calculate samples per chunk (40ms at 8kHz = 320 samples)
        samples_per_chunk = int(target_sr * chunk_ms / 1000)
        logger.info(f"Chunk size: {chunk_ms}ms = {samples_per_chunk} samples")
        
        # Convert to 16-bit PCM
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Yield chunks
        total_chunks = 0
        for i in range(0, len(audio_int16), samples_per_chunk):
            chunk = audio_int16[i:i+samples_per_chunk]
            
            # If last chunk is partial, pad with zeros
            if len(chunk) < samples_per_chunk:
                chunk = np.pad(chunk, (0, samples_per_chunk - len(chunk)))
                
            # Convert to raw PCM bytes (16-bit)
            chunk_bytes = chunk.tobytes()
            yield chunk_bytes
            total_chunks += 1
            
        logger.info(f"Audio processing complete. Generated {total_chunks} chunks")
            
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise
    
async def read_audio(audio_input_queue: asyncio.Queue, fpath:str):
    for chunk in process_wav_file(fpath):
        await audio_input_queue.put(chunk)
    logger.info("Finished reading audio file, signaling end of input.")
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    audio_queue = asyncio.Queue()
    asyncio.run(read_audio(audio_queue, "recording.wav"))