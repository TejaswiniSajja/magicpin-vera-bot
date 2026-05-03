from fastapi import FastAPI
from pydantic import BaseModel
from store import store_context, get_merchant, get_trigger, get_customer
from composer import compose_message
from reply_handler import handle_reply
from typing import Optional
app = FastAPI()


class ContextInput(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: dict
    delivered_at: str


class TickInput(BaseModel):
    merchant_context_id: str
    trigger_context_id: str
    customer_context_id: Optional[str] = None


class ReplyInput(BaseModel):
    merchant_reply: str
    last_message: dict


@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/v1/metadata")
def metadata():
    return {
        "bot_name": "magicpin_vera_submission_bot",
        "version": "1.0",
        "deterministic": True
    }


@app.post("/v1/context")
def ingest_context(data: ContextInput):
    accepted = store_context(data.scope, data.context_id, data.version, data.payload)
    return {
        "accepted": accepted,
        "ack_id": f"ack_{data.context_id}_{data.version}"
    }


@app.post("/v1/tick")
def tick(data: TickInput):
    merchant = get_merchant(data.merchant_context_id)
    trigger = get_trigger(data.trigger_context_id)
    customer = get_customer(data.customer_context_id) if data.customer_context_id else None

    result = compose_message(merchant, trigger, customer)
    return result


@app.post("/v1/reply")
def reply(data: dict):
    user_message = data.get("message", "")
    
    result = handle_reply(user_message, None)

    return result