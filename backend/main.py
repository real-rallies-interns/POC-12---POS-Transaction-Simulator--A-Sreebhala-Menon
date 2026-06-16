"""
Real Rails — PoC #12 · POS Transaction Simulator
FastAPI Backend — zero hardcoded data, all loaded from mock_data.py

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import random, uuid, datetime, os
from dotenv import load_dotenv

# ── All data from mock_data.py ────────────────────────────────────────────────
from data.mock_data import (
    SYNTHETIC_LABEL,
    MERCHANTS,
    CARD_BRAND_POOL,
    CARD_TYPE_POOL,
    ENTRY_METHOD_POOL,
    CURRENCY_POOL,
    DECLINE_POOL,
    DECLINE_REASONS,
    ENTRY_METHODS,
    ISSUING_BANK_POOL,
    TERMINAL_POOL,
    EDGE_CASES,
    FIELD_DEFINITIONS,
    EMV_HANDSHAKE_STEPS,
    DEFAULT_ENTRY_METHOD,
    EMV_ENTRY_METHODS,
)

load_dotenv()

app = FastAPI(
    title="Real Rails — PoC #12 · POS Transaction Simulator",
    description="Synthetic terminal event engine | Group 1: Geographic",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS — no data defined here, only logic
# ══════════════════════════════════════════════════════════════════════════════

def rand_merchant() -> dict:
    return random.choice(MERCHANTS)

def rand_amount(merchant: dict | None = None) -> float:
    """Scale amount around merchant avg_ticket when available."""
    if merchant:
        avg = merchant.get("avg_ticket", 50.0)
        lo  = max(0.50,  avg * 0.3)
        hi  = min(500.0, avg * 3.5)
        return round(random.uniform(lo, hi), 2)
    return round(random.uniform(2.50, 450.00), 2)

def rand_card() -> dict:
    return {
        "brand":        random.choice(CARD_BRAND_POOL),
        "last4":        str(random.randint(1000, 9999)),
        "exp":          f"{random.randint(1,12):02d}/{random.randint(26,30)}",
        "type":         random.choice(CARD_TYPE_POOL),
        "issuing_bank": random.choice(ISSUING_BANK_POOL),
    }

def rand_fraud_score(approved: bool) -> int:
    return random.randint(0, 30) if approved else random.randint(40, 95)

def utcnow(offset_minutes: int = 0) -> str:
    t = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset_minutes)
    return t.isoformat() + "Z"

def build_emv(amount: float) -> list:
    """Build EMV handshake from mock_data template — injects runtime values."""
    result = []
    for step in EMV_HANDSHAKE_STEPS:
        if step["phase"] == "GET PROCESSING OPTIONS":
            value = f"{int(float(amount) * 100):012d}"
        elif step["phase"] in ("FIRST GENERATE AC", "SECOND GENERATE AC"):
            value = uuid.uuid4().hex[:16].upper()
        elif step["phase"] == "ONLINE AUTH REQUEST":
            value = uuid.uuid4().hex[:8].upper()
        else:
            value = step["static_value"]
        result.append({
            "phase": step["phase"],
            "tag":   step["tag"],
            "value": value,
            "desc":  step["desc"],
        })
    return result

def weighted_decline() -> dict:
    return random.choice(DECLINE_POOL)

def build_receipt(merchant: dict, card: dict, entry_method: str,
                  amount: float, approved: bool, currency: str) -> dict:
    return {
        "merchant_name":    merchant["name"],
        "merchant_city":    merchant["city"],
        "merchant_country": merchant["country"],
        "merchant_mcc":     merchant["mcc"],
        "terminal_id":      f"T{random.randint(10000, 99999)}",
        "terminal_make":    random.choice(TERMINAL_POOL),
        "transaction_date": utcnow()[:10],
        "transaction_time": utcnow()[11:19],
        "entry_method":     entry_method,
        "card_brand":       card["brand"],
        "card_type":        card["type"],
        "last4":            card["last4"],
        "currency":         currency,
        "amount":           f"{amount:.2f}",
        "approval_code":    uuid.uuid4().hex[:6].upper() if approved else "DECLINED",
        "stan":             str(random.randint(100000, 999999)),
        "rrn":              uuid.uuid4().hex[:12].upper(),
        "cfpb_required":    [
            "Merchant Name", "Amount", "Auth Code",
            "Card Last4", "Entry Method", "Date/Time", "Currency"
        ],
    }

# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
def health():
    return {
        "status":  "ok",
        "service": "real-rails-poc12-pos-simulator",
        "version": "1.0.0",
    }


@app.post("/api/transaction/initiate")
def initiate_transaction(
    entry_method:  str             = Query(default=DEFAULT_ENTRY_METHOD),
    offline_mode:  bool            = Query(default=False),
    amount:        Optional[float] = Query(default=None),
    merchant_name: Optional[str]   = Query(default=None),
    currency:      Optional[str]   = Query(default=None),
):
    """Full POS transaction lifecycle — EMV handshake, approval/decline, receipt, SAF flag."""
    merchant   = next((m for m in MERCHANTS if m["name"] == merchant_name), rand_merchant()) \
                 if merchant_name else rand_merchant()
    txn_amount = amount if amount else rand_amount(merchant)
    card       = rand_card()
    txn_curr   = currency if currency else random.choice(CURRENCY_POOL)
    approved   = random.random() > 0.22
    decline    = weighted_decline() if not approved else None

    return {
        "transaction_id":     f"TXN-{uuid.uuid4().hex[:10].upper()}",
        "timestamp":          utcnow(),
        "merchant":           merchant["name"],
        "merchant_detail":    merchant,
        "amount":             txn_amount,
        "currency":           txn_curr,
        "card":               card,
        "entry_method":       entry_method,
        "status":             "APPROVED" if approved else "DECLINED",
        "offline_mode":       offline_mode,
        "authorization_code": uuid.uuid4().hex[:6].upper() if approved else None,
        "decline_reason":     decline,
        "store_and_forward":  offline_mode and approved,
        "risk_flag":          txn_amount > 200 and offline_mode,
        "fraud_score":        rand_fraud_score(approved),
        "processing_time_ms": random.randint(80, 3500),
        "emv_handshake":      build_emv(txn_amount) if entry_method in EMV_ENTRY_METHODS else [],
        "receipt_fields":     build_receipt(merchant, card, entry_method, txn_amount, approved, txn_curr),
        "data_label":         SYNTHETIC_LABEL,
    }


@app.get("/api/transactions/history")
def transaction_history(
    count:        int = Query(default=30, le=100),
    entry_method: str = Query(default="all"),
    status:       str = Query(default="all"),
    merchant:     str = Query(default="all"),
    city:         str = Query(default="all"),
):
    """Filterable batch of synthetic historical transactions."""
    rows = []
    for i in range(count * 3):
        m        = rand_merchant()
        card     = rand_card()
        method   = random.choice(ENTRY_METHOD_POOL)
        approved = random.random() > 0.22
        amount   = rand_amount(m)
        st       = "APPROVED" if approved else "DECLINED"

        if entry_method != "all" and method    != entry_method: continue
        if status       != "all" and st        != status:       continue
        if merchant     != "all" and m["name"] != merchant:     continue
        if city         != "all" and m["city"] != city:         continue

        dec = weighted_decline() if not approved else {}
        rows.append({
            "transaction_id":    f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "timestamp":         utcnow(offset_minutes=i * 3),
            "merchant":          m["name"],
            "merchant_city":     m["city"],
            "merchant_mcc":      m["mcc"],
            "merchant_category": m["category"],
            "amount":            amount,
            "currency":          random.choice(CURRENCY_POOL),
            "card_brand":        card["brand"],
            "card_type":         card["type"],
            "entry_method":      method,
            "status":            st,
            "fraud_score":       rand_fraud_score(approved),
            "decline_reason":    dec.get("label")    if not approved else None,
            "decline_code":      dec.get("code")     if not approved else None,
            "decline_category":  dec.get("category") if not approved else None,
            "offline_auth":      random.random() < 0.10,
            "data_label":        SYNTHETIC_LABEL,
        })
        if len(rows) >= count:
            break

    return {"transactions": rows[:count], "total": len(rows[:count])}


@app.get("/api/merchants")
def get_merchants():
    """All merchant locations with geographic coordinates for map rendering."""
    return {
        "merchants":  MERCHANTS,
        "total":      len(MERCHANTS),
        "data_label": SYNTHETIC_LABEL,
    }


@app.get("/api/analytics/decline-breakdown")
def decline_breakdown():
    """Decline reason distribution — CFPB consumer credit report benchmarks."""
    total = random.randint(80, 200)
    breakdown, category_rollup = [], {}
    for r in DECLINE_REASONS:
        count = max(1, int(total * r["pct"] / 100))
        breakdown.append({
            "code":          r["code"],
            "label":         r["label"],
            "category":      r["category"],
            "description":   r["description"],
            "retry_advised": r["retry_advised"],
            "count":         count,
            "percentage":    r["pct"],
        })
        category_rollup[r["category"]] = category_rollup.get(r["category"], 0) + count
    return {
        "total_declines":  total,
        "breakdown":       breakdown,
        "category_rollup": [{"category": k, "count": v} for k, v in category_rollup.items()],
        "source":          "Synthetic benchmark — CFPB Consumer Credit Reports",
        "data_label":      SYNTHETIC_LABEL,
    }


@app.get("/api/analytics/entry-method-stats")
def entry_method_stats():
    """Entry method market share + fraud rates — Federal Reserve Payments Study 2022."""
    return {
        "stats":      ENTRY_METHODS,
        "avg_tickets":[
            {"merchant": m["name"], "category": m["category"], "avg_ticket": m["avg_ticket"]}
            for m in MERCHANTS
        ],
        "source":     "Federal Reserve Payments Study 2022 (synthetic benchmark)",
        "data_label": SYNTHETIC_LABEL,
    }


@app.get("/api/analytics/merchant-stats")
def merchant_stats():
    """Per-merchant synthetic transaction volume and approval rate."""
    stats = []
    for m in MERCHANTS:
        txn_count = random.randint(120, 980)
        approved  = int(txn_count * random.uniform(0.74, 0.88))
        stats.append({
            "merchant":    m["name"],
            "category":    m["category"],
            "city":        m["city"],
            "mcc":         m["mcc"],
            "lat":         m["lat"],
            "lng":         m["lng"],
            "txn_count":   txn_count,
            "approved":    approved,
            "declined":    txn_count - approved,
            "approval_pct":round(approved / txn_count * 100, 1),
            "avg_ticket":  m["avg_ticket"],
            "peak_hours":  m["peak_hours"],
        })
    return {"merchants": stats, "data_label": SYNTHETIC_LABEL}


@app.get("/api/offline/pending")
def offline_pending():
    """Store-and-Forward queue — transactions held locally during outage."""
    count, pending = random.randint(2, 8), []
    for _ in range(count):
        m      = rand_merchant()
        amount = rand_amount(m)
        card   = rand_card()
        pending.append({
            "local_id":      f"SAF-{uuid.uuid4().hex[:6].upper()}",
            "queued_at":     utcnow(offset_minutes=random.randint(5, 120)),
            "merchant":      m["name"],
            "merchant_city": m["city"],
            "amount":        amount,
            "currency":      random.choice(CURRENCY_POOL),
            "card_brand":    card["brand"],
            "card_type":     card["type"],
            "last4":         card["last4"],
            "entry_method":  random.choice(ENTRY_METHOD_POOL),
            "status":        "PENDING_SYNC",
            "risk_flag":     amount > 200,
            "offline_token": uuid.uuid4().hex[:32].upper(),
        })
    return {
        "queue":         pending,
        "total_pending": count,
        "total_amount":  round(sum(t["amount"] for t in pending), 2),
        "sync_risk":     "HIGH" if any(t["risk_flag"] for t in pending) else "LOW",
        "data_label":    SYNTHETIC_LABEL,
    }


@app.get("/api/edge-cases")
def get_edge_cases():
    """All 30 edge case scenarios from the mock data package."""
    return {
        "edge_cases": EDGE_CASES,
        "total":      len(EDGE_CASES),
        "data_label": SYNTHETIC_LABEL,
    }


@app.get("/api/emv-template")
def emv_template():
    """EMV handshake protocol steps reference — EMVCo Book 3 v4.3."""
    return {
        "steps":      EMV_HANDSHAKE_STEPS,
        "total":      len(EMV_HANDSHAKE_STEPS),
        "source":     "EMVCo Book 3 — Application Specification v4.3",
        "data_label": SYNTHETIC_LABEL,
    }


@app.get("/api/data-dictionary")
def data_dictionary():
    """Full field definitions for all transaction entities."""
    return {
        "title":       "Real Rails PoC #12 — POS Transaction Simulator",
        "disclaimer":  SYNTHETIC_LABEL,
        "fields":      FIELD_DEFINITIONS,
        "field_count": len(FIELD_DEFINITIONS),
    }


@app.get("/api/sample-data")
def sample_data():
    """Downloadable 20-record synthetic dataset — CFPB Reg E labeled."""
    rows = []
    for i in range(20):
        m      = rand_merchant()
        amount = rand_amount(m)
        card   = rand_card()
        method = random.choice(ENTRY_METHOD_POOL)
        appr   = random.random() > 0.22
        dec    = weighted_decline() if not appr else {}
        rows.append({
            "txn_id":            f"TXN-{uuid.uuid4().hex[:8].upper()}",
            "timestamp":         utcnow(offset_minutes=i * 15),
            "merchant":          m["name"],
            "merchant_city":     m["city"],
            "merchant_country":  m["country"],
            "merchant_mcc":      m["mcc"],
            "merchant_category": m["category"],
            "merchant_lat":      m["lat"],
            "merchant_lng":      m["lng"],
            "amount":            amount,
            "currency":          random.choice(CURRENCY_POOL),
            "card_brand":        card["brand"],
            "card_type":         card["type"],
            "last4":             card["last4"],
            "issuing_bank":      card["issuing_bank"],
            "entry_method":      method,
            "status":            "APPROVED" if appr else "DECLINED",
            "decline_code":      dec.get("code", ""),
            "decline_reason":    dec.get("label", ""),
            "decline_category":  dec.get("category", ""),
            "fraud_score":       rand_fraud_score(appr),
            "offline_auth":      random.random() < 0.12,
            "processing_ms":     random.randint(80, 3500),
            "cfpb_compliant":    True,
            "data_label":        SYNTHETIC_LABEL,
        })
    return JSONResponse(content={
        "dataset":      "POS Transaction Simulator — Sample Data",
        "poc":          "12",
        "group":        "1 — Geographic",
        "generated":    utcnow(),
        "disclaimer":   SYNTHETIC_LABEL,
        "data_sources": ["CFPB Consumer Credit Reports", "Federal Reserve Payments Study 2022"],
        "records":      rows,
    })
