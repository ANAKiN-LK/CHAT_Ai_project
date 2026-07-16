from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest, ChatResponse
from app.graph.workflow import agent_app
router = APIRouter(prefix="/chat", tags=["Chat"])
@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        inputs = {
            "question": request.question,
            "context": None,
            "sources": [],
            "is_relevant": None,
            "answer": ""
        }
        print(f"Question: {request.question}")
        result = await agent_app.ainvoke(inputs)
        return ChatResponse(
            answer=result["answer"],
            is_from_knowledge_base=result.get("is_relevant", False),
            sources=result.get("sources", [])
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/stream")
async def chat_stream(request: ChatRequest):
    try:
        async def generate():
            inputs = {
                "question": request.question,
                "context": None,
                "sources": [],
                "is_relevant": None,
                "answer": ""
            }
            async for event in agent_app.astream_events(inputs, version="v1"):
                kind = event["event"]
                node_name = event.get("metadata", {}).get("langgraph_node", "")
                if kind == "on_chat_model_stream" and node_name in ["generate_rag", "generate_direct"]:
                    content = event["data"]["chunk"].content
                    if content:
                        yield content
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))