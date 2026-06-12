'use client';
import type { CSSProperties } from 'react';
import type { Transaction } from '@/types';

interface Props {
  txn:              Transaction | null;
  status:           'ready' | 'processing' | 'approved' | 'declined';
  offline:          boolean;
  selectedMerchant?: string | null;
}

type StatusKey = 'ready' | 'processing' | 'approved' | 'declined';

const statusMap: Record<StatusKey, (off: boolean) => { label: string; bg: string; color: string; border: string }> = {
  ready:      ()    => ({ label:'READY',              bg:'rgba(56,189,248,.1)',  color:'var(--cyan)',  border:'rgba(56,189,248,.25)'  }),
  processing: ()    => ({ label:'PROCESSING…',        bg:'rgba(251,191,36,.1)', color:'var(--amber)', border:'rgba(251,191,36,.25)'  }),
  approved:   (off) => ({ label: off ? 'APPROVED (OFFLINE)' : 'APPROVED', bg:'rgba(74,222,128,.1)',  color:'var(--green)', border:'rgba(74,222,128,.25)' }),
  declined:   ()    => ({ label:'DECLINED',           bg:'rgba(248,113,113,.1)',color:'var(--red)',   border:'rgba(248,113,113,.25)' }),
};

export default function TerminalScreen({ txn, status, offline, selectedMerchant }: Props) {
  const amt   = txn ? `$${txn.amt}`                        : '$0.00';
  const merch = txn ? txn.merchant : (selectedMerchant ?? '');
  const sub   = txn
    ? `${txn.merchant} · ${txn.method}`
    : selectedMerchant
      ? `📍 ${selectedMerchant} — ready to process`
      : 'Insert, tap, or swipe card — then press PROCESS';
  const last4 = txn ? `•••• •••• •••• ${txn.card.last4}` : '•••• •••• •••• ─ ─ ─ ─';
  const brand = txn ? txn.card.brand                       : '─ ─ ─';

  const { label, bg, color, border } = statusMap[status](offline);

  const screenStyle: CSSProperties = {
    background: '#010c12', border: '1px solid rgba(31,41,55,.8)',
    borderRadius: 12, padding: 18, minHeight: 160,
    display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
    position: 'relative', overflow: 'hidden', marginBottom: 14, width: '100%',
  };

  return (
    <div style={screenStyle}>
      {/* Scanlines */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(56,189,248,.012) 3px,rgba(56,189,248,.012) 4px)',
      }} />

      <div>
        <div style={{ fontSize: 8, fontFamily: 'JetBrains Mono, monospace', color: 'var(--text4)', letterSpacing: '0.18em', textTransform: 'uppercase' }}>
          REAL RAILS TERMINAL · EMV V4.3 · PCI-PTS 6.X
        </div>
        <div style={{ fontSize: 34, fontWeight: 600, color: 'var(--text)', letterSpacing: -2, margin: '8px 0 3px', fontFamily: 'JetBrains Mono, monospace' }}>
          {amt}
        </div>
        <div style={{ fontSize: 11, color: 'var(--text2)' }}>{sub}</div>
      </div>

      <div>
        <div style={{
          background: 'linear-gradient(135deg,#0d1e2e,#150e2a)', border: '1px solid var(--b2)',
          borderRadius: 8, padding: '10px 12px', display: 'flex',
          justifyContent: 'space-between', alignItems: 'center', marginTop: 8,
        }}>
          <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 11, color: 'var(--text2)', letterSpacing: '0.08em' }}>
            {last4}
          </span>
          <span style={{ fontSize: 10, fontWeight: 700, color: 'var(--indigo)', background: 'rgba(129,140,248,.12)', padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(129,140,248,.2)' }}>
            {brand}
          </span>
        </div>
        <div style={{ marginTop: 10 }}>
          <span style={{
            display: 'inline-block', fontSize: 11, fontWeight: 700,
            letterSpacing: '0.07em', padding: '5px 12px', borderRadius: 6,
            fontFamily: 'JetBrains Mono, monospace',
            background: bg, color, border: `1px solid ${border}`,
            animation: status === 'processing' ? 'blink .75s infinite' : 'none',
          }}>
            {label}
          </span>
        </div>
      </div>

      <style>{`@keyframes blink{0%,100%{opacity:1}50%{opacity:.45}}`}</style>
    </div>
  );
}
