export type EntryMethod = 'Contactless' | 'Chip' | 'Swipe' | 'Manual Entry';
export type TxnStatus   = 'APPROVED' | 'DECLINED';
export type APIMode     = 'live' | 'mock';

export interface Card {
  brand: string;
  last4: string;
  exp?:  string;
}
export interface DeclineReason {
  code: string; label: string; category: string;
}
export interface EmvStep {
  phase: string; tag: string; value: string; desc: string;
}
export interface Transaction {
  id: string; time: string; merchant: string; amt: string;
  card: Card; method: EntryMethod; approved: boolean;
  decline: DeclineReason | null; auth: string;
  emv: EmvStep[]; storeForward: boolean;
}
export interface SafItem {
  id: string; amt: string; card: Card; time: string; risk: boolean;
}
export interface APITransaction {
  transaction_id: string; timestamp: string; merchant: string;
  amount: number; currency: string;
  card: { brand: string; last4: string; exp: string; entry_method: string };
  status: TxnStatus; offline_mode: boolean;
  authorization_code: string | null;
  decline_reason: DeclineReason | null;
  store_and_forward: boolean; emv_handshake: EmvStep[];
  receipt_fields: Record<string, unknown>;
}
export interface APIDeclineBreakdown {
  total_declines: number;
  breakdown: Array<{ code: string; label: string; category: string; count: number; percentage: number }>;
  category_rollup: Array<{ category: string; count: number }>;
  source: string;
}
export interface APIEntryStats {
  stats: Array<{ method: string; share: number; trend: string; avg_ticket: number; fraud_rate_bps: number }>;
  source: string;
}
export interface APISampleData {
  dataset: string; poc: string; generated: string;
  records: Record<string, unknown>[];
}
export interface SessionMetrics {
  txn: number; rev: number; approvals: number; declines: number;
}
