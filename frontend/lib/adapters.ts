/**
 * lib/adapters.ts
 * All FastAPI calls live here.
 * Every function auto-falls back to mock data if the API is unreachable.
 */
import type {
  APITransaction, APIDeclineBreakdown, APIEntryStats, APISampleData, Transaction, EntryMethod,
} from '@/types';
import { buildMockTransaction, rHex, rAmt, rCard, rMerch, rDecline, buildSampleRecords } from './mock';

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const TIMEOUT_MS = 4000;

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(`${BASE}${path}`, {
      ...init,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!res.ok) return null;
    return res.json() as Promise<T>;
  } catch {
    return null;
  }
}

/** Probe /health — returns true if API is reachable */
export async function probeHealth(): Promise<boolean> {
  const data = await apiFetch<{ status: string }>('/health');
  return data?.status === 'ok';
}

/** Initiate a transaction — falls back to mock on failure */
export async function initiateTransaction(
  method: EntryMethod,
  offline: boolean,
): Promise<Transaction> {
  const params = new URLSearchParams({ entry_method: method, offline_mode: String(offline) });
  const data = await apiFetch<APITransaction>(`/api/transaction/initiate?${params}`, { method: 'POST' });

  if (!data) return buildMockTransaction(method);

  return {
    id:           data.transaction_id,
    time:         new Date(data.timestamp).toTimeString().slice(0, 8),
    merchant:     data.merchant,
    amt:          data.amount.toFixed(2),
    card:         { brand: data.card.brand, last4: data.card.last4 },
    method,
    approved:     data.status === 'APPROVED',
    decline:      data.decline_reason,
    auth:         data.authorization_code ?? '',
    emv:          data.emv_handshake ?? [],
    storeForward: data.store_and_forward,
  };
}

/** Decline breakdown analytics — falls back to static mock */
export async function fetchDeclineBreakdown(): Promise<APIDeclineBreakdown | null> {
  return apiFetch<APIDeclineBreakdown>('/api/analytics/decline-breakdown');
}

/** Entry method stats — falls back to static mock in component */
export async function fetchEntryStats(): Promise<APIEntryStats | null> {
  return apiFetch<APIEntryStats>('/api/analytics/entry-method-stats');
}

/** Sample data download — falls back to locally built mock */
export async function fetchSampleData(): Promise<Record<string, unknown>[]> {
  const data = await apiFetch<APISampleData>('/api/sample-data');
  return data?.records ?? buildSampleRecords(20);
}

/** Trigger sample-data download as JSON file in the browser */
export function downloadJSON(records: Record<string, unknown>[]): void {
  const payload = {
    dataset:    'POS Transaction Simulator — Sample Data',
    poc:        '12',
    generated:  new Date().toISOString(),
    disclaimer: 'Synthetic data only. Not real transaction records.',
    sources:    ['CFPB Consumer Credit Reports', 'Federal Reserve Payments Study 2022'],
    records,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'real_rails_poc12_sample_data.json';
  a.click();
  URL.revokeObjectURL(url);
}
