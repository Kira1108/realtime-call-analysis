import logging
logging.basicConfig(level=logging.INFO)
from microphone import MicrophoneClient
from asr import TencentASR
from llm import CallMonitor
import asyncio

async def workflow():
    audio_input_queue = asyncio.Queue()
    text_output_queue = asyncio.Queue()
    microphone_client = MicrophoneClient(audio_input_queue=audio_input_queue)
    asr_client = TencentASR(audio_input_queue=audio_input_queue, text_output_queue=text_output_queue)
    call_monitor = CallMonitor(text_input_queue=text_output_queue)
    await asr_client.connect()
    record_task = asyncio.create_task(microphone_client.record())
    send_task = asyncio.create_task(asr_client.send_audio())
    receive_task = asyncio.create_task(asr_client.receive_results())
    monitor_task = asyncio.create_task(call_monitor.analyze())
    logging.info("Starting the workflow...")
    
    await asyncio.gather(record_task, send_task, receive_task, monitor_task)
    await asyncio.sleep(0.1)
    print("Workflow completed.")
    
    
asyncio.run(workflow())
    
