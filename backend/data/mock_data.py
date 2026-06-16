"""
Real Rails — PoC #12 · POS Transaction Simulator
═══════════════════════════════════════════════════════════════════
MOCK DATA PACKAGE — ALL DATA IS SYNTHETIC
NOT REAL MERCHANT, CARD, OR TRANSACTION DATA
═══════════════════════════════════════════════════════════════════

Sources (benchmarks only):
  - CFPB Consumer Credit Reports
  - Federal Reserve Payments Study 2022
  - EMVCo Specification v4.3 (field reference)
  - ISO 18245 (MCC codes)
  - ISO 3166-1 (country codes)
  - ISO 4217 (currency codes)
  - ISO 8583 (decline response codes)
"""

SYNTHETIC_LABEL = "SYNTHETIC — NOT REAL TRANSACTION DATA"

# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: MERCHANTS
# Fields: name, mcc, category, city, country, lat, lng, avg_ticket, peak_hours
# Sample rows: 30
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — MERCHANTS
# name         : str  — Synthetic merchant trading name
# mcc          : str  — ISO 18245 Merchant Category Code
# category     : str  — Human-readable MCC category
# city         : str  — City of merchant location
# country      : str  — ISO 3166-1 alpha-3 country code
# lat          : float— WGS84 latitude for map rendering
# lng          : float— WGS84 longitude for map rendering
# avg_ticket   : float— Synthetic average transaction value (GBP)
# peak_hours   : str  — Comma-separated peak trading hour ranges (24h)

