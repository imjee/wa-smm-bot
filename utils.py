import re
from typing import Tuple, Optional


CMD_HELP = (
"📌 Menu:\n"
"saldo – cek saldo provider\n"
"layanan – list 10 layanan pertama\n"
"layanan <kata> – cari layanan mengandung kata\n"
"harga <service_id> <qty> – estimasi harga\n"
"order <service_id> <link> <qty> – buat pesanan\n"
"status <order_id> – cek status\n"
"status_multi <id1,id2,...> – cek banyak status\n"
"refill <order_id> – ajukan refill\n"
"cancel <id1,id2,...> – ajukan cancel\n"
"topup <nominalUSD> – buat invoice topup (dummy)\n"
)


RE_ORDER = re.compile(r"^order\s+(\d+)\s+(\S+)\s+(\d+)", re.I)
RE_HARGA = re.compile(r"^harga\s+(\d+)\s+(\d+)", re.I)




def parse_order(text: str) -> Optional[Tuple[int, str, int]]:
m = RE_ORDER.match(text)
if not m:
return None
return int(m.group(1)), m.group(2), int(m.group(3))




def parse_harga(text: str) -> Optional[Tuple[int, int]]:
m = RE_HARGA.match(text)
if not m:
return None
return int(m.group(1)), int(m.group(2))




def calc_charge_usd(rate_per_1000: float, qty: int) -> float:
return round((rate_per_1000 * qty) / 1000.0, 6)
