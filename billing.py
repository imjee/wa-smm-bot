from sqlalchemy.orm import Session
from models import User, Payment
from typing import Optional


USD_TO_IDR = 16000 # ubah sesuai kurs




def ensure_user(session: Session, wa: str, name: str = None) -> User:
user = session.query(User).filter_by(wa=wa).first()
if not user:
user = User(wa=wa, name=name or wa, balance=0.0)
session.add(user)
session.commit()
return user




def add_balance(session: Session, wa: str, amount_usd: float):
user = ensure_user(session, wa)
user.balance = round((user.balance or 0) + amount_usd, 6)
session.commit()
return user.balance




def deduct_balance(session: Session, wa: str, amount_usd: float) -> bool:
user = ensure_user(session, wa)
if (user.balance or 0) < amount_usd:
return False
user.balance = round(user.balance - amount_usd, 6)
session.commit()
return True




def create_invoice(session: Session, wa: str, amount_usd: float) -> Payment:
p = Payment(user_wa=wa, amount=amount_usd, currency="USD", status="pending", provider_ref=f"INV-{wa}")
session.add(p)
session.commit()
return p




def mark_invoice_paid(session: Session, payment_id: int) -> Optional[Payment]:
p = session.query(Payment).get(payment_id)
if not p:
return None
p.status = "paid"
session.commit()
add_balance(session, p.user_wa, p.amount)
return p
