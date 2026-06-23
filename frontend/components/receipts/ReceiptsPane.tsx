'use client';
import { useState, useEffect } from 'react';
import { useApp } from '@/lib/store';
import type { Transaction } from '@/types';

type MethodFilter = 'all' | 'Contactless' | 'Chip' | 'Swipe' | 'Manual Entry';
type StatusFilter = 'all' | 'APPROVED' | 'DECLINED';

export default function ReceiptsPane() {
  const { state } = useApp();
  const [methodF, setMethodF] = useState<MethodFilter>('all');
  const [statusF, setStatusF] = useState<StatusFilter>('all');

  // Listen for filter changes dispatched from Sidebar
  useEffect(() => {
    function handler(e: Event) {
      const { id, value } = (e as CustomEvent<{ id: string; value: string }>).detail;
      if (id === 'fil-method') setMethodF(value as MethodFilter);
      if (id === 'fil-status') setStatusF(value as StatusFilter);
    }
    window.addEventListener('rr-filter-change', handler);
    return () => window.removeEventListener('rr-filter-change', handler);
  }, []);

  const rows: Transaction[] = state.receipts.filter(r => {
    if (methodF !== 'all' && r.method !== methodF) return false;
    if (statusF === 'APPROVED' && !r.approved) return false;
    if (statusF === 'DECLINED' &&  r.approved) return false;
    return true;
  });

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px' }}>
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 12 }}>
        Digital Receipt Log — Mandatory CFPB / Reg E Compliance Fields
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 11, minWidth: 600 }}>
          <thead>
            <tr>
              {['TXN ID','Time','Merchant','Amount','Card','Method','Status','Auth Code'].map(h => (
                <th key={h} style={{
                  textAlign: 'left', color: 'var(--text3)', fontWeight: 600, fontSize: 9,
                  letterSpacing: '0.1em', textTransform: 'uppercase',
                  padding: '6px 8px', borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap',
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr><td colSpan={8} style={{ textAlign: 'center', color: 'var(--text3)', padding: 28, fontSize: 11 }}>
                {state.receipts.length === 0 ? 'Run a transaction to populate the log.' : 'No matching transactions.'}
              </td></tr>
            ) : rows.map(r => (
              <tr key={r.id} style={{ borderBottom: '1px solid rgba(31,41,55,.45)' }}
                onMouseEnter={e => (e.currentTarget.style.background = 'var(--s2)')}
                onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}>
                <Td mono>{r.id}</Td>
                <Td mono>{r.time}</Td>
                <Td>{r.merchant}</Td>
                <Td mono>${r.amt}</Td>
                <Td mono>{r.card.brand} ••{r.card.last4}</Td>
                <Td>{r.method}</Td>
                <Td>
                  <span style={{
                    fontSize: 9, fontWeight: 700, padding: '2px 7px', borderRadius: 4,
                    background: r.approved ? 'rgba(74,222,128,.09)' : 'rgba(248,113,113,.09)',
                    color: r.approved ? 'var(--green)' : 'var(--red)',
                    border: `1px solid ${r.approved ? 'rgba(74,222,128,.2)' : 'rgba(248,113,113,.2)'}`,
                  }}>{r.approved ? 'APPROVED' : 'DECLINED'}</span>
                </Td>
                <Td mono>{r.approved ? r.auth : '—'}</Td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Td({ children, mono = false }: { children: React.ReactNode; mono?: boolean }) {
  return (
    <td style={{
      padding: '7px 8px', color: 'var(--text2)', whiteSpace: 'nowrap',
      fontFamily: mono ? 'JetBrains Mono, monospace' : 'inherit', fontSize: 10,
    }}>{children}</td>
  );
}
