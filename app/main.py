from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, ChatResponse, VoiceOutRequest, HealthResponse
from app.memory.store import InMemoryStore
from app.agents.brain import FusionBrain
from app.voice.stt import STTEngine
from app.voice.tts import synthesize_stub
from config.settings import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_store = InMemoryStore()
brain = FusionBrain()
stt_engine = STTEngine(model_size="base")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse()


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    try:
        memory_items = memory_store.get(payload.user_id) if payload.use_memory else []
        memory_context = "\n".join([f"{m['role']}: {m['content']}" for m in memory_items])

        result = await brain.run(payload.message, memory_context=memory_context)

        memory_store.add(payload.user_id, "user", payload.message)
        memory_store.add(payload.user_id, "assistant", result["reply"])

        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/voice/in")
async def voice_in(audio: UploadFile = File(...), user_id: str = "default_user"):
    try:
        audio_bytes = await audio.read()
        text = stt_engine.transcribe_bytes(audio_bytes, suffix=".wav")

        memory_items = memory_store.get(user_id)
        memory_context = "\n".join([f"{m['role']}: {m['content']}" for m in memory_items])
        result = await brain.run(text, memory_context=memory_context)

        memory_store.add(user_id, "user", text)
        memory_store.add(user_id, "assistant", result["reply"])

        return {
            "transcript": text,
            "assistant_reply": result["reply"],
            "tool_used": result["tool_used"],
            "tool_result": result["tool_result"],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/voice/out")
async def voice_out(payload: VoiceOutRequest):
    return synthesize_stub(payload.text)
