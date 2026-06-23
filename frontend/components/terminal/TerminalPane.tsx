'use client';
import { useState, useCallback, useEffect } from 'react';
import { useApp } from '@/lib/store';
import { initiateTransaction } from '@/lib/adapters';
import { buildEmvSteps } from '@/lib/mock';
import EntryMethodGrid from './EntryMethodGrid';
import TerminalScreen  from './TerminalScreen';
import EmvLog          from './EmvLog';
import ResultCard      from './ResultCard';
import type { EmvStep, Transaction } from '@/types';

type Status = 'ready' | 'processing' | 'approved' | 'declined';

function sleep(ms: number) { return new Promise(r => setTimeout(r, ms)); }

async function animateEmv(steps: EmvStep[], onStep: (acc: EmvStep[]) => void): Promise<void> {
  const acc: EmvStep[] = [];
  for (const step of steps) {
    await sleep(110);
    acc.push(step);
    onStep([...acc]);
  }
}

interface Props {
  selectedMerchant?: string | null;
}

export default function TerminalPane({ selectedMerchant }: Props) {
  const { state, addTxn, addSaf, setOffline } = useApp();
  const [status,   setStatus]   = useState<Status>('ready');
  const [emvSteps, setEmvSteps] = useState<EmvStep[]>([]);
  const [lastTxn,  setLastTxn]  = useState<Transaction | null>(null);
  const [busy,     setBusy]     = useState(false);

  // When a merchant pin is clicked from the map, show it on screen
  useEffect(() => {
    if (selectedMerchant) {
      setStatus('ready');
      setEmvSteps([]);
      setLastTxn(null);
    }
  }, [selectedMerchant]);

  const handleMethodChange = useCallback(() => {
    setStatus('ready');
    setEmvSteps([]);
    setLastTxn(null);
  }, []);

  const run = useCallback(async () => {
    setBusy(true);
    setStatus('processing');
    setEmvSteps([]);
    setLastTxn(null);

    const txn = await initiateTransaction(state.method, state.offline);

    // Override merchant if selected from map
    if (selectedMerchant) txn.merchant = selectedMerchant;

    if (['Chip', 'Contactless'].includes(state.method)) {
      const steps = txn.emv.length ? txn.emv : buildEmvSteps(parseFloat(txn.amt));
      await animateEmv(steps, setEmvSteps);
    } else {
      await sleep(900);
    }

    setStatus(txn.approved ? 'approved' : 'declined');
    setLastTxn(txn);
    addTxn(txn);

    if (state.offline && txn.approved) {
      addSaf({
        id:   'SAF-' + txn.id.slice(-6),
        amt:  txn.amt,
        card: txn.card,
        time: txn.time,
        risk: parseFloat(txn.amt) > 200,
      });
    }
    setBusy(false);
  }, [state.method, state.offline, selectedMerchant, addTxn, addSaf]);

  const reset = useCallback(() => {
    setStatus('ready');
    setEmvSteps([]);
    setLastTxn(null);
  }, []);

  return (
    <div style={{
      flex: 1, overflowY: 'auto', padding: '16px 24px',
      display: 'flex', flexDirection: 'column', gap: 14,
      width: '100%', minWidth: 0,
    }}>

      {/* Selected merchant banner */}
      {selectedMerchant && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8, width: '100%',
          background: 'rgba(129,140,248,.08)', border: '1px solid rgba(129,140,248,.3)',
          borderRadius: 8, padding: '8px 14px', fontSize: 11, color: 'var(--indigo)',
        }}>
          <span>📍</span>
          <span>Terminal selected from map: <strong>{selectedMerchant}</strong></span>
        </div>
      )}

      <EntryMethodGrid onMethodChange={handleMethodChange} />

      {state.offline && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8, width: '100%',
          background: 'rgba(251,191,36,.07)', border: '1px solid rgba(251,191,36,.25)',
          borderRadius: 10, padding: '9px 14px', fontSize: 11, color: 'var(--amber)',
        }}>
          <span style={{ width: 7, height: 7, background: 'var(--amber)', borderRadius: '50%', flexShrink: 0, animation: 'livepulse 1.4s infinite' }} />
          <div><strong>OFFLINE MODE ACTIVE</strong> — Transactions stored via Store &amp; Forward.</div>
          <style>{`@keyframes livepulse{0%,100%{opacity:1}50%{opacity:.35}}`}</style>
        </div>
      )}

      {/* Device */}
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--b2)',
        borderRadius: 14, padding: 18, position: 'relative', overflow: 'hidden', width: '100%',
      }}>
        <div style={{ position: 'absolute', top: 0, left: '20%', right: '20%', height: 1, background: 'linear-gradient(90deg,transparent,var(--cyan),transparent)', opacity: .5 }} />

        <TerminalScreen txn={lastTxn} status={status} offline={state.offline} selectedMerchant={selectedMerchant} />

        <div style={{ display: 'flex', gap: 10, width: '100%' }}>
          <button disabled={busy} onClick={run} style={{
            flex: 1, background: 'rgba(56,189,248,.12)', border: '1px solid rgba(56,189,248,.4)',
            color: 'var(--cyan)', borderRadius: 9, padding: 11,
            font: '600 13px/1 Inter, sans-serif', cursor: busy ? 'not-allowed' : 'pointer',
            transition: 'all .2s', letterSpacing: '0.04em', opacity: busy ? .5 : 1,
          }}>
            {busy ? '⏳  Processing…' : '▶  PROCESS TRANSACTION'}
          </button>
          <button onClick={reset} style={{
            background: 'var(--s2)', border: '1px solid var(--border)', color: 'var(--text2)',
            borderRadius: 9, padding: '11px 16px', font: '500 13px/1 Inter, sans-serif', cursor: 'pointer',
          }}>↺  Reset</button>
        </div>

        <div onClick={() => setOffline(!state.offline)} style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          background: state.offline ? 'rgba(251,191,36,.05)' : 'var(--s2)',
          border: `1px solid ${state.offline ? 'rgba(251,191,36,.4)' : 'var(--border)'}`,
          borderRadius: 9, padding: '10px 14px', marginTop: 11, cursor: 'pointer', width: '100%',
        }}>
          <span style={{ fontSize: 12, fontWeight: 500, color: state.offline ? 'var(--amber)' : 'var(--text3)' }}>
            {state.offline ? '⚡  Offline Mode — Store & Forward active' : '☁  Online Mode — Bank connection active'}
          </span>
          <div style={{ width: 32, height: 18, background: state.offline ? 'var(--amber)' : 'var(--b2)', borderRadius: 20, position: 'relative', transition: 'background .25s', flexShrink: 0 }}>
            <div style={{ position: 'absolute', width: 12, height: 12, background: '#fff', borderRadius: '50%', top: 3, left: state.offline ? 17 : 3, transition: 'left .25s', boxShadow: '0 1px 3px rgba(0,0,0,.4)' }} />
          </div>
        </div>
      </div>

      {emvSteps.length > 0 && <EmvLog steps={emvSteps} />}
      {lastTxn && <ResultCard txn={lastTxn} offline={state.offline} />}
    </div>
  );
}
