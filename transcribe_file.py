import asyncio
import json
import logging
from pathlib import Path
import argparse

from reader import process_wav_file
from asr import TencentASR

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def transcribe_audio_file(file_path: str):
    """
    Transcribe an audio file using Tencent ASR in streaming mode
    
    Args:
        file_path: Path to the audio file to transcribe
    """
    # Create the audio input and text output queues
    audio_queue = asyncio.Queue()
    text_queue = asyncio.Queue()
    
    # Create the ASR client
    asr_client = TencentASR(audio_input_queue=audio_queue, text_output_queue=text_queue)
    
    # Start the ASR service in a background task
    asr_task = asyncio.create_task(asr_client.run())
    
    # Load and queue audio chunks
    logger.info(f"Loading audio file: {file_path}")
    chunks_loaded = 0
    
    # Process the audio file and put chunks into the queue
    for chunk in process_wav_file(file_path):
        await audio_queue.put(chunk)
        chunks_loaded += 1
        
    logger.info(f"Loaded {chunks_loaded} audio chunks into the queue")
    
    # Signal the end of audio with the special end message
    await audio_queue.put(json.dumps({"type": "end"}))
    logger.info("Added end signal to the queue")
    
    # Process and display transcription results as they arrive
    full_transcript = []
    try:
        while True:
            # Wait for transcription results with a timeout
            text = await asyncio.wait_for(text_queue.get(), timeout=10.0)
            logger.info(f"Received transcription: {text}")
            full_transcript.append(text)
            text_queue.task_done()
    except asyncio.TimeoutError:
        logger.info("No more transcription results received")
    except Exception as e:
        logger.error(f"Error while processing transcription results: {e}")
    
    # Wait for the ASR task to complete
    try:
        await asr_task
    except Exception as e:
        logger.error(f"Error in ASR task: {e}")
    
    # Display the final transcript
    if full_transcript:
        logger.info("-" * 50)
        logger.info("Full transcript:")
        logger.info(" ".join(full_transcript))
        logger.info("-" * 50)
    else:
        logger.warning("No transcript was generated")

async def main():
    """
    Main function to parse arguments and run transcription
    """
    parser = argparse.ArgumentParser(description='Transcribe audio files using Tencent ASR')
    parser.add_argument('file_path', help='Path to the audio file to transcribe')
    
    args = parser.parse_args()
    file_path = args.file_path
    
    # Verify file exists
    if not Path(file_path).exists():
        logger.error(f"Audio file not found: {file_path}")
        return
    
    await transcribe_audio_file(file_path)

if __name__ == "__main__":
    asyncio.run(main())