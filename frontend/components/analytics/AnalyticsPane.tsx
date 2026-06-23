'use client';
import { useEffect, useState } from 'react';
import { fetchDeclineBreakdown, fetchEntryStats } from '@/lib/adapters';
import { DECLINE_POOL } from '@/lib/mock';
import type { APIDeclineBreakdown, APIEntryStats } from '@/types';

// ─── Static fallbacks ────────────────────────────────────────────────────────
const MOCK_CATS: Record<string,number> = {};
DECLINE_POOL.forEach(d => { MOCK_CATS[d.category] = (MOCK_CATS[d.category] || 0) + 1; });

const ENTRY_FALLBACK = [
  { method:'Contactless', share:41, trend:'+12% YoY', avg_ticket:28.50, fraud_rate_bps:4  },
  { method:'Chip',        share:38, trend:'+2% YoY',  avg_ticket:74.20, fraud_rate_bps:2  },
  { method:'Swipe',       share:15, trend:'-8% YoY',  avg_ticket:42.10, fraud_rate_bps:18 },
  { method:'Manual',      share:6,  trend:'-2% YoY',  avg_ticket:190,   fraud_rate_bps:65 },
];

const CAT_COLORS = ['#38BDF8','#818CF8','#FBBF24','#F87171','#4ADE80'];

export default function AnalyticsPane() {
  const [decline, setDecline] = useState<APIDeclineBreakdown | null>(null);
  const [entry,   setEntry]   = useState<APIEntryStats | null>(null);

  useEffect(() => {
    fetchDeclineBreakdown().then(d => setDecline(d));
    fetchEntryStats().then(e => setEntry(e));
  }, []);

  const cats   = decline ? buildCatMap(decline) : MOCK_CATS;
  const codes  = decline ? decline.breakdown.slice(0,7) : DECLINE_POOL.slice(0,7).map(d => ({ code:d.code, label:d.label, percentage:10 }));
  const eMeth  = entry   ? entry.stats : ENTRY_FALLBACK;
  const totDec = decline ? decline.total_declines : 147;
  const topDec = decline ? decline.breakdown.reduce((a,b)=>b.percentage>a.percentage?b:a, decline.breakdown[0]) : { label:'Insuff. Funds', code:'51' };

  const maxShare = Math.max(...eMeth.map(e=>e.share));
  const maxPct   = Math.max(...codes.map(c=>c.percentage));

  return (
    <div style={{ flex:1, overflowY:'auto', padding:'18px 20px', display:'flex', flexDirection:'column', gap:14 }}>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
        {/* Donut — categories */}
        <ChartCard title="Decline Categories">
          <DonutChart cats={cats} />
        </ChartCard>

        {/* Bar — top codes */}
        <ChartCard title="Top Decline Codes">
          <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
            {codes.map((c,i) => (
              <div key={c.code} style={{ display:'flex', alignItems:'center', gap:8, fontSize:10 }}>
                <span style={{ fontFamily:'JetBrains Mono,monospace', color:'var(--text3)', width:28, flexShrink:0 }}>{c.code}</span>
                <span style={{ color:'var(--text2)', flex:1, fontSize:9 }}>{c.label}</span>
                <div style={{ width:80, height:10, background:'var(--s2)', borderRadius:3, overflow:'hidden' }}>
                  <div style={{ width:`${(c.percentage/maxPct)*100}%`, height:'100%', background:'rgba(129,140,248,.6)', borderRadius:3 }} />
                </div>
                <span style={{ fontFamily:'JetBrains Mono,monospace', color:'var(--indigo)', width:28, textAlign:'right', fontSize:9 }}>{c.percentage}%</span>
              </div>
            ))}
          </div>
        </ChartCard>
      </div>

      {/* Entry method */}
      <ChartCard title="Entry Method Market Share — Fed Reserve Payments Study 2022">
        <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
          {eMeth.map(e => (
            <div key={e.method} style={{ display:'flex', alignItems:'center', gap:10 }}>
              <span style={{ color:'var(--text2)', fontSize:11, width:90, flexShrink:0 }}>{e.method}</span>
              <div style={{ flex:1, height:20, background:'var(--s2)', borderRadius:4, overflow:'hidden' }}>
                <div style={{ width:`${(e.share/maxShare)*100}%`, height:'100%', background:'rgba(56,189,248,.55)', borderRadius:4, display:'flex', alignItems:'center', paddingLeft:6 }}>
                  <span style={{ fontSize:9, color:'var(--cyan)', fontWeight:700 }}>{e.share}%</span>
                </div>
              </div>
              <span style={{ fontSize:9, color:'var(--text3)', width:70, textAlign:'right', flexShrink:0 }}>avg ${e.avg_ticket}</span>
            </div>
          ))}
        </div>
      </ChartCard>

      {/* Stats row */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:8 }}>
        <StatCard label="Total Declines" value={String(totDec)}  sub="Benchmark" />
        <StatCard label="Top Reason"     value={topDec.label}    sub={`Code ${topDec.code}`} valStyle={{ fontSize:12 }} />
        <StatCard label="Approval Rate"  value="78%"             sub="Fed Reserve avg"  valColor="var(--green)" />
        <StatCard label="Avg Ticket"     value="$58"             sub="Card-present" />
      </div>

      <div style={{ fontSize:9, color:'var(--text3)', paddingBottom:4 }}>
        ⓘ Sources: CFPB Consumer Credit Reports · Federal Reserve Payments Study (2022) · Synthetic benchmark
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

function ChartCard({ title, children }: { title:string; children:React.ReactNode }) {
  return (
    <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:12, padding:14 }}>
      <div style={{ fontSize:10, fontWeight:700, color:'var(--text2)', letterSpacing:'0.07em', textTransform:'uppercase', marginBottom:12 }}>{title}</div>
      {children}
    </div>
  );
}

