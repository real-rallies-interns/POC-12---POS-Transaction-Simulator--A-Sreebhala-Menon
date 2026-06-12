'use client';
import { useEffect, useRef, useState, useCallback } from 'react';
import type { CSSProperties } from 'react';
import { useApp } from '@/lib/store';

export const MERCHANTS: Array<{
  id: string; name: string; lat: number; lng: number; category: string;
}> = [
  { id:'m1',  name:'Corner Deli',      lat:51.5074,  lng:-0.1278,  category:'Food & Drink'  },
  { id:'m2',  name:'Urban Coffee',     lat:51.5155,  lng:-0.0922,  category:'Food & Drink'  },
  { id:'m3',  name:'QuickMart',        lat:51.4994,  lng:-0.1248,  category:'Retail'        },
  { id:'m4',  name:'The Food Hall',    lat:51.5033,  lng:-0.1195,  category:'Food & Drink'  },
  { id:'m5',  name:'Pharmacy Plus',    lat:51.5200,  lng:-0.1350,  category:'Health'        },
  { id:'m6',  name:'Fuel & Go',        lat:51.4900,  lng:-0.1400,  category:'Fuel'          },
  { id:'m7',  name:'BookNook',         lat:51.5250,  lng:-0.1050,  category:'Retail'        },
  { id:'m8',  name:'Electronics Hub',  lat:51.5080,  lng:-0.0980,  category:'Electronics'   },
  { id:'m9',  name:'Garden Centre',    lat:51.4850,  lng:-0.1550,  category:'Retail'        },
  { id:'m10', name:'Apparel & Co',     lat:51.5120,  lng:-0.1420,  category:'Fashion'       },
];

interface TxnPin {
  id: string; lat: number; lng: number; approved: boolean; amt: string;
}

interface Props {
  onMerchantClick: (merchant: string) => void;
}

// Leaflet type shorthands
type LMarker = {
  addTo: (m: unknown) => LMarker;
  bindTooltip: (content: string, opts: unknown) => LMarker;
  on: (event: string, handler: () => void) => LMarker;
  setStyle: (style: unknown) => void;
  remove: () => void;
};
type LLeaflet = {
  map: (el: HTMLElement, opts: unknown) => unknown;
  tileLayer: (url: string, opts: unknown) => { addTo: (m: unknown) => void };
  circleMarker: (latlng: [number, number], opts: unknown) => LMarker;
};

function getL(): LLeaflet | null {
  if (typeof window === 'undefined') return null;
  return (window as unknown as { L?: LLeaflet }).L ?? null;
}

