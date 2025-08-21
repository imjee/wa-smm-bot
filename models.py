from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True)
wa = Column(String(64), unique=True, nullable=False) # whatsapp jid/number
name = Column(String(128))
balance = Column(Float, default=0.0)
is_blocked = Column(Boolean, default=False)
created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
__tablename__ = "orders"
id = Column(Integer, primary_key=True)
user_wa = Column(String(64), index=True)
service_id = Column(Integer, nullable=False)
link = Column(Text, nullable=False)
quantity = Column(Integer, nullable=False)
est_charge = Column(Float, default=0.0) # perkiraan charge (USD)
provider_order_id = Column(String(64), index=True)
status = Column(String(32), default="created")
created_at = Column(DateTime, default=datetime.utcnow)


class Service(Base):
__tablename__ = "services"
service = Column(Integer, primary_key=True) # id layanan dari indosmm
name = Column(String(256))
type = Column(String(128))
category = Column(String(256))
rate = Column(Float) # USD / 1000
min = Column(Integer)
max = Column(Integer)
refill = Column(Boolean)
cancel = Column(Boolean)
updated_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
__tablename__ = "payments"
id = Column(Integer, primary_key=True)
user_wa = Column(String(64), index=True)
amount = Column(Float, default=0.0)
currency = Column(String(8), default="USD")
status = Column(String(16), default="pending") # pending|paid|failed
provider_ref = Column(String(128)) # id invoice dari PG (jika ada)
created_at = Column(DateTime, default=datetime.utcnow)


class MessageLog(Base):
__tablename__ = "messages"
id = Column(Integer, primary_key=True)
to = Column(String(64))
body = Column(Text)
provider_msg_id = Column(String(128))
created_at = Column(DateTime, default=datetime.utcnow)
