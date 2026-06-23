'use client';
import { useEffect, useRef } from 'react';
import type { EmvStep } from '@/types';

interface Props { steps: EmvStep[] }

export default function EmvLog({ steps }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [steps]);

  if (!steps.length) return null;

  return (
    <div style={{
      background: 'var(--surface)', border: '1px solid var(--border)',
      borderRadius: 12, padding: 14,
    }}>
      <div style={{
        fontSize: 10, fontWeight: 700, color: 'var(--indigo)',
        letterSpacing: '0.1em', textTransform: 'uppercase',
        marginBottom: 10, display: 'flex', alignItems: 'center', gap: 5,
      }}>
        ⚡ EMV Chip Handshake — Live Protocol Log
      </div>
      <div ref={containerRef} style={{ maxHeight: 220, overflowY: 'auto' }}>
        {steps.map((s, i) => (
          <div key={i} style={{
            display: 'grid', gridTemplateColumns: '150px 28px 1fr 1fr',
            gap: 6, alignItems: 'flex-start',
            padding: '4px 0',
            borderBottom: i < steps.length - 1 ? '1px solid rgba(31,41,55,.5)' : 'none',
            animation: 'emvSlide .25s ease forwards',
            animationDelay: `${i * 0.05}s`,
          }}>
            <span style={{ fontSize: 9, fontWeight: 700, color: 'var(--indigo)', fontFamily: 'JetBrains Mono, monospace', letterSpacing: '0.03em', paddingTop: 1 }}>{s.phase}</span>
            <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 9, color: 'var(--text3)' }}>{s.tag}</span>
            <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 9, color: 'var(--cyan)', wordBreak: 'break-all' }}>{s.value}</span>
            <span style={{ fontSize: 9, color: 'var(--text2)', textAlign: 'right' }}>{s.desc}</span>
          </div>
        ))}
      </div>
      <style>{`@keyframes emvSlide{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}`}</style>
    </div>
  );
}
