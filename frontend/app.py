import chainlit as cl
import httpx
import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
@cl.on_chat_start
async def on_chat_start():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                await cl.Message(
                    content=f"สวัสดีครับ! ยินดีต้อนรับสู่ **{data.get('app_name', 'OfficeMate AI')}**\n\n"
                            "ผมช่วยตอบคำถามเกี่ยวกับองค์กรได้ครับ เช่น:\n"
                            "- นโยบายการลาป่วยเป็นอย่างไร\n"
                            "- สวัสดิการพนักงานมีอะไรบ้าง\n"
                            "- ขั้นตอนการขอเบิกค่ารักษาพยาบาล\n"
                            "- เวลาทำงานปกติของบริษัทคือกี่โมง\n\n"
                            "ลองถามมาได้เลยครับ!"
                ).send()
    except Exception as e:
        await cl.Message(
            content=f" ไม่สามารถเชื่อมต่อ Backend ได้\n"
                    f"กรุณาตรวจสอบว่า Backend Server ทำงานอยู่\n\n"
                    f"Error: {str(e)}"
        ).send()
@cl.on_message
async def on_message(message: cl.Message):
    user_message = message.content
    thinking_content = ""
    is_thinking = False
    thinking_done = False
    msg = None  
    thinking_msg = None 
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{API_BASE_URL}/chat/stream",
                json={"question": user_message},
                timeout=60.0
            ) as response:
                if response.status_code != 200:
                    await cl.Message(content=f"Error: Server returned {response.status_code}").send()
                    return
                async for chunk in response.aiter_text():
                    if not chunk:
                        continue
                    if "<think>" in chunk:
                        is_thinking = True
                        chunk = chunk.replace("<think>", "")
                        thinking_msg = cl.Message(content="กำลังคิด...")
                        await thinking_msg.send()
                    if "</think>" in chunk:
                        is_thinking = False
                        thinking_done = True
                        parts = chunk.split("</think>")
                        thinking_content += parts[0]
                        if thinking_msg:
                            await thinking_msg.remove()
                        if thinking_content.strip():
                            async with cl.Step(name="Used Thinking Process", type="tool", show_input=False) as step:
                                step.output = thinking_content.strip()
                        msg = cl.Message(content="")
                        await msg.send()
                        if len(parts) > 1 and parts[1].strip():
                            await msg.stream_token(parts[1])
                        continue
                    if is_thinking:
                        thinking_content += chunk
                    else:
                        if msg is None:
                            msg = cl.Message(content="")
                            await msg.send()
                        await msg.stream_token(chunk)
        if msg:
            await msg.update()
    except httpx.TimeoutException:
        await cl.Message(content="⏱️ Request Timeout - กรุณาลองใหม่").send()
    except httpx.ConnectError:
        await cl.Message(content=f"ไม่สามารถเชื่อมต่อ Backend ได้").send()
    except Exception as e:
        await cl.Message(content=f"เกิดข้อผิดพลาด: {str(e)}").send()