'use client';
import type { CSSProperties } from 'react';
import { useApp } from '@/lib/store';
import type { EntryMethod } from '@/types';

const METHODS: Array<{ method: EntryMethod; icon: string; sub: string }> = [
  { method: 'Contactless',  icon: '📱', sub: 'NFC / EMV'   },
  { method: 'Chip',         icon: '💳', sub: 'EMV ICC'     },
  { method: 'Swipe',        icon: '⬅️', sub: 'Mag-stripe'  },
  { method: 'Manual Entry', icon: '⌨️', sub: 'MOTO / CNP' },
];

const labelStyle: CSSProperties = {
  fontSize: 9, fontWeight: 700, letterSpacing: '0.12em',
  textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 10,
};

const gridStyle: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(4, 1fr)',
  gap: 10,
  width: '100%',
};

interface Props {
  onMethodChange: () => void; // callback to reset terminal state
}

export default function EntryMethodGrid({ onMethodChange }: Props) {
  const { state, setMethod } = useApp();

  function handlePick(method: EntryMethod) {
    setMethod(method);
    onMethodChange(); // clear previous result + EMV log
  }

  return (
    <div style={{ width: '100%' }}>
      <div style={labelStyle}>Entry Method</div>
      <div style={gridStyle}>
        {METHODS.map(({ method, icon, sub }) => {
          const on = state.method === method;
          return (
            <button
              key={method}
              onClick={() => handlePick(method)}
              style={{
                background:   on ? 'rgba(56,189,248,.08)' : 'var(--s2)',
                border:       `1px solid ${on ? 'rgba(56,189,248,.5)' : 'var(--border)'}`,
                boxShadow:    on ? '0 0 0 1px rgba(56,189,248,.12)' : 'none',
                borderRadius: 10,
                padding:      '14px 8px',
                textAlign:    'center',
                cursor:       'pointer',
                transition:   'all .2s',
                width:        '100%',
              }}
            >
              <span style={{ fontSize: 22, display: 'block', marginBottom: 6, lineHeight: 1 }}>
                {icon}
              </span>
              <div style={{ fontSize: 11, fontWeight: 600, color: on ? 'var(--cyan)' : 'var(--text2)' }}>
                {method}
              </div>
              <div style={{ fontSize: 9, color: 'var(--text3)', marginTop: 2 }}>
                {sub}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
