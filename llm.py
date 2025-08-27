import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import asyncio
from dataclasses import dataclass, field
from ollama import AsyncClient
import json
from typing import Optional

from pydantic import BaseModel, Field

class PoliceCallInfo(BaseModel):
    caller_name: Optional[str] = Field(None, description="Name of the caller")
    location: Optional[str] = Field(None, description="Location of the incident")
    case_category: Optional[str] = Field(None, description="Category of the case, for example, 'theft', 'assault', etc.")
    description: Optional[str] = Field(None, description="Description of the incident, less than 30 Chinese characters")
    
PoliceCallPrompt = """
You will be given a conversation of a police call between a police officer and a person.
You will need to extract the key information defined by the json schema.

Since the call is ongoing, you will update the json schema by generating a new json schema based on the recent conversation. 
and the previously generated json schema.

Your task is generate detailed information as complete as possible.
If there are no updates, you should return the current json schema.

Current collected json object is(Feel free to update this information by return new PoliceCallInfo instance):
{current_schema}

The full conversation is as follows:
{conversation}
"""

@dataclass
class CallMonitor:
    ollama_url: str = 'http://localhost:11434'
    ollama_model: str = 'qwen3:8b'
    think:bool = False
    response_model: BaseModel = field(default_factory=lambda: PoliceCallInfo)
    memory: list = field(default_factory=list)
    text_input_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    
    def __post_init__(self):
        self.client = AsyncClient(host='http://localhost:11434')
        self.current_schema = PoliceCallInfo().model_dump_json()
        
    async def run(self, message: str):
        prompt = PoliceCallPrompt.format(
            current_schema=self.current_schema,
            conversation=message
        )
        
        response = await self.client.chat(
            model=self.ollama_model, 
            messages=[{'role': 'user', 'content': prompt}], 
            think=self.think, 
            format=self.response_model.model_json_schema())
        
        instance = self.response_model(**json.loads(response.message.content))
        self.current_schema = instance.model_dump_json()
        return instance
    
    async def analyze(self):
        
        while True:
            message = await self.text_input_queue.get()
            self.memory.append(message)
            
            if self.text_input_queue.empty():
                history = "\n".join(self.memory)
                response = await self.run(history)
                caller_name = response.caller_name or "Unknown"
                location = response.location or "Unknown"
                case_category = response.case_category or "Unknown"
                description = response.description or "No description provided"
                
                logger.info("-" * 50)
                logger.info("📞 Call Analysis Update:")
                logger.info(f"👤 Caller: {caller_name}")
                logger.info(f"📍 Location: {location}")
                logger.info(f"🔖 Case Type: {case_category}")
                logger.info(f"📝 Description: {description}")
                logger.info("-" * 50)
                
                await asyncio.sleep(2)
                
            self.text_input_queue.task_done()
                
        
        
# monitor = CallMonitor()

# res = asyncio.run(monitor.run("My name is Wanghuan, working in Beijing and 33 years old."))
# print(res)