function StatCard({ label, value, sub, valColor='var(--text)', valStyle={} }: {
  label:string; value:string; sub:string; valColor?:string; valStyle?: React.CSSProperties;
}) {
  return (
    <div style={{ background:'var(--s2)', border:'1px solid var(--border)', borderRadius:8, padding:'10px 12px' }}>
      <div style={{ fontSize:8, fontWeight:700, letterSpacing:'0.1em', textTransform:'uppercase', color:'var(--text3)', marginBottom:4 }}>{label}</div>
      <div style={{ fontSize:17, fontWeight:700, color:valColor, fontFamily:'JetBrains Mono,monospace', letterSpacing:-0.5, ...valStyle }}>{value}</div>
      <div style={{ fontSize:9, marginTop:3, color:'var(--text3)' }}>{sub}</div>
    </div>
  );
}

function DonutChart({ cats }: { cats: Record<string,number> }) {
  const entries = Object.entries(cats);
  const total   = entries.reduce((s,[,v])=>s+v,0);
  let   angle   = -90;
  const cx = 70, cy = 70, r = 52, inner = 34;

  const slices = entries.map(([cat,val],i) => {
    const pct  = val/total;
    const deg  = pct * 360;
    const rad1 = (angle * Math.PI) / 180;
    const rad2 = ((angle+deg) * Math.PI) / 180;
    const lx   = cx + r * Math.cos(rad1), ly = cy + r * Math.sin(rad1);
    const ex   = cx + r * Math.cos(rad2), ey = cy + r * Math.sin(rad2);
    const ix   = cx + inner * Math.cos(rad1), iy = cy + inner * Math.sin(rad1);
    const ox   = cx + inner * Math.cos(rad2), oy = cy + inner * Math.sin(rad2);
    const large = deg > 180 ? 1 : 0;
    const path  = `M${ix},${iy} L${lx},${ly} A${r},${r},0,${large},1,${ex},${ey} L${ox},${oy} A${inner},${inner},0,${large},0,${ix},${iy}Z`;
    angle += deg;
    return { path, color: CAT_COLORS[i % CAT_COLORS.length], cat, pct };
  });

  return (
    <div style={{ display:'flex', alignItems:'center', gap:12 }}>
      <svg width={140} height={140} viewBox="0 0 140 140">
        {slices.map(s => <path key={s.cat} d={s.path} fill={s.color} stroke="var(--surface)" strokeWidth={1.5} />)}
        <circle cx={cx} cy={cy} r={inner-2} fill="var(--surface)" />
      </svg>
      <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
        {slices.map((s,i) => (
          <div key={s.cat} style={{ display:'flex', alignItems:'center', gap:5, fontSize:9 }}>
            <div style={{ width:8, height:8, borderRadius:2, background:CAT_COLORS[i%CAT_COLORS.length], flexShrink:0 }} />
            <span style={{ color:'var(--text2)' }}>{s.cat}</span>
            <span style={{ color:'var(--text3)', fontFamily:'JetBrains Mono,monospace' }}>{(s.pct*100).toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function buildCatMap(d: APIDeclineBreakdown): Record<string,number> {
  const m: Record<string,number> = {};
  d.category_rollup.forEach(c => { m[c.category] = c.count; });
  return m;
}
