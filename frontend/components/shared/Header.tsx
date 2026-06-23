'use client';
import { useEffect, useRef } from 'react';
import { useApp } from '@/lib/store';
import { probeHealth } from '@/lib/adapters';

export default function Header() {
  const { state, setApiMode } = useApp();
  const clockRef = useRef<HTMLSpanElement>(null);

  // Live clock
  useEffect(() => {
    const id = setInterval(() => {
      if (clockRef.current)
        clockRef.current.textContent = new Date().toTimeString().slice(0, 8);
    }, 1000);
    return () => clearInterval(id);
  }, []);

  // API probe on mount + every 30 s
  useEffect(() => {
    async function probe() {
      const alive = await probeHealth();
      setApiMode(alive ? 'live' : 'mock');
    }
    probe();
    const id = setInterval(probe, 30_000);
    return () => clearInterval(id);
  }, [setApiMode]);

  const isLive = state.apiMode === 'live';

  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      height: 48, padding: '0 20px', borderBottom: '1px solid var(--border)',
      background: 'rgba(11,17,23,0.92)', backdropFilter: 'blur(16px)',
      position: 'relative', zIndex: 50, flexShrink: 0,
    }}>
      {/* Left */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 30, height: 30, borderRadius: 7,
          background: 'linear-gradient(135deg,#0ea5e9,#6366f1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 12, fontWeight: 800, color: '#fff', letterSpacing: -0.5,
        }}>RR</div>

        <span style={{ fontSize: 12, fontWeight: 600, letterSpacing: '0.05em', color: 'var(--text2)' }}>
          <strong style={{ color: 'var(--text)', fontWeight: 700 }}>REAL RAILS</strong>
          {' · '}Intelligence Library
        </span>

        <span style={pillStyle('#071520', 'var(--border2)', 'var(--cyan)')}>PoC #12</span>
        <span style={pillStyle('#0d1520', 'var(--border2)', 'var(--violet)')}>● Geographic</span>
      </div>

      {/* Right */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
        {/* API indicator */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 5, fontSize: 10, fontWeight: 700,
          padding: '3px 9px', borderRadius: 20, border: '1px solid',
          letterSpacing: '0.05em',
          background: isLive ? 'rgba(74,222,128,.08)' : 'rgba(251,191,36,.08)',
          borderColor: isLive ? 'rgba(74,222,128,.3)' : 'rgba(251,191,36,.3)',
          color: isLive ? 'var(--green)' : 'var(--amber)',
        }}>
          <span style={{
            width: 5, height: 5, borderRadius: '50%',
            background: isLive ? 'var(--green)' : 'var(--amber)',
            animation: 'livepulse 1.8s infinite',
          }} />
          {isLive ? 'LIVE API' : 'MOCK DATA'}
        </div>

        <span style={{ fontSize: 10, color: 'var(--text3)', letterSpacing: '0.04em' }}>
          POS TRANSACTION SIMULATOR
        </span>

        <span style={{
          width: 6, height: 6, borderRadius: '50%', background: 'var(--green)',
          boxShadow: '0 0 5px var(--green)', animation: 'livepulse 2s infinite',
        }} />

        <span ref={clockRef} style={{ fontFamily: 'var(--mono-rr)', fontSize: 11, color: 'var(--text2)' }}>
          --:--:--
        </span>
      </div>

      <style>{`
        @keyframes livepulse { 0%,100%{opacity:1} 50%{opacity:.35} }
      `}</style>
    </header>
  );
}

function pillStyle(bg: string, border: string, color: string) {
  return {
    display: 'inline-flex', alignItems: 'center', borderRadius: 20,
    fontSize: 10, fontWeight: 700, letterSpacing: '0.06em',
    padding: '3px 10px', border: `1px solid ${border}`,
    background: bg, color,
  } as React.CSSProperties;
}
