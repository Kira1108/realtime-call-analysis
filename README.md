# RealTime Phone Call Analysis (实时电话质检)

Real-time Mandarin speech recognition system integrated with live analysis capabilities.

## Project Overview

Run with
```bash
python workflow.py
```

This project implements a real-time speech recognition and analysis system with the following components:

- **Audio Capture**: Records audio from microphone or processes audio files
- **Speech Recognition**: Uses Tencent Cloud ASR (Automatic Speech Recognition) through WebSockets for streaming transcription
- **Real-time Analysis**: Processes transcriptions using LLM to extract key information from conversations

The system is particularly designed for police call monitoring, extracting relevant information such as caller details, location, case category, and incident description in real-time.

For the LLM analysis, ensure you have Ollama running locally with the qwen3:8b model:

```bash
ollama run qwen3:8b
``` 

## Analysis Overview
```bash
INFO:asr:Got asr result: 你好，我想报警。
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: Unknown
INFO:llm:📍 Location: Unknown
INFO:llm:🔖 Case Type: Unknown
INFO:llm:📝 Description: 报警人表示需要报警
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 请问你是哪哪边？
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: Unknown
INFO:llm:📍 Location: Unknown
INFO:llm:🔖 Case Type: Unknown
INFO:llm:📝 Description: No description provided
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 我是朝阳区的一个群众。
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: Unknown
INFO:llm:📍 Location: 朝阳区
INFO:llm:🔖 Case Type: Unknown
INFO:llm:📝 Description: No description provided
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 你叫什么名字？我叫大老王。
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: 大老王
INFO:llm:📍 Location: 朝阳区
INFO:llm:🔖 Case Type: Unknown
INFO:llm:📝 Description: No description provided
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 好的，你有什么事？我们家被盗了？
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: 大老王
INFO:llm:📍 Location: 朝阳区
INFO:llm:🔖 Case Type: 盗窃
INFO:llm:📝 Description: 家中被盗
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 有贼吗？
INFO:asr:Got asr result: 对的。
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: 大老王
INFO:llm:📍 Location: 朝阳区
INFO:llm:🔖 Case Type: 盗窃
INFO:llm:📝 Description: 家中被盗
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 然后你们家具体位置在哪？
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: 大老王
INFO:llm:📍 Location: 朝阳区
INFO:llm:🔖 Case Type: 盗窃
INFO:llm:📝 Description: 家中被盗
INFO:llm:--------------------------------------------------
INFO:asr:Got asr result: 我们家具体位置在朝阳区呃，枣营北里72号楼308。
INFO:httpx:HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO:llm:--------------------------------------------------
INFO:llm:📞 Call Analysis Update:
INFO:llm:👤 Caller: 大老王
INFO:llm:📍 Location: 朝阳区枣营北里72号楼308
INFO:llm:🔖 Case Type: 盗窃
INFO:llm:📝 Description: 家中被盗
INFO:llm:--------------------------------------------------
```