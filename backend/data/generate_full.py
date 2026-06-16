"""
Real Rails — PoC #12 · POS Transaction Simulator
═══════════════════════════════════════════════════════════════════
TITLE:        POS Transaction Simulator — Synthetic Mock Data Package
ENTITIES:     Transaction, Merchant, Card, Terminal, EMV Handshake,
              Decline Reason, Store-and-Forward Queue, Receipt
FIELDS:       63 fields per transaction record
SAMPLE_ROWS:  500 main records + 30 edge case records
EXPORTS:      CSV + JSON (main + edge cases + data dictionary)
LABEL:        Every record carries data_label = 'SYNTHETIC — NOT REAL TRANSACTION DATA'
EDGE CASES:   30 scenarios covering error states and unusual conditions
═══════════════════════════════════════════════════════════════════
"""

import json, csv, random, uuid, datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_data import (
    SYNTHETIC_LABEL,
    MERCHANTS,
    CARD_BRANDS, CARD_BRAND_POOL,
    CARD_TYPES,  CARD_TYPE_POOL,
    ENTRY_METHODS, ENTRY_METHOD_POOL,
    CURRENCIES, CURRENCY_POOL,
    DECLINE_REASONS, DECLINE_POOL,
    ISSUING_BANKS, ISSUING_BANK_POOL,
    TERMINAL_MANUFACTURERS, TERMINAL_POOL,
    EDGE_CASES,
    EMV_HANDSHAKE_STEPS,
    FIELD_DEFINITIONS,
)

random.seed(42)  # reproducible

# ── CONFIG ────────────────────────────────────────────────────────────────────
TITLE       = "POS Transaction Simulator — Synthetic Mock Data Package"
SAMPLE_ROWS = 500
EDGE_ROWS   = 30
OUT         = os.path.dirname(os.path.abspath(__file__))

# ── ENTITIES (for data dictionary header) ─────────────────────────────────────
ENTITIES = {
    "Transaction":   "A single card payment event from initiation to final status",
    "Merchant":      "Physical or virtual point-of-sale location",
    "Card":          "Synthetic payment card (brand, type, issuing bank)",
    "Terminal":      "POS hardware device at merchant location",
    "EMV_Handshake": "10-step chip card protocol exchange between card and terminal",
    "DeclineReason": "ISO 8583 response code with category and retry guidance",
    "SAF_Queue":     "Store-and-Forward offline transaction queue",
    "Receipt":       "CFPB Reg E compliant digital receipt fields",
}

# ── FIELDS (63 total — sourced from mock_data.FIELD_DEFINITIONS) ──────────────
FIELDS = list(FIELD_DEFINITIONS.keys())

# ── HELPERS ───────────────────────────────────────────────────────────────────
def rn(a, b):    return round(random.uniform(a, b), 2)
def ri(a, b):    return random.randint(a, b)
def rHex(n):     return ''.join(random.choices('0123456789ABCDEF', k=n))
def ts(offset=0):
    t = datetime.datetime.utcnow() - datetime.timedelta(minutes=offset)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def rand_merchant():   return random.choice(MERCHANTS)
def rand_card():
    return {
        "card_brand":   random.choice(CARD_BRAND_POOL),
        "card_last4":   str(ri(1000, 9999)),
        "card_exp":     f"{ri(1,12):02d}/{ri(26,30)}",
        "card_type":    random.choice(CARD_TYPE_POOL),
        "issuing_bank": random.choice(ISSUING_BANK_POOL),
    }
def rand_amount(m):
    avg = m.get("avg_ticket", 50.0)
    return round(random.uniform(max(0.50, avg*0.3), min(500.0, avg*3.5)), 2)
def rand_terminal():   return random.choice(TERMINAL_POOL)
def rand_decline():    return random.choice(DECLINE_POOL)
def rand_entry():      return random.choice(ENTRY_METHOD_POOL)
def rand_currency():   return random.choice(CURRENCY_POOL)
def fraud_score(appr): return ri(0,30) if appr else ri(40,95)

def build_emv_log(amount):
    rows = []
    for step in EMV_HANDSHAKE_STEPS:
        if step["phase"] == "GET PROCESSING OPTIONS":
            value = f"{int(float(amount)*100):012d}"
        elif step["phase"] in ("FIRST GENERATE AC","SECOND GENERATE AC"):
            value = rHex(16)
        elif step["phase"] == "ONLINE AUTH REQUEST":
            value = rHex(8)
        else:
            value = step["static_value"]
        rows.append(f"{step['phase']}|{step['tag']}|{value}|{step['desc']}")
    return " || ".join(rows)

