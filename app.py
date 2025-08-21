import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Order, Service, MessageLog
from services_client import IndosmmClient
from utils import CMD_HELP, parse_order, parse_harga, calc_charge_usd
from billing import ensure_user, create_invoice, mark_invoice_paid, deduct_balance
import requests


# Optional: Twilio Client
from twilio.rest import Client as TwilioClient


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smm.db")
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "changeme")


# Provider setup
USE_PROVIDER = os.getenv("USE_PROVIDER", "twilio")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")


twilio_client = None
if USE_PROVIDER == "twilio" and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# indosmm client
smm = IndosmmClient()


# ===== Helper: send message =====


def send_wa(to: str, body: str):
"""Send a WhatsApp text message via provider (Twilio).
`to` should be in format 'whatsapp:+62xxxxxxxxxx' for Twilio.
"""
session = Session()
try:
if USE_PROVIDER == "twilio":
if not twilio_client:
print("Twilio not configured")
return
msg = twilio_client.messages.create(
from_=TWILIO_WHATSAPP_FROM,
to=to,
body=body,
)
session.add(MessageLog(to=to, body=body, provider_msg_id=msg.sid))
session.commit()
else:
print("Provider not implemented. Message:", body)
finally:
session.close()




# ===== Commands Implementation =====


@app.post("/webhook/wa")
def webhook_wa():
"""
Twilio WhatsApp inbound webhook (set URL ini di Twilio console)
Body params minimal: From, Body
"""
from_wa = request.form.get("From") # e.g., 'whatsapp:+62812xxxx'
body = (request.form.get("Body") or "").strip()


if not from_wa:
return ("", 400)


session = Session()
try:
ensure_user(session, wa=fr
