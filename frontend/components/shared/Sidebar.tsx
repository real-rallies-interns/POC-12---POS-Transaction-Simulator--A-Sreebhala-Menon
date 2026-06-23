'use client';
import { useApp } from '@/lib/store';
import { fetchSampleData, downloadJSON } from '@/lib/adapters';

const GOV = [
  { icon:'🏭', name:'POS Manufacturer',   sub:'Verifone, Ingenico, PAX — hardware & firmware' },
  { icon:'🏦', name:'Acquirer / Processor',sub:'Stripe, Square, Worldpay — merchant settlement' },
  { icon:'🌐', name:'Card Networks',       sub:'Visa & Mastercard — interchange & routing' },
  { icon:'📋', name:'EMVCo',              sub:'Global chip & contactless standards body' },
  { icon:'⚖️', name:'Regulators',         sub:'Federal Reserve · CFPB — Reg E / Durbin Amendment' },
];

const GOV_COLORS = ['rgba(56,189,248,.1)','rgba(129,140,248,.1)','rgba(74,222,128,.1)','rgba(251,191,36,.1)','rgba(248,113,113,.1)'];

export default function Sidebar() {
  const { state } = useApp();
  const { txn, rev, approvals, declines } = state;

  async function handleDownload() {
    const records = await fetchSampleData();
    downloadJSON(records);
  }

  return (
    <div style={{ flex: '0 0 30%', minWidth: 0, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ overflowY: 'auto', flex: 1 }}>

        {/* A: Metrics */}
        <Section head="Section A — Live Metrics">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 7 }}>
            <MetCard label="Transactions" value={txn} sub="This session" />
            <MetCard label="Revenue"      value={'$'+rev.toFixed(0)} sub="Approved" subColor="var(--green)" />
            <MetCard label="Approvals"    value={approvals} sub={txn ? ((approvals/txn)*100).toFixed(0)+'%' : '─'} valColor="var(--green)" />
            <MetCard label="Declines"     value={declines}  sub={txn ? ((declines/txn)*100).toFixed(0)+'%'  : '─'} valColor="var(--red)" />
          </div>
        </Section>

        {/* B: Why This Matters */}
        <Section head="Section B — Why This Matters">
          <div style={infoBlkStyle}>
            The POS terminal is the <strong style={{color:'var(--text)'}}>last mile of every payment</strong>.
            A broken terminal means $0 revenue — no fallback.
            One hour of peak downtime costs a busy restaurant{' '}
            <strong style={{color:'var(--text)'}}>$800–$2,400</strong> in direct lost sales.<br/><br/>
            This simulator exposes the invisible mechanics: the EMV chip handshake, offline auth fallback,
            and decline codes that determine whether a customer walks away satisfied or humiliated.<br/><br/>
            Sources: <strong style={{color:'var(--text)'}}>CFPB Consumer Credit Reports</strong>
            {' · '}<strong style={{color:'var(--text)'}}>Federal Reserve Payments Study</strong>
          </div>
        </Section>

        {/* C: Who Controls the Rail */}
        <Section head="Section C — Who Controls the Rail">
          {GOV.map((g, i) => (
            <div key={g.name} style={{
              display: 'flex', alignItems: 'flex-start', gap: 9,
              padding: '7px 0', borderBottom: i < GOV.length - 1 ? '1px solid rgba(31,41,55,.55)' : 'none',
            }}>
              <div style={{
                width: 26, height: 26, borderRadius: 6, display: 'flex',
                alignItems: 'center', justifyContent: 'center',
                fontSize: 13, flexShrink: 0, marginTop: 1,
                background: GOV_COLORS[i],
              }}>{g.icon}</div>
              <div>
                <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--text)', marginBottom: 1 }}>{g.name}</div>
                <div style={{ fontSize: 10, color: 'var(--text3)' }}>{g.sub}</div>
              </div>
            </div>
          ))}
        </Section>

        {/* D: Filters (receipt tab filters — passed via a custom event for decoupling) */}
        <Section head="Section D — Filters">
          <FilterRow label="Entry Method" id="fil-method" options={['all','Contactless','Chip','Swipe','Manual Entry']} labels={['All Methods','Contactless','Chip','Swipe','Manual Entry']} />
          <FilterRow label="Status"       id="fil-status" options={['all','APPROVED','DECLINED']}                       labels={['All','Approved only','Declined only']} />
        </Section>

        {/* E: Sample Data */}
        <Section head="Section E — Sample Data">
          <p style={{ fontSize: 10, color: 'var(--text3)', lineHeight: 1.5, marginBottom: 6 }}>
            Synthetic dataset: 20 terminal events with EMV fields, receipt fields, and offline
            auth tokens. Labeled per CFPB Reg E disclosure requirements.
          </p>
          <button onClick={handleDownload} style={{
            width: '100%', background: 'rgba(129,140,248,.1)', border: '1px solid rgba(129,140,248,.3)',
            color: 'var(--indigo)', borderRadius: 8, padding: 10,
            font: '600 11px/1 Inter, sans-serif', cursor: 'pointer', letterSpacing: '0.05em',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, marginTop: 2,
          }}>
            ⬇&nbsp; Download Sample Data (JSON)
          </button>
        </Section>

      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

function Section({ head, children }: { head: string; children: React.ReactNode }) {
  return (
    <div style={{ padding: '16px 18px', borderBottom: '1px solid var(--border)' }}>
      <div style={{
        fontSize: 9, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase',
        color: 'var(--text3)', marginBottom: 12,
        display: 'flex', alignItems: 'center', gap: 6,
      }}>
        <span style={{ width: 2, height: 11, background: 'var(--cyan)', borderRadius: 2, display: 'inline-block' }} />
        {head}
      </div>
      {children}
    </div>
  );
}

function MetCard({
  label, value, sub, valColor = 'var(--text)', subColor = 'var(--text3)',
}: { label: string; value: number | string; sub: string; valColor?: string; subColor?: string }) {
  return (
    <div style={{ background: 'var(--s2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 12px' }}>
      <div style={{ fontSize: 8, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 3 }}>{label}</div>
      <div style={{ fontSize: 20, fontWeight: 700, color: valColor, fontFamily: 'JetBrains Mono, monospace', letterSpacing: -0.5 }}>{value}</div>
      <div style={{ fontSize: 9, marginTop: 2, color: subColor }}>{sub}</div>
    </div>
  );
}

function FilterRow({ label, id, options, labels }: { label: string; id: string; options: string[]; labels: string[] }) {
  function onChange(e: React.ChangeEvent<HTMLSelectElement>) {
    window.dispatchEvent(new CustomEvent('rr-filter-change', { detail: { id, value: e.target.value } }));
  }
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 8 }}>
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--text3)' }}>{label}</div>
      <select id={id} onChange={onChange} style={{
        background: 'var(--s2)', border: '1px solid var(--border)', color: 'var(--text2)',
        borderRadius: 6, padding: '7px 10px', fontSize: 12, width: '100%',
        outline: 'none', appearance: 'none', cursor: 'pointer', fontFamily: 'Inter, sans-serif',
      }}>
        {options.map((o, i) => <option key={o} value={o}>{labels[i]}</option>)}
      </select>
    </div>
  );
}

const infoBlkStyle: React.CSSProperties = {
  background: 'var(--s2)', border: '1px solid var(--border)',
  borderLeft: '2px solid var(--cyan)', borderRadius: '0 8px 8px 0',
  padding: '11px 14px', fontSize: 11, color: 'var(--text2)', lineHeight: 1.6,
};