MERCHANTS = [
    # ── London ────────────────────────────────────────────────────────────────
    {"name": "Corner Deli",           "mcc": "5812", "category": "Food & Drink",  "city": "London",      "country": "GBR", "lat": 51.5074,  "lng": -0.1278,  "avg_ticket": 12.50,  "peak_hours": "07-09,12-14"},
    {"name": "Urban Coffee",          "mcc": "5812", "category": "Food & Drink",  "city": "London",      "country": "GBR", "lat": 51.5155,  "lng": -0.0922,  "avg_ticket": 6.80,   "peak_hours": "08-10,15-17"},
    {"name": "QuickMart",             "mcc": "5411", "category": "Grocery",       "city": "London",      "country": "GBR", "lat": 51.4994,  "lng": -0.1248,  "avg_ticket": 34.20,  "peak_hours": "17-20"},
    {"name": "The Food Hall",         "mcc": "5411", "category": "Grocery",       "city": "London",      "country": "GBR", "lat": 51.5033,  "lng": -0.1195,  "avg_ticket": 78.40,  "peak_hours": "11-14,17-19"},
    {"name": "Pharmacy Plus",         "mcc": "5912", "category": "Health",        "city": "London",      "country": "GBR", "lat": 51.5200,  "lng": -0.1350,  "avg_ticket": 22.10,  "peak_hours": "09-12"},
    {"name": "Fuel & Go",             "mcc": "5541", "category": "Fuel",          "city": "London",      "country": "GBR", "lat": 51.4900,  "lng": -0.1400,  "avg_ticket": 65.00,  "peak_hours": "07-09,17-19"},
    {"name": "BookNook",              "mcc": "5942", "category": "Books & Media",  "city": "London",      "country": "GBR", "lat": 51.5250,  "lng": -0.1050,  "avg_ticket": 18.90,  "peak_hours": "10-18"},
    {"name": "Electronics Hub",       "mcc": "5732", "category": "Electronics",   "city": "London",      "country": "GBR", "lat": 51.5080,  "lng": -0.0980,  "avg_ticket": 189.00, "peak_hours": "12-19"},
    {"name": "Garden Centre",         "mcc": "5261", "category": "Garden & Home", "city": "London",      "country": "GBR", "lat": 51.4850,  "lng": -0.1550,  "avg_ticket": 45.60,  "peak_hours": "10-16"},
    {"name": "Apparel & Co",          "mcc": "5651", "category": "Fashion",       "city": "London",      "country": "GBR", "lat": 51.5120,  "lng": -0.1420,  "avg_ticket": 72.30,  "peak_hours": "11-19"},
    {"name": "Waterloo Sandwiches",   "mcc": "5812", "category": "Food & Drink",  "city": "London",      "country": "GBR", "lat": 51.5031,  "lng": -0.1132,  "avg_ticket": 7.90,   "peak_hours": "12-14"},
    {"name": "Kings Cross Kiosk",     "mcc": "5994", "category": "Newsagent",     "city": "London",      "country": "GBR", "lat": 51.5309,  "lng": -0.1233,  "avg_ticket": 3.80,   "peak_hours": "06-09,16-19"},
    # ── Manchester ────────────────────────────────────────────────────────────
    {"name": "City Bakery",           "mcc": "5461", "category": "Food & Drink",  "city": "Manchester",  "country": "GBR", "lat": 53.4808,  "lng": -2.2426,  "avg_ticket": 8.40,   "peak_hours": "07-10"},
    {"name": "Northern Quarter Café", "mcc": "5812", "category": "Food & Drink",  "city": "Manchester",  "country": "GBR", "lat": 53.4837,  "lng": -2.2342,  "avg_ticket": 11.20,  "peak_hours": "08-11,12-15"},
    {"name": "Arndale Pharmacy",      "mcc": "5912", "category": "Health",        "city": "Manchester",  "country": "GBR", "lat": 53.4831,  "lng": -2.2386,  "avg_ticket": 19.40,  "peak_hours": "09-18"},
    # ── Birmingham ────────────────────────────────────────────────────────────
    {"name": "Metro Newsagent",       "mcc": "5994", "category": "Newsagent",     "city": "Birmingham",  "country": "GBR", "lat": 52.4862,  "lng": -1.8904,  "avg_ticket": 4.20,   "peak_hours": "06-09,17-20"},
    {"name": "Bullring Electronics",  "mcc": "5732", "category": "Electronics",   "city": "Birmingham",  "country": "GBR", "lat": 52.4775,  "lng": -1.8937,  "avg_ticket": 210.00, "peak_hours": "11-19"},
    {"name": "Brum Fuel Stop",        "mcc": "5541", "category": "Fuel",          "city": "Birmingham",  "country": "GBR", "lat": 52.4950,  "lng": -1.9000,  "avg_ticket": 58.00,  "peak_hours": "07-09,17-19"},
    # ── Edinburgh ─────────────────────────────────────────────────────────────
    {"name": "Station Café",          "mcc": "5812", "category": "Food & Drink",  "city": "Edinburgh",   "country": "GBR", "lat": 55.9533,  "lng": -3.1883,  "avg_ticket": 9.10,   "peak_hours": "08-10,12-14"},
    {"name": "Royal Mile Gifts",      "mcc": "5947", "category": "Gifts & Souvenirs","city":"Edinburgh",  "country": "GBR", "lat": 55.9500,  "lng": -3.1880,  "avg_ticket": 24.50,  "peak_hours": "10-18"},
    {"name": "Edinburgh Grocer",      "mcc": "5411", "category": "Grocery",       "city": "Edinburgh",   "country": "GBR", "lat": 55.9486,  "lng": -3.2000,  "avg_ticket": 41.30,  "peak_hours": "16-20"},
    # ── Leeds ─────────────────────────────────────────────────────────────────
    {"name": "TechZone",              "mcc": "5945", "category": "Electronics",   "city": "Leeds",       "country": "GBR", "lat": 53.8008,  "lng": -1.5491,  "avg_ticket": 145.00, "peak_hours": "12-19"},
    {"name": "Victoria Quarter Café", "mcc": "5812", "category": "Food & Drink",  "city": "Leeds",       "country": "GBR", "lat": 53.7997,  "lng": -1.5430,  "avg_ticket": 10.50,  "peak_hours": "09-11,12-14"},
    # ── Bristol ───────────────────────────────────────────────────────────────
    {"name": "Health Hub Pharmacy",   "mcc": "5912", "category": "Health",        "city": "Bristol",     "country": "GBR", "lat": 51.4545,  "lng": -2.5879,  "avg_ticket": 28.70,  "peak_hours": "09-13"},
    {"name": "Harbourside Deli",      "mcc": "5812", "category": "Food & Drink",  "city": "Bristol",     "country": "GBR", "lat": 51.4490,  "lng": -2.5990,  "avg_ticket": 14.30,  "peak_hours": "12-15"},
    # ── Glasgow ───────────────────────────────────────────────────────────────
    {"name": "Sauchiehall Sportswear","mcc": "5941", "category": "Sport & Leisure","city": "Glasgow",    "country": "GBR", "lat": 55.8617,  "lng": -4.2583,  "avg_ticket": 55.90,  "peak_hours": "10-18"},
    {"name": "Glasgow Central Kiosk", "mcc": "5994", "category": "Newsagent",     "city": "Glasgow",     "country": "GBR", "lat": 55.8583,  "lng": -4.2575,  "avg_ticket": 3.60,   "peak_hours": "06-09,17-20"},
    # ── Cardiff ───────────────────────────────────────────────────────────────
    {"name": "Bay Bookshop",          "mcc": "5942", "category": "Books & Media",  "city": "Cardiff",    "country": "GBR", "lat": 51.4638,  "lng": -3.1680,  "avg_ticket": 16.70,  "peak_hours": "10-18"},
    {"name": "Cardiff Market Grocer", "mcc": "5411", "category": "Grocery",       "city": "Cardiff",     "country": "GBR", "lat": 51.4800,  "lng": -3.1791,  "avg_ticket": 29.80,  "peak_hours": "09-17"},
    # ── Liverpool ─────────────────────────────────────────────────────────────
    {"name": "Albert Dock Café",      "mcc": "5812", "category": "Food & Drink",  "city": "Liverpool",   "country": "GBR", "lat": 53.4008,  "lng": -2.9960,  "avg_ticket": 13.40,  "peak_hours": "10-15"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: CARD BRANDS
# Fields: brand, weight, bin_prefix, network
# Sample rows: 4
# Weights sourced from UK Finance Card Spending Report 2022
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — CARD BRANDS
# brand       : str — Card network name
# weight      : int — Relative market share weight (sums to 100)
# bin_prefix  : str — First digit of synthetic card number
# network     : str — Processing network

CARD_BRANDS = [
    {"brand": "Visa",       "weight": 57, "bin_prefix": "4", "network": "VisaNet"},
    {"brand": "Mastercard", "weight": 32, "bin_prefix": "5", "network": "Banknet"},
    {"brand": "Amex",       "weight": 7,  "bin_prefix": "3", "network": "AmexNet"},
    {"brand": "Discover",   "weight": 4,  "bin_prefix": "6", "network": "PULSE"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: CARD TYPES
# Fields: type, weight, credit_limit_typical, overdraft_risk
# Sample rows: 3
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — CARD TYPES
# type                 : str   — Card funding type
# weight               : int   — Market share weight
# credit_limit_typical : float — Typical synthetic credit limit (GBP)
# overdraft_risk       : bool  — True if insufficient funds decline is common

CARD_TYPES = [
    {"type": "Credit",  "weight": 48, "credit_limit_typical": 3500.00, "overdraft_risk": False},
    {"type": "Debit",   "weight": 44, "credit_limit_typical": 0.00,    "overdraft_risk": True},
    {"type": "Prepaid", "weight": 8,  "credit_limit_typical": 0.00,    "overdraft_risk": True},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: ENTRY METHODS
# Fields: method, weight, emv, fraud_rate_bps, pin_required, description
# Sample rows: 4
# Weights: Federal Reserve Payments Study 2022
# Fraud rates: UK Finance Fraud Report 2022 (benchmarks)
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — ENTRY METHODS
# method          : str  — Terminal entry method name
# weight          : int  — Market share weight (sums to 100)
# emv             : bool — True if EMV chip handshake is performed
# fraud_rate_bps  : int  — Fraud rate in basis points per £1,000 transacted
# pin_required    : bool — True if PIN entry is typically required
# description     : str  — Human-readable description

ENTRY_METHODS = [
    {"method": "Contactless",  "weight": 41, "emv": True,  "fraud_rate_bps": 4,  "pin_required": False, "description": "NFC tap — EMV tokenised, no PIN under £100"},
    {"method": "Chip",         "weight": 38, "emv": True,  "fraud_rate_bps": 2,  "pin_required": True,  "description": "EMV chip insert with online PIN verification"},
    {"method": "Swipe",        "weight": 15, "emv": False, "fraud_rate_bps": 18, "pin_required": False, "description": "Magnetic stripe — no chip auth, higher fraud risk"},
    {"method": "Manual Entry", "weight": 6,  "emv": False, "fraud_rate_bps": 65, "pin_required": False, "description": "Card-not-present / MOTO — highest fraud risk"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: CURRENCIES
# Fields: code, symbol, weight, region
# Sample rows: 3
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — CURRENCIES
# code   : str — ISO 4217 currency code
# symbol : str — Currency symbol
# weight : int — Transaction share weight
# region : str — Primary region

CURRENCIES = [
    {"code": "GBP", "symbol": "£", "weight": 85, "region": "United Kingdom"},
    {"code": "USD", "symbol": "$", "weight": 10, "region": "United States"},
    {"code": "EUR", "symbol": "€", "weight": 5,  "region": "Eurozone"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: DECLINE REASONS
# Fields: code, label, category, pct, description, retry_advised
# Sample rows: 10
# Weights: CFPB Consumer Credit Reports (benchmark distributions)
# Codes: ISO 8583 response codes
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — DECLINE REASONS
# code          : str  — ISO 8583 response code
# label         : str  — Standard decline reason label
# category      : str  — High-level decline category
# pct           : int  — Percentage weight of all declines
# description   : str  — Explanation for the cardholder
# retry_advised : bool — True if retrying the transaction may succeed

DECLINE_REASONS = [
    {"code": "05", "label": "Do Not Honor",             "category": "Issuer Block",   "pct": 8,  "description": "Issuer has blocked this card for unspecified reasons",     "retry_advised": False},
    {"code": "14", "label": "Invalid Card Number",      "category": "Data Error",     "pct": 5,  "description": "Card PAN failed Luhn check or is not on file",            "retry_advised": False},
    {"code": "51", "label": "Insufficient Funds",       "category": "Balance",        "pct": 25, "description": "Available balance is below the transaction amount",       "retry_advised": False},
    {"code": "54", "label": "Expired Card",             "category": "Data Error",     "pct": 8,  "description": "Card expiry date has passed",                            "retry_advised": False},
    {"code": "55", "label": "Incorrect PIN",            "category": "Auth Failure",   "pct": 20, "description": "PIN entered does not match issuer record",               "retry_advised": True},
    {"code": "57", "label": "Transaction Not Permitted","category": "Issuer Block",   "pct": 7,  "description": "Transaction type not allowed for this card",             "retry_advised": False},
    {"code": "62", "label": "Restricted Card",          "category": "Issuer Block",   "pct": 5,  "description": "Card is on a restriction list (lost, stolen, fraud)",    "retry_advised": False},
    {"code": "76", "label": "Chip Read Error",          "category": "Hardware",       "pct": 8,  "description": "Terminal could not read the chip — try swipe fallback",  "retry_advised": True},
    {"code": "91", "label": "Bank Unavailable",         "category": "Network",        "pct": 9,  "description": "Issuer host is unreachable — offline auth may apply",    "retry_advised": True},
    {"code": "96", "label": "System Error",             "category": "Technical Error","pct": 5,  "description": "Acquirer or network system error — not card related",    "retry_advised": True},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: ISSUING BANKS (SYNTHETIC)
# Fields: name, country, bic_prefix, type
# Sample rows: 15
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — ISSUING BANKS
# name       : str — Synthetic bank name (not real institution)
# country    : str — ISO 3166-1 alpha-3
# bic_prefix : str — Synthetic BIC/SWIFT prefix (not real)
# type       : str — Traditional | Challenger | Building Society

ISSUING_BANKS = [
    {"name": "Barclays Bank",      "country": "GBR", "bic_prefix": "BARC", "type": "Traditional"},
    {"name": "HSBC UK",            "country": "GBR", "bic_prefix": "MIDL", "type": "Traditional"},
    {"name": "Lloyds Bank",        "country": "GBR", "bic_prefix": "LOYD", "type": "Traditional"},
    {"name": "NatWest",            "country": "GBR", "bic_prefix": "NWBK", "type": "Traditional"},
    {"name": "Santander UK",       "country": "GBR", "bic_prefix": "ABBG", "type": "Traditional"},
    {"name": "Monzo Bank",         "country": "GBR", "bic_prefix": "MONZ", "type": "Challenger"},
    {"name": "Starling Bank",      "country": "GBR", "bic_prefix": "SRLG", "type": "Challenger"},
    {"name": "Halifax",            "country": "GBR", "bic_prefix": "HLFX", "type": "Traditional"},
    {"name": "TSB Bank",           "country": "GBR", "bic_prefix": "TSBS", "type": "Traditional"},
    {"name": "Metro Bank",         "country": "GBR", "bic_prefix": "MYMB", "type": "Challenger"},
    {"name": "Nationwide BS",      "country": "GBR", "bic_prefix": "NAIA", "type": "Building Society"},
    {"name": "Virgin Money",       "country": "GBR", "bic_prefix": "CYBG", "type": "Traditional"},
    {"name": "Revolut",            "country": "GBR", "bic_prefix": "RVLT", "type": "Challenger"},
    {"name": "Chase UK",           "country": "GBR", "bic_prefix": "JPMC", "type": "Challenger"},
    {"name": "First Direct",       "country": "GBR", "bic_prefix": "FDUK", "type": "Challenger"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: TERMINAL MANUFACTURERS
# Fields: make, model, nfc, emv, magstripe, pci_pts
# Sample rows: 10
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — TERMINAL MANUFACTURERS
# make      : str  — Terminal manufacturer name
# model     : str  — Terminal model
# nfc       : bool — Supports NFC contactless
# emv       : bool — Supports EMV chip
# magstripe : bool — Supports magnetic stripe swipe
# pci_pts   : str  — PCI PTS certification version

TERMINAL_MANUFACTURERS = [
    {"make": "Verifone",  "model": "V400m",      "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "6.x"},
    {"make": "Ingenico",  "model": "Move 5000",  "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "6.x"},
    {"make": "PAX",       "model": "A920 Pro",   "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "5.x"},
    {"make": "Clover",    "model": "Flex",        "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "5.x"},
    {"make": "Square",    "model": "Terminal",    "nfc": True,  "emv": True,  "magstripe": False, "pci_pts": "5.x"},
    {"make": "Verifone",  "model": "V240m",       "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "5.x"},
    {"make": "Ingenico",  "model": "Desk 3500",   "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "6.x"},
    {"make": "PAX",       "model": "S920",        "nfc": False, "emv": True,  "magstripe": True,  "pci_pts": "4.x"},
    {"make": "Miura",     "model": "M010",        "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "5.x"},
    {"make": "Spire",     "model": "SPp10",       "nfc": True,  "emv": True,  "magstripe": True,  "pci_pts": "5.x"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: EDGE CASES
# 30 realistic error states and unusual transaction scenarios
# Fields: id, description, category, overrides, risk_level
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — EDGE CASES
# id          : int  — Unique edge case identifier
# description : str  — Human-readable scenario description
# category    : str  — Edge case category
# overrides   : dict — Field overrides applied to a base transaction record
# risk_level  : str  — Low | Medium | High | Critical

EDGE_CASES = [
    {
        "id": 1, "description": "Zero amount transaction",
        "category": "Validation Error", "risk_level": "Medium",
        "overrides": {"amount_usd": 0.00, "status": "DECLINED", "decline_code": "57", "decline_reason": "Transaction Not Permitted"},
    },
    {
        "id": 2, "description": "Maximum floor limit exceeded — Store & Forward",
        "category": "Offline Auth", "risk_level": "High",
        "overrides": {"amount_usd": 999.99, "offline_auth": True, "status": "APPROVED", "store_and_forward": True, "risk_flag": True},
    },
    {
        "id": 3, "description": "Duplicate transaction — same card, amount, merchant within 60s",
        "category": "Fraud Signal", "risk_level": "High",
        "overrides": {"status": "APPROVED", "duplicate": True, "fraud_score": 78},
    },
    {
        "id": 4, "description": "Expired card presented at terminal",
        "category": "Data Error", "risk_level": "Low",
        "overrides": {"card_exp": "01/20", "status": "DECLINED", "decline_code": "54", "decline_reason": "Expired Card"},
    },
    {
        "id": 5, "description": "Chip read failure — fallback to magnetic stripe",
        "category": "Hardware Fallback", "risk_level": "Medium",
        "overrides": {"entry_method": "Swipe", "status": "APPROVED", "fallback_swipe": True, "emv_fallback": True},
    },
    {
        "id": 6, "description": "Partial authorisation — pre-paid card insufficient balance",
        "category": "Partial Auth", "risk_level": "Low",
        "overrides": {"amount_usd": 150.00, "amount_authorized": 80.00, "partial_auth": True, "status": "PARTIAL"},
    },
    {
        "id": 7, "description": "Network timeout — offline authorisation applied",
        "category": "Offline Auth", "risk_level": "Medium",
        "overrides": {"offline_auth": True, "status": "APPROVED", "store_and_forward": True, "timeout_ms": 9999, "processing_time_ms": 9999},
    },
    {
        "id": 8, "description": "Foreign currency transaction with DCC",
        "category": "FX Conversion", "risk_level": "Low",
        "overrides": {"currency": "EUR", "fx_conversion": True, "status": "APPROVED"},
    },
    {
        "id": 9, "description": "Manual entry CNP — high fraud score triggered",
        "category": "Fraud Signal", "risk_level": "Critical",
        "overrides": {"entry_method": "Manual Entry", "fraud_score": 92, "status": "DECLINED", "decline_code": "05", "decline_reason": "Do Not Honor"},
    },
    {
        "id": 10, "description": "Contactless floor limit exceeded — PIN required",
        "category": "Limit Exceeded", "risk_level": "Medium",
        "overrides": {"entry_method": "Contactless", "amount_usd": 250.00, "status": "DECLINED", "decline_code": "57", "decline_reason": "Transaction Not Permitted", "contactless_limit_exceeded": True},
    },
    {
        "id": 11, "description": "Transaction cancelled by cardholder before completion",
        "category": "Cancellation", "risk_level": "Low",
        "overrides": {"status": "CANCELLED", "cancellation_reason": "Cardholder pressed cancel at PIN entry"},
    },
    {
        "id": 12, "description": "Refund transaction processed at terminal",
        "category": "Refund", "risk_level": "Low",
        "overrides": {"txn_type": "REFUND", "amount_usd": -45.00, "status": "APPROVED"},
    },
    {
        "id": 13, "description": "Voice authorisation required — issuer referral",
        "category": "Manual Override", "risk_level": "High",
        "overrides": {"status": "DECLINED", "decline_code": "01", "decline_reason": "Refer to Card Issuer", "voice_auth_required": True},
    },
    {
        "id": 14, "description": "PIN bypass on contactless — low-value transaction",
        "category": "PIN Bypass", "risk_level": "Low",
        "overrides": {"entry_method": "Contactless", "pin_bypass": True, "status": "APPROVED"},
    },
    {
        "id": 15, "description": "Card blocked due to confirmed fraud",
        "category": "Fraud Block", "risk_level": "Critical",
        "overrides": {"status": "DECLINED", "decline_code": "62", "decline_reason": "Restricted Card", "fraud_block": True, "fraud_score": 99},
    },
    {
        "id": 16, "description": "Acquirer host timeout — terminal error state",
        "category": "System Error", "risk_level": "Medium",
        "overrides": {"status": "ERROR", "error_code": "T001", "error_reason": "Acquirer host connection timed out", "processing_time_ms": 30000},
    },
    {
        "id": 17, "description": "End-of-day batch settlement failure",
        "category": "Settlement Error", "risk_level": "High",
        "overrides": {"status": "ERROR", "error_code": "B001", "error_reason": "Batch settlement rejected by acquirer"},
    },
    {
        "id": 18, "description": "EMV chip processing failed — fallback to magstripe",
        "category": "Hardware Fallback", "risk_level": "Medium",
        "overrides": {"entry_method": "Swipe", "emv_fallback": True, "status": "APPROVED"},
    },
    {
        "id": 19, "description": "High velocity — 5 transactions in 3 minutes on same card",
        "category": "Fraud Signal", "risk_level": "Critical",
        "overrides": {"fraud_score": 88, "velocity_flag": True, "status": "DECLINED", "decline_code": "05", "decline_reason": "Do Not Honor"},
    },
    {
        "id": 20, "description": "Issuer unavailable — acquirer stand-in approval",
        "category": "Offline Auth", "risk_level": "Medium",
        "overrides": {"offline_auth": True, "stand_in_approval": True, "status": "APPROVED"},
    },
    {
        "id": 21, "description": "Amount mismatch between terminal and authorisation",
        "category": "Validation Error", "risk_level": "Medium",
        "overrides": {"amount_usd": 100.00, "amount_authorized": 99.00, "status": "DECLINED", "decline_code": "13", "decline_reason": "Invalid Amount"},
    },
    {
        "id": 22, "description": "Card-not-present e-commerce with 3D Secure authentication",
        "category": "CNP / 3DS", "risk_level": "Low",
        "overrides": {"entry_method": "Manual Entry", "cnp": True, "three_ds": True, "status": "APPROVED"},
    },
    {
        "id": 23, "description": "Pre-authorisation hold — hotel check-in",
        "category": "Pre-Auth", "risk_level": "Low",
        "overrides": {"txn_type": "PRE_AUTH", "amount_usd": 200.00, "status": "APPROVED"},
    },
    {
        "id": 24, "description": "Pre-authorisation completion — final billing",
        "category": "Pre-Auth", "risk_level": "Low",
        "overrides": {"txn_type": "COMPLETION", "amount_usd": 187.50, "status": "APPROVED"},
    },
    {
        "id": 25, "description": "Void transaction — same-day reversal",
        "category": "Void", "risk_level": "Low",
        "overrides": {"txn_type": "VOID", "status": "APPROVED"},
    },
    {
        "id": 26, "description": "Multiple declined retries — insufficient funds",
        "category": "Retry Pattern", "risk_level": "Medium",
        "overrides": {"retry_count": 3, "status": "DECLINED", "decline_code": "51", "decline_reason": "Insufficient Funds"},
    },
    {
        "id": 27, "description": "Unsupported currency at terminal",
        "category": "Validation Error", "risk_level": "Low",
        "overrides": {"currency": "JPY", "status": "DECLINED", "decline_code": "57", "decline_reason": "Transaction Not Permitted"},
    },
    {
        "id": 28, "description": "Terminal fully offline — no network connectivity",
        "category": "Offline Auth", "risk_level": "High",
        "overrides": {"offline_auth": True, "terminal_offline": True, "status": "APPROVED", "store_and_forward": True},
    },
    {
        "id": 29, "description": "Chip and PIN success after initial contactless decline",
        "category": "Retry Pattern", "risk_level": "Low",
        "overrides": {"retry_count": 1, "entry_method": "Chip", "status": "APPROVED"},
    },
    {
        "id": 30, "description": "Stolen card — confirmed on hot list",
        "category": "Fraud Block", "risk_level": "Critical",
        "overrides": {"status": "DECLINED", "decline_code": "43", "decline_reason": "Stolen Card", "fraud_block": True, "fraud_score": 100},
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — TRANSACTION FIELDS (57 fields)
# Used by generate.py and main.py for documentation and validation
# ══════════════════════════════════════════════════════════════════════════════

FIELD_DEFINITIONS = {
    "record_id":                 {"type": "integer",  "description": "Sequential record number"},
    "txn_id":                    {"type": "string",   "description": "Unique synthetic transaction ID (TXN-XXXXXXXXXX)"},
    "data_label":                {"type": "string",   "description": "Always 'SYNTHETIC — NOT REAL TRANSACTION DATA'"},
    "edge_case":                 {"type": "string",   "description": "Edge case description if applicable"},
    "timestamp_utc":             {"type": "datetime", "description": "ISO 8601 UTC transaction timestamp"},
    "processing_time_ms":        {"type": "integer",  "description": "End-to-end processing time in milliseconds"},
    "timeout_ms":                {"type": "integer",  "description": "Timeout value for edge cases"},
    "merchant_name":             {"type": "string",   "description": "Synthetic merchant trading name"},
    "merchant_mcc":              {"type": "string",   "description": "ISO 18245 Merchant Category Code"},
    "merchant_category":         {"type": "string",   "description": "Human-readable MCC category"},
    "merchant_city":             {"type": "string",   "description": "Merchant city"},
    "merchant_country":          {"type": "string",   "description": "ISO 3166-1 alpha-3 country code"},
    "merchant_lat":              {"type": "float",    "description": "WGS84 latitude"},
    "merchant_lng":              {"type": "float",    "description": "WGS84 longitude"},
    "terminal_id":               {"type": "string",   "description": "Synthetic terminal identifier"},
    "terminal_make":             {"type": "string",   "description": "Terminal manufacturer and model"},
    "card_brand":                {"type": "string",   "description": "Visa | Mastercard | Amex | Discover"},
    "card_last4":                {"type": "string",   "description": "Last 4 digits of synthetic card PAN"},
    "card_exp":                  {"type": "string",   "description": "Synthetic card expiry MM/YY"},
    "card_type":                 {"type": "string",   "description": "Credit | Debit | Prepaid"},
    "issuing_bank":              {"type": "string",   "description": "Synthetic issuing bank name"},
    "txn_type":                  {"type": "string",   "description": "PURCHASE | REFUND | PRE_AUTH | COMPLETION | VOID"},
    "entry_method":              {"type": "string",   "description": "Contactless | Chip | Swipe | Manual Entry"},
    "amount_usd":                {"type": "decimal",  "description": "Transaction amount in base currency"},
    "amount_authorized":         {"type": "decimal",  "description": "Amount actually authorized"},
    "currency":                  {"type": "string",   "description": "ISO 4217 currency code"},
    "fx_conversion":             {"type": "boolean",  "description": "True if foreign currency conversion applied"},
    "offline_auth":              {"type": "boolean",  "description": "True if authorized offline"},
    "store_and_forward":         {"type": "boolean",  "description": "True if queued for replay on reconnect"},
    "risk_flag":                 {"type": "boolean",  "description": "True if high-value offline — manual review required"},
    "fraud_score":               {"type": "integer",  "description": "Synthetic fraud risk score 0–100"},
    "velocity_flag":             {"type": "boolean",  "description": "True if high transaction velocity detected"},
    "duplicate":                 {"type": "boolean",  "description": "True if suspected duplicate"},
    "retry_count":               {"type": "integer",  "description": "Number of retry attempts"},
    "status":                    {"type": "string",   "description": "APPROVED | DECLINED | CANCELLED | ERROR | PARTIAL"},
    "authorization_code":        {"type": "string",   "description": "6-character auth code (approved only)"},
    "stan":                      {"type": "string",   "description": "System Trace Audit Number"},
    "rrn":                       {"type": "string",   "description": "Retrieval Reference Number"},
    "decline_code":              {"type": "string",   "description": "ISO 8583 response code"},
    "decline_reason":            {"type": "string",   "description": "Human-readable decline reason"},
    "decline_category":          {"type": "string",   "description": "Balance | Auth Failure | Issuer Block | Data Error | Hardware | Network | Technical"},
    "emv_handshake":             {"type": "json",     "description": "EMV chip protocol steps (Chip/Contactless only)"},
    "receipt_merchant":          {"type": "string",   "description": "Merchant name on receipt (CFPB Reg E)"},
    "receipt_date":              {"type": "date",     "description": "Transaction date on receipt (CFPB Reg E)"},
    "receipt_time":              {"type": "time",     "description": "Transaction time on receipt (CFPB Reg E)"},
    "receipt_amount":            {"type": "string",   "description": "Formatted amount on receipt (CFPB Reg E)"},
    "receipt_auth_code":         {"type": "string",   "description": "Auth code on receipt (CFPB Reg E)"},
    "partial_auth":              {"type": "boolean",  "description": "True if partial authorization"},
    "fallback_swipe":            {"type": "boolean",  "description": "True if chip failed and fell back to swipe"},
    "emv_fallback":              {"type": "boolean",  "description": "True if EMV fell back to magstripe"},
    "stand_in_approval":         {"type": "boolean",  "description": "True if acquirer stand-in approval"},
    "contactless_limit_exceeded":{"type": "boolean",  "description": "True if contactless floor limit exceeded"},
    "voice_auth_required":       {"type": "boolean",  "description": "True if voice authorization required"},
    "fraud_block":               {"type": "boolean",  "description": "True if blocked by fraud detection"},
    "pin_bypass":                {"type": "boolean",  "description": "True if PIN verification bypassed"},
    "cnp":                       {"type": "boolean",  "description": "True if card-not-present"},
    "three_ds":                  {"type": "boolean",  "description": "True if 3D Secure authentication used"},
    "terminal_offline":          {"type": "boolean",  "description": "True if terminal had no network"},
    "cancellation_reason":       {"type": "string",   "description": "Cancellation reason if applicable"},
    "error_code":                {"type": "string",   "description": "System error code if applicable"},
    "error_reason":              {"type": "string",   "description": "System error description"},
    "cfpb_compliant":            {"type": "boolean",  "description": "True if all CFPB Reg E fields present"},
    "source":                    {"type": "string",   "description": "Always 'SYNTHETIC — NOT REAL TRANSACTION DATA'"},
}


# ══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE — pre-built weighted pools for random sampling
# ══════════════════════════════════════════════════════════════════════════════

CARD_BRAND_POOL   = [c["brand"]  for c in CARD_BRANDS    for _ in range(c["weight"])]
CARD_TYPE_POOL    = [c["type"]   for c in CARD_TYPES      for _ in range(c["weight"])]
ENTRY_METHOD_POOL = [e["method"] for e in ENTRY_METHODS   for _ in range(e["weight"])]
CURRENCY_POOL     = [c["code"]   for c in CURRENCIES       for _ in range(c["weight"])]
DECLINE_POOL      = [r           for r in DECLINE_REASONS  for _ in range(r["pct"])]
ISSUING_BANK_POOL = [b["name"]   for b in ISSUING_BANKS]
TERMINAL_POOL     = [f"{t['make']} {t['model']}" for t in TERMINAL_MANUFACTURERS]


# ══════════════════════════════════════════════════════════════════════════════
# ENTITY: EMV HANDSHAKE TEMPLATE
# Fields: phase, tag, static_value, desc
# Rows: 10 — one per EMV protocol step
# Source: EMVCo Book 3 — Application Specification v4.3
# Note: value_fn is excluded here (uses uuid/runtime values).
#       Use static_value for documentation; main.py injects runtime values.
# ══════════════════════════════════════════════════════════════════════════════
# DATA DICTIONARY — EMV HANDSHAKE STEPS
# phase        : str — EMV protocol phase name
# tag          : str — EMV TLV tag identifier (hex)
# static_value : str — Fixed value where applicable; empty if runtime-generated
# desc         : str — Human-readable description of the tag/value

EMV_HANDSHAKE_STEPS = [
    {"phase": "SELECT APPLICATION",      "tag": "84",   "static_value": "A0000000031010", "desc": "AID — Visa Credit"},
    {"phase": "GET PROCESSING OPTIONS",  "tag": "9F02", "static_value": "",               "desc": "Amount encoded (cents) — runtime value"},
    {"phase": "READ RECORD",             "tag": "5F28", "static_value": "0840",           "desc": "Issuer Country Code: GBR"},
    {"phase": "OFFLINE DATA AUTH",       "tag": "9F27", "static_value": "40",             "desc": "TC — Transaction Cert"},
    {"phase": "CARDHOLDER VERIFICATION", "tag": "9F34", "static_value": "420300",         "desc": "CVM: Online PIN"},
    {"phase": "TERMINAL RISK MGMT",      "tag": "9F1A", "static_value": "0826",           "desc": "Terminal Country: GBR"},
    {"phase": "FIRST GENERATE AC",       "tag": "9F26", "static_value": "",               "desc": "Application Cryptogram — runtime UUID"},
    {"phase": "ONLINE AUTH REQUEST",     "tag": "9F37", "static_value": "",               "desc": "Unpredictable Number — runtime UUID"},
    {"phase": "ISSUER RESPONSE",         "tag": "8A",   "static_value": "3030",           "desc": "Auth Response: 00 Approved"},
    {"phase": "SECOND GENERATE AC",      "tag": "9F26", "static_value": "",               "desc": "TC — Transaction Completed — runtime UUID"},
]


# ── Runtime constants used in main.py ─────────────────────────────────────────
DEFAULT_ENTRY_METHOD = "Contactless"
EMV_ENTRY_METHODS    = ["Chip", "Contactless"]   # methods that trigger EMV handshake
