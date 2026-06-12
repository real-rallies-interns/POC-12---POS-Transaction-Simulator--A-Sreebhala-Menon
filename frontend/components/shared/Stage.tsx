'use client';
import { useState } from 'react';
import type { CSSProperties } from 'react';
import MapView       from '@/components/map/MapView';
import TerminalPane  from '@/components/terminal/TerminalPane';
import AnalyticsPane from '@/components/analytics/AnalyticsPane';
import ReceiptsPane  from '@/components/receipts/ReceiptsPane';
import OfflinePane   from '@/components/offline/OfflinePane';

const TABS = ['Terminal Simulator', 'Decline Analytics', 'Receipt Log', 'Offline Queue'] as const;
type Tab = typeof TABS[number];

const stageStyle: CSSProperties = {
  width: '70%', minWidth: 0, flexShrink: 0,
  display: 'flex', flexDirection: 'column',
  borderRight: '1px solid var(--border)', overflow: 'hidden',
};

const tabBarStyle: CSSProperties = {
  display: 'flex', borderBottom: '1px solid var(--border)',
  flexShrink: 0, background: 'var(--surface)',
};

export default function Stage() {
  const [active, setActive] = useState<Tab>('Terminal Simulator');
  const [selectedMerchant, setSelectedMerchant] = useState<string | null>(null);
  const [mapCollapsed, setMapCollapsed] = useState(false);

  return (
    <div style={stageStyle}>

      {/* MAP — collapsible */}
      <div style={{
        height: mapCollapsed ? 36 : '32%',
        flexShrink: 0,
        position: 'relative',
        transition: 'height .3s ease',
        borderBottom: '1px solid var(--border)',
        overflow: 'hidden',
      }}>
        {/* Collapse toggle */}
        <button
          onClick={() => setMapCollapsed(c => !c)}
          style={{
            position: 'absolute', bottom: 8, right: 8, zIndex: 1001,
            background: 'rgba(11,17,23,0.92)', border: '1px solid var(--b2)',
            color: 'var(--text2)', borderRadius: 6, padding: '3px 10px',
            fontSize: 10, fontWeight: 600, cursor: 'pointer',
            letterSpacing: '0.05em', backdropFilter: 'blur(8px)',
          }}
        >
          {mapCollapsed ? '▼ SHOW MAP' : '▲ HIDE MAP'}
        </button>

        {!mapCollapsed && (
          <MapView
            onMerchantClick={(merchant) => {
              setSelectedMerchant(merchant);
              setActive('Terminal Simulator');
            }}
          />
        )}

        {mapCollapsed && (
          <div style={{
            height: 36, display: 'flex', alignItems: 'center',
            padding: '0 14px', gap: 8,
            background: 'var(--surface)',
          }}>
            <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--cyan)' }}>
              ● MERCHANT TERMINAL MAP — 10 LOCATIONS
            </span>
            {selectedMerchant && (
              <span style={{ fontSize: 10, color: 'var(--indigo)' }}>
                📍 {selectedMerchant} selected
              </span>
            )}
          </div>
        )}
      </div>

      {/* TAB BAR */}
      <div style={tabBarStyle}>
        {TABS.map(t => (
          <button key={t} onClick={() => setActive(t)} style={{
            padding: '10px 16px', fontSize: 11, fontWeight: 500,
            color: active === t ? 'var(--cyan)' : 'var(--text3)',
            background: 'none', border: 'none',
            borderBottom: active === t ? '2px solid var(--cyan)' : '2px solid transparent',
            cursor: 'pointer', transition: 'color .18s, border-color .18s',
            letterSpacing: '0.03em', whiteSpace: 'nowrap',
          }}>{t}</button>
        ))}
      </div>

      {/* PANES */}
      <div style={{
        flex: 1, minHeight: 0, overflow: 'hidden',
        display: 'flex', flexDirection: 'column', width: '100%',
      }}>
        {active === 'Terminal Simulator' && <TerminalPane selectedMerchant={selectedMerchant} />}
        {active === 'Decline Analytics'  && <AnalyticsPane />}
        {active === 'Receipt Log'        && <ReceiptsPane  />}
        {active === 'Offline Queue'      && <OfflinePane   />}
      </div>
    </div>
  );
}