def build_record(i, merchant=None, overrides=None, edge_desc=""):
    m      = merchant or rand_merchant()
    card   = rand_card()
    method = rand_entry()
    amount = rand_amount(m)
    curr   = rand_currency()
    appr   = random.random() > 0.22
    dec    = rand_decline() if not appr else {}
    offline= random.random() < 0.10
    emv    = method in ["Chip","Contactless"]

    rec = {
        # ── Identity
        "record_id":                  i + 1,
        "txn_id":                     f"TXN-{rHex(10)}",
        "data_label":                 SYNTHETIC_LABEL,
        "edge_case_description":      edge_desc,

        # ── Timing
        "timestamp_utc":              ts(offset=i*7),
        "processing_time_ms":         ri(80, 3500),
        "timeout_ms":                 "",

        # ── Merchant
        "merchant_name":              m["name"],
        "merchant_mcc":               m["mcc"],
        "merchant_category":          m["category"],
        "merchant_city":              m["city"],
        "merchant_country":           m["country"],
        "merchant_lat":               m["lat"],
        "merchant_lng":               m["lng"],
        "merchant_avg_ticket":        m["avg_ticket"],
        "merchant_peak_hours":        m["peak_hours"],

        # ── Terminal
        "terminal_id":                f"T{ri(10000,99999)}",
        "terminal_make":              rand_terminal(),

        # ── Card
        "card_brand":                 card["card_brand"],
        "card_last4":                 card["card_last4"],
        "card_exp":                   card["card_exp"],
        "card_type":                  card["card_type"],
        "issuing_bank":               card["issuing_bank"],

        # ── Transaction
        "txn_type":                   "PURCHASE",
        "entry_method":               method,
        "amount":                     amount,
        "amount_authorized":          amount if appr else 0.00,
        "currency":                   curr,
        "fx_conversion":              curr != "GBP",
        "offline_auth":               offline,
        "store_and_forward":          offline and appr,
        "risk_flag":                  amount > 200 and offline,
        "fraud_score":                fraud_score(appr),
        "velocity_flag":              False,
        "duplicate":                  False,
        "retry_count":                0,

        # ── Auth result
        "status":                     "APPROVED" if appr else "DECLINED",
        "authorization_code":         rHex(6) if appr else "",
        "stan":                       str(ri(100000, 999999)),
        "rrn":                        rHex(12),
        "decline_code":               dec.get("code", ""),
        "decline_reason":             dec.get("label", ""),
        "decline_category":           dec.get("category", ""),
        "decline_retry_advised":      dec.get("retry_advised", ""),

        # ── EMV
        "emv_steps":                  build_emv_log(amount) if emv else "",

        # ── Receipt (CFPB Reg E)
        "receipt_merchant":           m["name"],
        "receipt_date":               ts(offset=i*7)[:10],
        "receipt_time":               ts(offset=i*7)[11:19],
        "receipt_currency":           curr,
        "receipt_amount":             f"{amount:.2f}",
        "receipt_auth_code":          rHex(6) if appr else "DECLINED",
        "receipt_terminal_id":        f"T{ri(10000,99999)}",

        # ── Edge case flags
        "partial_auth":               False,
        "fallback_swipe":             False,
        "emv_fallback":               False,
        "stand_in_approval":          False,
        "contactless_limit_exceeded": False,
        "voice_auth_required":        False,
        "fraud_block":                False,
        "pin_bypass":                 False,
        "cnp":                        False,
        "three_ds":                   False,
        "terminal_offline":           False,
        "cancellation_reason":        "",
        "error_code":                 "",
        "error_reason":               "",

        # ── Compliance
        "cfpb_compliant":             True,
        "source":                     SYNTHETIC_LABEL,
    }

    if overrides:
        rec.update(overrides)

    return rec

# ── BUILD MAIN DATASET (500 rows) ─────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  TITLE:   {TITLE}")
print(f"  ROWS:    {SAMPLE_ROWS} main + {EDGE_ROWS} edge cases")
print(f"  FIELDS:  {len(FIELDS)}")
print(f"  LABEL:   {SYNTHETIC_LABEL}")
print(f"{'='*60}\n")

print("Generating main dataset...")
main_records = []
for i in range(SAMPLE_ROWS):
    main_records.append(build_record(i))
print(f"  ✓ {len(main_records)} records")

