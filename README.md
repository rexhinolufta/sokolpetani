# FusionBrain v0.1

FusionBrain është një prototip në stilin Jarvis me fokus te mjetet free dhe deployment cloud.

## Çfarë përfshin v0.1
- Chat endpoint me memory të thjeshtë.
- Tool-calling për motin (wttr.in) dhe web lookup (DuckDuckGo instant answer).
- Voice-in endpoint (Whisper STT).
- Voice-out endpoint placeholder.
- UI frontend minimal në `index.html`.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Vendos `OPENROUTER_API_KEY` në `.env`.

## Run backend
```bash
uvicorn app.main:app --reload --port 8000
```

## Test
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","message":"Si eshte moti ne Tirane?","use_memory":true}'
```

## Run frontend
Hap `index.html` direkt në browser. Frontend thërret API-n në `http://127.0.0.1:8000`.

## Roadmap v0.2
- Piper TTS real (audio `.wav`).
- Vision endpoint (OpenCV + YOLO).
- Organizim autonom (reminder/task scheduler).
