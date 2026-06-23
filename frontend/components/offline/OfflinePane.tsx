'use client';
import { useApp } from '@/lib/store';

export default function OfflinePane() {
  const { state } = useApp();
  const total = state.saf.reduce((a, s) => a + parseFloat(s.amt), 0);

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px', display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Info block */}
      <div style={{
        background: 'var(--s2)', border: '1px solid var(--border)',
        borderLeft: '2px solid var(--cyan)', borderRadius: '0 8px 8px 0',
        padding: '11px 14px', fontSize: 11, color: 'var(--text2)', lineHeight: 1.6,
      }}>
        When a terminal loses bank connectivity, approved transactions are stored locally using{' '}
        <strong style={{ color: 'var(--text)' }}>offline authorization tokens</strong> derived from
        the card's EMV chip. These are batched and replayed to the acquiring bank on reconnect.
        <br /><br />
        <strong style={{ color: 'var(--text)' }}>Risk rule:</strong> Transactions over $200 are
        flagged — the card's floor limit has been exceeded and issuer auth cannot be confirmed offline.
      </div>

      {/* Queue */}
      {state.saf.length === 0 ? (
        <div style={{ color: 'var(--text3)', fontSize: 11, textAlign: 'center', padding: '24px 0' }}>
          Enable Offline Mode, then run transactions to populate the Store &amp; Forward queue.
        </div>
      ) : (
        state.saf.map(s => (
          <div key={s.id} style={{
            background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8,
            padding: '10px 12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            animation: 'slideIn .25s ease forwards',
          }}>
            <div>
              <div style={{ fontFamily: 'JetBrains Mono,monospace', fontSize: 9, color: 'var(--text3)' }}>{s.id}</div>
              <div style={{ fontSize: 10, color: 'var(--text2)', marginTop: 2 }}>
                {s.card.brand} ••••{s.card.last4} · {s.time}
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontFamily: 'JetBrains Mono,monospace', fontSize: 14, fontWeight: 700, color: 'var(--amber)' }}>
                ${s.amt}
              </div>
              <div style={{ display: 'flex', gap: 4, justifyContent: 'flex-end', marginTop: 4 }}>
                <Tag color="amber">PENDING</Tag>
                {s.risk && <Tag color="red">⚠ HIGH VALUE</Tag>}
              </div>
            </div>
          </div>
        ))
      )}

      {state.saf.length > 0 && (
        <div style={{
          background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8,
          padding: '10px 14px', display: 'flex', justifyContent: 'space-between', fontSize: 11, alignItems: 'center',
        }}>
          <span style={{ color: 'var(--text2)' }}>Pending: <strong style={{ color: 'var(--amber)', fontFamily: 'JetBrains Mono,monospace' }}>{state.saf.length}</strong></span>
          <span style={{ color: 'var(--text2)' }}>Total exposure: <strong style={{ color: 'var(--amber)', fontFamily: 'JetBrains Mono,monospace' }}>${total.toFixed(2)}</strong></span>
          <span style={{ fontSize: 9, color: 'var(--text3)' }}>⚡ Auto-sync on reconnect</span>
        </div>
      )}

      <style>{`@keyframes slideIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}`}</style>
    </div>
  );
}

function Tag({ children, color }: { children: React.ReactNode; color: 'amber' | 'red' }) {
  const map = {
    amber: { bg: 'rgba(251,191,36,.09)', color: 'var(--amber)', border: 'rgba(251,191,36,.25)' },
    red:   { bg: 'rgba(248,113,113,.09)', color: 'var(--red)',  border: 'rgba(248,113,113,.25)' },
  }[color];
  return (
    <span style={{
      fontSize: 8, fontWeight: 700, padding: '2px 7px', borderRadius: 4,
      background: map.bg, color: map.color, border: `1px solid ${map.border}`,
    }}>{children}</span>
  );
}