# ── BUILD EDGE CASES (30 rows) ────────────────────────────────────────────────
print("Generating edge cases...")
edge_records = []
for i, ec in enumerate(EDGE_CASES[:EDGE_ROWS]):
    rec = build_record(SAMPLE_ROWS + i, overrides=ec["overrides"], edge_desc=ec["description"])
    rec["edge_case_id"]       = ec["id"]
    rec["edge_case_category"] = ec["category"]
    rec["edge_case_risk"]     = ec["risk_level"]
    edge_records.append(rec)
print(f"  ✓ {len(edge_records)} edge case records")

ALL_FIELDS = list(main_records[0].keys())

# ── BUILD DATA DICTIONARY ─────────────────────────────────────────────────────
data_dict = {
    "title":       TITLE,
    "disclaimer":  SYNTHETIC_LABEL,
    "generated":   ts(),
    "entities":    ENTITIES,
    "sample_rows": SAMPLE_ROWS,
    "edge_rows":   EDGE_ROWS,
    "field_count": len(ALL_FIELDS),
    "sources": [
        "CFPB Consumer Credit Reports (benchmark distributions)",
        "Federal Reserve Payments Study 2022 (entry method weights)",
        "EMVCo Book 3 — Application Specification v4.3 (EMV tags)",
        "ISO 18245 (MCC codes)",
        "ISO 3166-1 alpha-3 (country codes)",
        "ISO 4217 (currency codes)",
        "ISO 8583 (decline response codes)",
        "UK Finance Card Spending Report 2022 (card brand weights)",
    ],
    "entities_detail": {
        "Transaction":   {"record_count": SAMPLE_ROWS, "fields": FIELD_DEFINITIONS},
        "Merchant":      {"record_count": len(MERCHANTS),   "fields": {
            "name":          {"type":"string",  "description":"Synthetic merchant trading name"},
            "mcc":           {"type":"string",  "description":"ISO 18245 Merchant Category Code"},
            "category":      {"type":"string",  "description":"Human-readable MCC category"},
            "city":          {"type":"string",  "description":"City of merchant location"},
            "country":       {"type":"string",  "description":"ISO 3166-1 alpha-3 country code"},
            "lat":           {"type":"float",   "description":"WGS84 latitude for map rendering"},
            "lng":           {"type":"float",   "description":"WGS84 longitude for map rendering"},
            "avg_ticket":    {"type":"float",   "description":"Synthetic average transaction value (GBP)"},
            "peak_hours":    {"type":"string",  "description":"Peak trading hour ranges (24h)"},
        }},
        "Card":          {"record_count": len(CARD_BRANDS), "fields": {
            "brand":         {"type":"string",  "description":"Visa | Mastercard | Amex | Discover"},
            "last4":         {"type":"string",  "description":"Last 4 digits of synthetic PAN"},
            "exp":           {"type":"string",  "description":"Synthetic expiry MM/YY"},
            "type":          {"type":"string",  "description":"Credit | Debit | Prepaid"},
            "issuing_bank":  {"type":"string",  "description":"Synthetic UK issuing bank"},
        }},
        "Terminal":      {"record_count": len(TERMINAL_MANUFACTURERS), "fields": {
            "make":          {"type":"string",  "description":"Terminal manufacturer name"},
            "model":         {"type":"string",  "description":"Terminal model"},
            "nfc":           {"type":"boolean", "description":"Supports NFC contactless"},
            "emv":           {"type":"boolean", "description":"Supports EMV chip"},
            "magstripe":     {"type":"boolean", "description":"Supports magnetic stripe"},
            "pci_pts":       {"type":"string",  "description":"PCI PTS certification version"},
        }},
        "EMV_Handshake": {"record_count": len(EMV_HANDSHAKE_STEPS), "fields": {
            "phase":         {"type":"string",  "description":"EMV protocol phase name"},
            "tag":           {"type":"string",  "description":"EMV TLV tag (hex)"},
            "static_value":  {"type":"string",  "description":"Fixed value where applicable"},
            "desc":          {"type":"string",  "description":"Human-readable description"},
        }},
        "DeclineReason": {"record_count": len(DECLINE_REASONS), "fields": {
            "code":           {"type":"string",  "description":"ISO 8583 response code"},
            "label":          {"type":"string",  "description":"Standard decline label"},
            "category":       {"type":"string",  "description":"High-level decline category"},
            "pct":            {"type":"integer", "description":"Percentage of all declines"},
            "description":    {"type":"string",  "description":"Cardholder-facing explanation"},
            "retry_advised":  {"type":"boolean", "description":"True if retry may succeed"},
        }},
        "SAF_Queue":     {"record_count": "dynamic", "fields": {
            "local_id":       {"type":"string",  "description":"Local queue item ID (SAF-XXXXXX)"},
            "queued_at":      {"type":"datetime","description":"ISO 8601 timestamp when queued"},
            "amount":         {"type":"decimal", "description":"Transaction amount"},
            "status":         {"type":"string",  "description":"Always PENDING_SYNC"},
            "risk_flag":      {"type":"boolean", "description":"True if amount exceeds floor limit"},
            "offline_token":  {"type":"string",  "description":"32-char offline auth token"},
        }},
        "Receipt":       {"record_count": "per_transaction", "fields": {
            "merchant_name":  {"type":"string",  "description":"CFPB Reg E required field"},
            "date":           {"type":"date",    "description":"CFPB Reg E required field"},
            "time":           {"type":"time",    "description":"CFPB Reg E required field"},
            "currency":       {"type":"string",  "description":"CFPB Reg E required field"},
            "amount":         {"type":"string",  "description":"CFPB Reg E required field"},
            "auth_code":      {"type":"string",  "description":"CFPB Reg E required field"},
            "terminal_id":    {"type":"string",  "description":"CFPB Reg E required field"},
        }},
    },
    "decline_codes":       {d["code"]: {"label":d["label"],"category":d["category"],"pct":d["pct"],"retry_advised":d["retry_advised"]} for d in DECLINE_REASONS},
    "entry_method_weights":{e["method"]: e["weight"] for e in ENTRY_METHODS},
    "edge_case_scenarios": [{"id":e["id"],"description":e["description"],"category":e["category"],"risk_level":e["risk_level"]} for e in EDGE_CASES],
}