export default function MapView({ onMerchantClick }: Props) {
  const mapRef        = useRef<HTMLDivElement>(null);
  const leafletMapRef = useRef<unknown>(null);
  const markersRef    = useRef<Record<string, LMarker>>({});
  const { state }     = useApp();
  const [mapReady, setMapReady]     = useState(false);
  const [txnPins,  setTxnPins]      = useState<TxnPin[]>([]);

  // ── Load Leaflet CSS + JS once ───────────────────────────────────────────
  useEffect(() => {
    if (typeof window === 'undefined' || leafletMapRef.current) return;

    if (!document.getElementById('leaflet-css')) {
      const link  = document.createElement('link');
      link.id     = 'leaflet-css';
      link.rel    = 'stylesheet';
      link.href   = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
      document.head.appendChild(link);
    }

    if (document.getElementById('leaflet-js')) {
      initMap();
      return;
    }

    const script    = document.createElement('script');
    script.id       = 'leaflet-js';
    script.src      = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
    script.onload   = () => initMap();
    document.head.appendChild(script);
  }, []);

  const initMap = useCallback(() => {
    if (!mapRef.current || leafletMapRef.current) return;
    const L = getL();
    if (!L) return;

    const map = L.map(mapRef.current, {
      center: [51.505, -0.12], zoom: 13,
      zoomControl: true, attributionControl: false,
    });

    L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      { subdomains: 'abcd', maxZoom: 19 }
    ).addTo(map);

    leafletMapRef.current = map;

    MERCHANTS.forEach(m => {
      const marker = L.circleMarker([m.lat, m.lng], {
        radius: 10, fillColor: '#38BDF8', color: '#0ea5e9',
        weight: 2, opacity: 1, fillOpacity: 0.85,
      }).addTo(map);

      marker.bindTooltip(`
        <div style="background:#0B1117;border:1px solid #263447;border-radius:6px;padding:8px 10px;color:#F1F5F9;font-family:Inter,sans-serif;font-size:11px;min-width:130px">
          <div style="font-weight:700;color:#38BDF8;margin-bottom:3px">${m.name}</div>
          <div style="color:#94A3B8;font-size:10px">${m.category}</div>
          <div style="color:#475569;font-size:9px;margin-top:4px">Click to open terminal</div>
        </div>
      `, { className: 'rr-tooltip', permanent: false, direction: 'top', offset: [0, -12] });

      marker.on('click',     () => onMerchantClick(m.name));
      marker.on('mouseover', () => marker.setStyle({ radius: 13, fillColor: '#818CF8', color: '#6366f1' }));
      marker.on('mouseout',  () => marker.setStyle({ radius: 10, fillColor: '#38BDF8', color: '#0ea5e9' }));

      markersRef.current[m.id] = marker;
    });

    setMapReady(true);
  }, [onMerchantClick]);

  // ── React to new transactions — pulse pin on map ─────────────────────────
  useEffect(() => {
    if (!mapReady || !state.receipts.length) return;

    // Guard: map must still be alive
    if (!leafletMapRef.current) return;

    const L = getL();
    if (!L) return;

    const latest   = state.receipts[0];
    const merchant = MERCHANTS.find(m => m.name === latest.merchant);
    if (!merchant) return;

    // Safe addTo with null check
    try {
      const pulse = L.circleMarker([merchant.lat, merchant.lng], {
        radius: 10, fillColor: latest.approved ? '#4ADE80' : '#F87171',
        color:  latest.approved ? '#4ADE80' : '#F87171',
        weight: 2, opacity: 0.9, fillOpacity: 0.3,
      }).addTo(leafletMapRef.current);

      setTimeout(() => { try { pulse.remove(); } catch { /* already removed */ } }, 1500);
    } catch {
      // Map was unmounted — silently skip
      return;
    }

    // Update base marker colour
    const baseMarker = markersRef.current[merchant.id];
    if (baseMarker) {
      baseMarker.setStyle({
        fillColor: latest.approved ? '#4ADE80' : '#F87171',
        color:     latest.approved ? '#22c55e' : '#ef4444',
      });
      setTimeout(() => {
        try {
          baseMarker.setStyle({ fillColor: '#38BDF8', color: '#0ea5e9' });
        } catch { /* marker may be gone */ }
      }, 3000);
    }

    setTxnPins(prev => [
      { id: latest.id, lat: merchant.lat, lng: merchant.lng, approved: latest.approved, amt: latest.amt },
      ...prev.slice(0, 19),
    ]);
  }, [state.receipts, mapReady]);

  const legendStyle: CSSProperties = {
    position: 'absolute', bottom: 12, left: 12, zIndex: 1000,
    background: 'rgba(11,17,23,0.92)', border: '1px solid #263447',
    borderRadius: 8, padding: '8px 12px', fontSize: 10,
    backdropFilter: 'blur(8px)', display: 'flex', flexDirection: 'column', gap: 5,
  };

  const statsStyle: CSSProperties = {
    position: 'absolute', top: 12, right: 12, zIndex: 1000,
    background: 'rgba(11,17,23,0.92)', border: '1px solid #263447',
    borderRadius: 8, padding: '8px 12px', fontSize: 10,
    backdropFilter: 'blur(8px)', display: 'flex', flexDirection: 'column', gap: 4, minWidth: 140,
  };

  const approved = txnPins.filter(t => t.approved).length;
  const declined = txnPins.filter(t => !t.approved).length;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', background: '#030712' }}>
      <div ref={mapRef} style={{ width: '100%', height: '100%' }} />

      {!mapReady && (
        <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#030712', flexDirection: 'column', gap: 10 }}>
          <div style={{ width: 32, height: 32, border: '2px solid #263447', borderTop: '2px solid #38BDF8', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
          <span style={{ fontSize: 11, color: '#475569' }}>Loading map…</span>
          <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
        </div>
      )}

      {mapReady && (
        <div style={{ position: 'absolute', top: 12, left: 12, zIndex: 1000, background: 'rgba(11,17,23,0.92)', border: '1px solid #263447', borderRadius: 6, padding: '5px 10px', fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#38BDF8', backdropFilter: 'blur(8px)' }}>
          ● MERCHANT TERMINAL MAP — {MERCHANTS.length} LOCATIONS
        </div>
      )}

      {mapReady && txnPins.length > 0 && (
        <div style={statsStyle}>
          <div style={{ fontSize: 9, fontWeight: 700, color: '#475569', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 2 }}>Live Activity</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#4ADE80', display: 'inline-block' }} />
            <span style={{ color: '#94A3B8' }}>Approved</span>
            <span style={{ color: '#4ADE80', fontWeight: 700, marginLeft: 'auto', fontFamily: 'JetBrains Mono, monospace' }}>{approved}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#F87171', display: 'inline-block' }} />
            <span style={{ color: '#94A3B8' }}>Declined</span>
            <span style={{ color: '#F87171', fontWeight: 700, marginLeft: 'auto', fontFamily: 'JetBrains Mono, monospace' }}>{declined}</span>
          </div>
        </div>
      )}

      {mapReady && (
        <div style={legendStyle}>
          <div style={{ fontSize: 9, fontWeight: 700, color: '#475569', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 2 }}>Map Legend</div>
          {[
            { color: '#38BDF8', label: 'Merchant terminal'     },
            { color: '#4ADE80', label: 'Last txn: approved'    },
            { color: '#F87171', label: 'Last txn: declined'    },
            { color: '#818CF8', label: 'Hovered pin'           },
          ].map(({ color, label }) => (
            <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />
              <span style={{ color: '#94A3B8' }}>{label}</span>
            </div>
          ))}
        </div>
      )}

      <style>{`
        .rr-tooltip { background: transparent !important; border: none !important; box-shadow: none !important; }
        .leaflet-tooltip { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; }
        .leaflet-tooltip::before { display: none !important; }
      `}</style>
    </div>
  );
}