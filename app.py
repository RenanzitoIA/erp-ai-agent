import os, requests, hashlib, hmac, json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from erp_schemas import ERPEvent, AskInput, ForecastRequest
from slack_client import post_message
from llm_client import ask_llm

load_dotenv()

R_URL = f"http://r-analytics:{os.getenv('R_PORT','8000')}"
ERP_SIGNING_SECRET = os.getenv("ERP_SIGNING_SECRET", "change-me")

app = FastAPI(title="ERP Copilot API")

def verify_signature(body: bytes, signature: str):
    mac = hmac.new(ERP_SIGNING_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature or "")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/webhook/erp")
async def erp_webhook(request: Request):
    signature = request.headers.get("X-ERP-Signature", "")
    body = await request.body()
    if not verify_signature(body, signature):
        raise HTTPException(401, "invalid signature")
    data = ERPEvent(**json.loads(body.decode()))
    if data.event == "order.created":
        order = data.payload
        msg = f"🧾 Pedido #{order.get('id')} criado por {order.get('customer')} no valor de {order.get('amount')}."
        post_message(msg)
    return {"received": True}

@app.post("/ask")
def ask(payload: AskInput):
    prompt = f"Você é um copiloto de ERP. Contexto: {payload.context or 'N/A'}. KPIs: {json.dumps(payload.kpis or {}, ensure_ascii=False)}. Pergunta: {payload.question}. Responda de forma objetiva."
    answer = ask_llm(prompt)
    post_message(f"🤖 *Resposta do Copilot:*\n{answer[:1800]}")
    return {"answer": answer}

@app.post("/forecast")
def forecast(req: ForecastRequest):
    r = requests.post(f"{R_URL}/forecast", json=req.model_dump(), timeout=60)
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    return r.json()
