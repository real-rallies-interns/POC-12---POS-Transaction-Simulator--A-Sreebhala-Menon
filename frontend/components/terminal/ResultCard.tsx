'use client';
import type { Transaction } from '@/types';

interface Props { txn: Transaction; offline: boolean }

export default function ResultCard({ txn, offline }: Props) {
  return (
    <div style={{
      background: 'var(--surface)', border: '1px solid var(--border)',
      borderRadius: 12, padding: 14, animation: 'fadeUp .3s ease forwards',
    }}>
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 10 }}>
        Transaction Result
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px 10px', fontSize: 11 }}>
        <Row label="Transaction ID" value={txn.id} />
        <Row label="Amount"         value={`$${txn.amt}`} />
        <Row label="Merchant"       value={txn.merchant} mono={false} />
        <Row label="Card"           value={`${txn.card.brand} ••••${txn.card.last4}`} />
        <Row label="Entry Method"   value={txn.method} mono={false} />
        <Row label="Status"
          value={txn.approved ? 'APPROVED' : `DECLINED — ${txn.decline?.label}`}
          color={txn.approved ? 'var(--green)' : 'var(--red)'}
          bold
        />
        {txn.approved && <Row label="Auth Code" value={txn.auth} color="var(--cyan)" />}
        {txn.approved && offline && <Row label="Queue" value="Store & Forward — awaiting sync" color="var(--amber)" bold />}
      </div>
      <style>{`@keyframes fadeUp{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}`}</style>
    </div>
  );
}

function Row({ label, value, mono = true, color = 'var(--text)', bold = false }: {
  label: string; value: string; mono?: boolean; color?: string; bold?: boolean;
}) {
  return (
    <>
      <span style={{ color: 'var(--text3)' }}>{label}</span>
      <span style={{
        color, fontWeight: bold ? 700 : 400,
        fontFamily: mono ? 'JetBrains Mono, monospace' : 'inherit',
      }}>{value}</span>
    </>
  );
}
