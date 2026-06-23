'use client';
/**
 * lib/store.tsx
 * Lightweight React context that holds session state:
 * transactions, SAF queue, metrics, offline mode, API health.
 */
import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { Transaction, SafItem, EntryMethod, APIMode } from '@/types';

// ─── State ────────────────────────────────────────────────────────────────────

interface AppState {
  apiMode:    APIMode;
  offline:    boolean;
  method:     EntryMethod;
  receipts:   Transaction[];
  saf:        SafItem[];
  txn:        number;
  rev:        number;
  approvals:  number;
  declines:   number;
}

const initial: AppState = {
  apiMode:   'mock',
  offline:   false,
  method:    'Contactless',
  receipts:  [],
  saf:       [],
  txn:       0,
  rev:       0,
  approvals: 0,
  declines:  0,
};

// ─── Actions ─────────────────────────────────────────────────────────────────

type Action =
  | { type: 'SET_API_MODE';  payload: APIMode }
  | { type: 'SET_OFFLINE';   payload: boolean }
  | { type: 'SET_METHOD';    payload: EntryMethod }
  | { type: 'ADD_TXN';       payload: Transaction }
  | { type: 'ADD_SAF';       payload: SafItem };

function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_API_MODE': return { ...state, apiMode: action.payload };
    case 'SET_OFFLINE':  return { ...state, offline: action.payload };
    case 'SET_METHOD':   return { ...state, method:  action.payload };
    case 'ADD_TXN': {
      const t = action.payload;
      return {
        ...state,
        receipts:  [t, ...state.receipts],
        txn:       state.txn + 1,
        rev:       t.approved ? state.rev + parseFloat(t.amt) : state.rev,
        approvals: t.approved ? state.approvals + 1 : state.approvals,
        declines:  t.approved ? state.declines     : state.declines + 1,
      };
    }
    case 'ADD_SAF':
      return { ...state, saf: [action.payload, ...state.saf] };
    default:
      return state;
  }
}

// ─── Context ─────────────────────────────────────────────────────────────────

interface AppCtx {
  state:       AppState;
  setApiMode:  (m: APIMode)     => void;
  setOffline:  (v: boolean)     => void;
  setMethod:   (m: EntryMethod) => void;
  addTxn:      (t: Transaction) => void;
  addSaf:      (s: SafItem)     => void;
}

const Ctx = createContext<AppCtx | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initial);
  const setApiMode = useCallback((m: APIMode)     => dispatch({ type: 'SET_API_MODE', payload: m }), []);
  const setOffline = useCallback((v: boolean)     => dispatch({ type: 'SET_OFFLINE',  payload: v }), []);
  const setMethod  = useCallback((m: EntryMethod) => dispatch({ type: 'SET_METHOD',   payload: m }), []);
  const addTxn     = useCallback((t: Transaction) => dispatch({ type: 'ADD_TXN',      payload: t }), []);
  const addSaf     = useCallback((s: SafItem)     => dispatch({ type: 'ADD_SAF',      payload: s }), []);
  return (
    <Ctx.Provider value={{ state, setApiMode, setOffline, setMethod, addTxn, addSaf }}>
      {children}
    </Ctx.Provider>
  );
}

export function useApp(): AppCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useApp must be used inside <AppProvider>');
  return ctx;
}
