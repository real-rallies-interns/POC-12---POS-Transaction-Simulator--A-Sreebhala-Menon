# Real Rails · PoC #12 · POS Transaction Simulator
**Group 1: Geographic (Satellite View) · Obsidian DNA #030712 · 70/30 Split**

---

## What's in this zip

```
poc12/
├── backend/                    FastAPI — synthetic terminal event engine
│   ├── main.py                 All 7 API endpoints
│   ├── requirements.txt        pip dependencies
│   └── .env                    CORS origins + port config
│
├── frontend/
│   ├── standalone/
│   │   └── poc12_pos_simulator.html   Self-contained HTML — open directly in browser
│   │                                  Auto-connects to backend; falls back to mock data
│   │
│   ├── app/                    Next.js 14 App Router
│   │   ├── globals.css         Obsidian DNA CSS variables + Tailwind base
│   │   ├── layout.tsx          Root layout wrapping AppProvider
│   │   └── page.tsx            Root page (Header + Stage + Sidebar)
│   │
│   ├── components/
│   │   ├── shared/
│   │   │   ├── Header.tsx      Sticky header — API health indicator + live clock
│   │   │   ├── Stage.tsx       70% pane — tab bar + tab routing
│   │   │   └── Sidebar.tsx     30% pane — Sections A–E
│   │   ├── terminal/
│   │   │   ├── TerminalPane.tsx       Orchestrates full transaction flow
│   │   │   ├── EntryMethodGrid.tsx    4-button entry method selector
│   │   │   ├── TerminalScreen.tsx     POS display component
│   │   │   ├── EmvLog.tsx             Animated EMV chip handshake log
│   │   │   └── ResultCard.tsx         Transaction result display
│   │   ├── analytics/
│   │   │   └── AnalyticsPane.tsx      Decline donut + bar + entry stats
│   │   ├── receipts/
│   │   │   └── ReceiptsPane.tsx       CFPB-compliant receipt log table
│   │   └── offline/
│   │       └── OfflinePane.tsx        Store-and-Forward queue
│   │
│   ├── lib/
│   │   ├── adapters.ts         All FastAPI calls — auto-fallback to mock on error
│   │   ├── mock.ts             Synthetic data generators + EMV template
│   │   └── store.tsx           React context + useReducer session state
│   │
│   ├── types/index.ts          All TypeScript interfaces
│   ├── .env.local              NEXT_PUBLIC_API_URL=http://localhost:8000
│   ├── next.config.ts          API rewrite: /api/backend/* → FastAPI
│   ├── tailwind.config.ts      RR colour palette as rr-* Tailwind tokens
│   ├── tsconfig.json
│   ├── postcss.config.js
│   └── package.json
│
└── README.md                   ← you are here
```

---

## Quick Start

### Option A — Standalone (no install needed)
1. Start the backend (optional — app works without it):
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```
2. Open `frontend/standalone/poc12_pos_simulator.html` directly in your browser.
   The header shows **LIVE API** (green) when the backend is running,
   **MOCK DATA** (amber) when it isn't — every action auto-falls back.

### Option B — Full Next.js Dev Server
1. Start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   # → http://localhost:3000
   ```

---

## API Reference

| Method | Endpoint                              | Description                          |
|--------|---------------------------------------|--------------------------------------|
| GET    | `/health`                             | Health probe                         |
| POST   | `/api/transaction/initiate`           | Full transaction lifecycle + EMV     |
| GET    | `/api/transactions/history`           | Filterable historical batch          |
| GET    | `/api/analytics/decline-breakdown`    | CFPB-weighted decline distribution   |
| GET    | `/api/analytics/entry-method-stats`   | Fed Reserve entry method benchmarks  |
| GET    | `/api/offline/pending`                | Store-and-Forward queue              |
| GET    | `/api/sample-data`                    | 20-record downloadable JSON dataset  |

---

## DNA Compliance

| Constraint                         | Status |
|------------------------------------|--------|
| Background `#030712` Obsidian      | ✅     |
| 70% Stage / 30% Sidebar split      | ✅     |
| Sidebar Sections A–E               | ✅     |
| Group 1 — Geographic archetype     | ✅     |
| Filters update without page reload | ✅     |
| API → mock auto-fallback guardrail | ✅     |
| CFPB / Reg E receipt fields        | ✅     |
| Fed Reserve benchmark data         | ✅     |
| EMV handshake animated log         | ✅     |
| Store-and-Forward offline queue    | ✅     |

---

*Synthetic data only. Not real transaction records.*
*Sources: CFPB Consumer Credit Reports · Federal Reserve Payments Study 2022*