# ── WRITE FILES ───────────────────────────────────────────────────────────────
def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    size = os.path.getsize(path)
    print(f"  ✓ {os.path.basename(path):40s} {size//1024:>5} KB")

def write_csv(path, records, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(records)
    size = os.path.getsize(path)
    print(f"  ✓ {os.path.basename(path):40s} {size//1024:>5} KB")

print("\nWriting exports...")
write_json(f"{OUT}/data_dictionary.json",   data_dict)
write_json(f"{OUT}/transactions.json",      {"title":TITLE,"disclaimer":SYNTHETIC_LABEL,"generated":ts(),"sample_rows":SAMPLE_ROWS,"records":main_records})
write_csv( f"{OUT}/transactions.csv",       main_records,  ALL_FIELDS)
write_json(f"{OUT}/edge_cases.json",        {"title":TITLE,"disclaimer":SYNTHETIC_LABEL,"generated":ts(),"edge_rows":EDGE_ROWS,"records":edge_records})
write_csv( f"{OUT}/edge_cases.csv",         edge_records,  ALL_FIELDS)

# ── STATS ─────────────────────────────────────────────────────────────────────
from collections import Counter
statuses  = Counter(r["status"]       for r in main_records)
methods   = Counter(r["entry_method"] for r in main_records)
cities    = Counter(r["merchant_city"]for r in main_records)
offlines  = sum(1 for r in main_records if r["offline_auth"])
safs      = sum(1 for r in main_records if r["store_and_forward"])
avg_amt   = sum(r["amount"] for r in main_records) / len(main_records)

print(f"\n{'='*60}")
print(f"  DATASET STATISTICS")
print(f"{'='*60}")
print(f"  Total main records:   {SAMPLE_ROWS}")
print(f"  Total edge cases:     {EDGE_ROWS}")
print(f"  Fields per record:    {len(ALL_FIELDS)}")
print(f"  Approval rate:        {statuses['APPROVED']/SAMPLE_ROWS*100:.1f}%")
print(f"  Decline rate:         {statuses['DECLINED']/SAMPLE_ROWS*100:.1f}%")
print(f"  Avg transaction:      £{avg_amt:.2f}")
print(f"  Offline transactions: {offlines} ({offlines/SAMPLE_ROWS*100:.1f}%)")
print(f"  Store & Forward:      {safs} ({safs/SAMPLE_ROWS*100:.1f}%)")
print(f"\n  Entry method breakdown:")
for method, count in methods.most_common():
    print(f"    {method:<18} {count:>4} ({count/SAMPLE_ROWS*100:.1f}%)")
print(f"\n  Cities covered:       {len(cities)}")
for city, count in cities.most_common():
    print(f"    {city:<18} {count:>4} merchants")
print(f"\n  All records labeled:  '{SYNTHETIC_LABEL}'")
print(f"{'='*60}\n")
