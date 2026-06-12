"""
Real Rails — PoC #12 · POS Transaction Simulator
FastAPI Backend: Synthetic Terminal & Offline Event Engine

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import random, uuid, datetime

app = FastAPI(
    title="Real Rails — PoC #12 · POS Transaction Simulator",
    description="Synthetic terminal event engine | Group 1: Geographic",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Synthetic Data Pools ──────────────────────────────────────────────────────

MERCHANT_NAMES = [
    "Corner Deli", "Urban Coffee", "QuickMart", "The Food Hall",
    "Pharmacy Plus", "Fuel & Go", "BookNook", "Apparel & Co",
    "Electronics Hub", "Garden Centre",
]

CARD_BRANDS    = ["Visa", "Mastercard", "Amex", "Discover"]
ENTRY_METHODS  = ["Contactless", "Chip", "Swipe", "Manual Entry"]

DECLINE_REASONS = [
    {"code": "05", "label": "Do Not Honor",            "category": "Issuer Block",    "pct": 8},
    {"code": "14", "label": "Invalid Card Number",     "category": "Data Error",      "pct": 5},
    {"code": "51", "label": "Insufficient Funds",      "category": "Balance",         "pct": 25},
    {"code": "54", "label": "Expired Card",            "category": "Data Error",      "pct": 8},
    {"code": "55", "label": "Incorrect PIN",           "category": "Auth Failure",    "pct": 20},
    {"code": "57", "label": "Transaction Not Permitted","category": "Issuer Block",   "pct": 7},
    {"code": "62", "label": "Restricted Card",         "category": "Issuer Block",    "pct": 5},
    {"code": "76", "label": "Chip Read Error",         "category": "Hardware",        "pct": 8},
    {"code": "91", "label": "Bank Unavailable",        "category": "Network",         "pct": 9},
    {"code": "96", "label": "System Error",            "category": "Technical Error", "pct": 5},
]

EMV_HANDSHAKE_TEMPLATE = [
    {"phase": "SELECT APPLICATION",      "tag": "84",   "value_fn": lambda _: "A0000000031010",           "desc": "AID — Visa Credit"},
    {"phase": "GET PROCESSING OPTIONS",  "tag": "9F02", "value_fn": lambda a: f"{int(float(a)*100):012d}", "desc": "Amount encoded (cents)"},
    {"phase": "READ RECORD",             "tag": "5F28", "value_fn": lambda _: "0840",                      "desc": "Issuer Country Code: USA"},
    {"phase": "OFFLINE DATA AUTH",       "tag": "9F27", "value_fn": lambda _: "40",                        "desc": "TC — Transaction Cert"},
    {"phase": "CARDHOLDER VERIFICATION", "tag": "9F34", "value_fn": lambda _: "420300",                    "desc": "CVM: Online PIN"},
    {"phase": "TERMINAL RISK MGMT",      "tag": "9F1A", "value_fn": lambda _: "0840",                      "desc": "Terminal Country: USA"},
    {"phase": "FIRST GENERATE AC",       "tag": "9F26", "value_fn": lambda _: uuid.uuid4().hex[:16].upper(),"desc": "Application Cryptogram"},
    {"phase": "ONLINE AUTH REQUEST",     "tag": "9F37", "value_fn": lambda _: uuid.uuid4().hex[:8].upper(), "desc": "Unpredictable Number"},
    {"phase": "ISSUER RESPONSE",         "tag": "8A",   "value_fn": lambda _: "3030",                      "desc": "Auth Response: 00 Approved"},
    {"phase": "SECOND GENERATE AC",      "tag": "9F26", "value_fn": lambda _: uuid.uuid4().hex[:16].upper(),"desc": "TC — Transaction Completed"},
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def rand_amount() -> float:
    return round(random.uniform(2.50, 450.00), 2)

def rand_card() -> dict:
    return {
        "brand":        random.choice(CARD_BRANDS),
        "last4":        str(random.randint(1000, 9999)),
        "exp":          f"{random.randint(1,12):02d}/{random.randint(25,30)}",
        "entry_method": random.choice(ENTRY_METHODS),
    }

def utcnow(offset_minutes: int = 0) -> str:
    t = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset_minutes)
    return t.isoformat() + "Z"

def build_emv(amount: float) -> list:
    return [{"phase": s["phase"], "tag": s["tag"], "value": s["value_fn"](amount), "desc": s["desc"]}
            for s in EMV_HANDSHAKE_TEMPLATE]

def weighted_decline() -> dict:
    pool = [r for r in DECLINE_REASONS for _ in range(r["pct"])]
    return random.choice(pool)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "real-rails-poc12-pos-simulator", "version": "1.0.0"}


@app.post("/api/transaction/initiate")
def initiate_transaction(
    entry_method: str           = Query(default="Contactless"),
    offline_mode: bool          = Query(default=False),
    amount:       Optional[float] = Query(default=None),
):
    """Full POS transaction lifecycle — EMV handshake, approval/decline, receipt, SAF flag."""
    txn_amount = amount if amount else rand_amount()
    card       = rand_card()
    card["entry_method"] = entry_method
    approved   = random.random() > 0.22
    decline    = weighted_decline() if not approved else None

    return {
        "transaction_id":     f"TXN-{uuid.uuid4().hex[:10].upper()}",
        "timestamp":          utcnow(),
        "merchant":           random.choice(MERCHANT_NAMES),
        "amount":             txn_amount,
        "currency":           "USD",
        "card":               card,
        "status":             "APPROVED" if approved else "DECLINED",
        "offline_mode":       offline_mode,
        "authorization_code": uuid.uuid4().hex[:6].upper() if approved else None,
        "decline_reason":     decline,
        "store_and_forward":  offline_mode and approved,
        "emv_handshake":      build_emv(txn_amount) if entry_method in ["Chip", "Contactless"] else [],
        "receipt_fields": {
            "merchant_name":    random.choice(MERCHANT_NAMES),
            "terminal_id":      f"T{random.randint(10000,99999)}",
            "transaction_date": utcnow()[:10],
            "transaction_time": utcnow()[11:19],
            "entry_method":     entry_method,
            "card_brand":       card["brand"],
            "last4":            card["last4"],
            "amount":           f"${txn_amount:.2f}",
            "approval_code":    uuid.uuid4().hex[:6].upper() if approved else "DECLINED",
            "stan":             str(random.randint(100000, 999999)),
            "cfpb_required":    ["Merchant Name","Amount","Auth Code","Card Last4","Entry Method","Date/Time"],
        },
    }


@app.get("/api/transactions/history")
def transaction_history(
    count:        int = Query(default=30, le=100),
    entry_method: str = Query(default="all"),
    status:       str = Query(default="all"),
):
    """Filterable batch of synthetic historical transactions."""
    rows = []
    for i in range(count * 2):
        card     = rand_card()
        approved = random.random() > 0.22
        method   = card["entry_method"]
        st       = "APPROVED" if approved else "DECLINED"
        if entry_method != "all" and method != entry_method: continue
        if status != "all" and st != status: continue
        rows.append({
            "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "timestamp":      utcnow(offset_minutes=i * 3),
            "merchant":       random.choice(MERCHANT_NAMES),
            "amount":         rand_amount(),
            "card_brand":     card["brand"],
            "entry_method":   method,
            "status":         st,
            "decline_reason": weighted_decline()["label"] if not approved else None,
        })
        if len(rows) >= count: break
    return {"transactions": rows[:count], "total": len(rows[:count])}


@app.get("/api/analytics/decline-breakdown")
def decline_breakdown():
    """Decline reason distribution — CFPB consumer credit report benchmarks."""
    total = random.randint(80, 200)
    breakdown = []
    category_rollup: dict = {}
    for r in DECLINE_REASONS:
        count = max(1, int(total * r["pct"] / 100))
        breakdown.append({"code": r["code"], "label": r["label"], "category": r["category"], "count": count, "percentage": r["pct"]})
        category_rollup[r["category"]] = category_rollup.get(r["category"], 0) + count
    return {
        "total_declines":  total,
        "breakdown":       breakdown,
        "category_rollup": [{"category": k, "count": v} for k, v in category_rollup.items()],
        "source":          "Synthetic benchmark — CFPB Consumer Credit Reports",
    }


@app.get("/api/analytics/entry-method-stats")
def entry_method_stats():
    """Entry method share + avg ticket — Federal Reserve Payments Study 2022."""
    return {
        "stats": [
            {"method": "Contactless", "share": 41, "trend": "+12% YoY", "avg_ticket": 28.50, "fraud_rate_bps": 4},
            {"method": "Chip",        "share": 38, "trend": "+2% YoY",  "avg_ticket": 74.20, "fraud_rate_bps": 2},
            {"method": "Swipe",       "share": 15, "trend": "-8% YoY",  "avg_ticket": 42.10, "fraud_rate_bps": 18},
            {"method": "Manual Entry","share": 6,  "trend": "-2% YoY",  "avg_ticket": 190.00,"fraud_rate_bps": 65},
        ],
        "source": "Federal Reserve Payments Study 2022 (synthetic benchmark)",
        "note":   "Fraud rate in basis points per $1,000 transacted",
    }


@app.get("/api/offline/pending")
def offline_pending():
    """Store-and-Forward queue — transactions held locally during outage."""
    count   = random.randint(2, 8)
    pending = []
    for _ in range(count):
        amount = rand_amount()
        card   = rand_card()
        pending.append({
            "local_id":     f"SAF-{uuid.uuid4().hex[:6].upper()}",
            "queued_at":    utcnow(offset_minutes=random.randint(5, 120)),
            "amount":       amount,
            "card_brand":   card["brand"],
            "last4":        card["last4"],
            "status":       "PENDING_SYNC",
            "risk_flag":    amount > 200,
            "offline_token":uuid.uuid4().hex[:32].upper(),
        })
    return {
        "queue":         pending,
        "total_pending": count,
        "total_amount":  round(sum(t["amount"] for t in pending), 2),
        "sync_risk":     "HIGH" if any(t["risk_flag"] for t in pending) else "LOW",
    }


@app.get("/api/sample-data")
def sample_data():
    """Downloadable 20-record synthetic dataset — CFPB Reg E labeled."""
    rows = []
    for i in range(20):
        amount = rand_amount()
        card   = rand_card()
        appr   = random.random() > 0.22
        dec    = weighted_decline() if not appr else {}
        rows.append({
            "txn_id":         f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "timestamp":      utcnow(offset_minutes=i * 15),
            "merchant":       random.choice(MERCHANT_NAMES),
            "amount_usd":     amount,
            "card_brand":     card["brand"],
            "last4":          card["last4"],
            "entry_method":   card["entry_method"],
            "status":         "APPROVED" if appr else "DECLINED",
            "decline_code":   dec.get("code", ""),
            "decline_reason": dec.get("label", ""),
            "offline_auth":   random.random() < 0.12,
            "cfpb_compliant": True,
            "source":         "Synthetic — Real Rails PoC #12",
        })
    return JSONResponse(content={
        "dataset":      "POS Transaction Simulator — Sample Data",
        "poc":          "12",
        "generated":    utcnow(),
        "disclaimer":   "Synthetic data only. Not real transaction records.",
        "data_sources": ["CFPB Consumer Credit Reports", "Federal Reserve Payments Study"],
        "records":      rows,
    })
