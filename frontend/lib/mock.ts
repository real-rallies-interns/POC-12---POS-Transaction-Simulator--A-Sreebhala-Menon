import type { EntryMethod, Transaction, DeclineReason, EmvStep } from '@/types';

const MERCHANTS = ['Corner Deli','Urban Coffee','QuickMart','The Food Hall','Pharmacy Plus','Fuel & Go','BookNook','Electronics Hub'];
const BRANDS    = ['Visa','Mastercard','Amex','Discover'];

export const DECLINE_POOL: DeclineReason[] = [
  { code:'51', label:'Insufficient Funds',  category:'Balance'      },
  { code:'55', label:'Incorrect PIN',       category:'Auth Failure' },
  { code:'91', label:'Bank Unavailable',    category:'Network'      },
  { code:'05', label:'Do Not Honor',        category:'Issuer Block' },
  { code:'76', label:'Chip Read Error',     category:'Hardware'     },
  { code:'54', label:'Expired Card',        category:'Data Error'   },
  { code:'57', label:'Not Permitted',       category:'Issuer Block' },
  { code:'62', label:'Restricted Card',     category:'Issuer Block' },
  { code:'14', label:'Invalid Card Number', category:'Data Error'   },
  { code:'96', label:'System Error',        category:'Technical'    },
];

export const EMV_TEMPLATE: Array<{ ph: string; tag: string; val: (a: number) => string; desc: string }> = [
  { ph:'SELECT APPLICATION',  tag:'84',   val:()=>'A0000000031010',                               desc:'AID — Visa Credit'         },
  { ph:'GET PROCESSING OPT',  tag:'9F02', val:(a)=>String(Math.round(a*100)).padStart(12,'0'),    desc:'Amount encoded (cents)'    },
  { ph:'READ RECORD',         tag:'5F28', val:()=>'0840',                                          desc:'Issuer Country: USA'       },
  { ph:'OFFLINE DATA AUTH',   tag:'9F27', val:()=>'40',                                            desc:'TC — Transaction Cert'     },
  { ph:'CARDHOLDER VERIFY',   tag:'9F34', val:()=>'420300',                                        desc:'CVM: Online PIN'           },
  { ph:'TERMINAL RISK MGMT',  tag:'9F1A', val:()=>'0840',                                          desc:'Terminal Country: USA'     },
  { ph:'FIRST GENERATE AC',   tag:'9F26', val:()=>rHex(16),                                        desc:'Application Cryptogram'    },
  { ph:'ONLINE AUTH REQUEST', tag:'9F37', val:()=>rHex(8),                                         desc:'Unpredictable Number'      },
  { ph:'ISSUER RESPONSE',     tag:'8A',   val:()=>'3030',                                          desc:'Auth: 00 Approved'         },
  { ph:'SECOND GENERATE AC',  tag:'9F26', val:()=>rHex(16),                                        desc:'TC — Completed'            },
];

export function rHex(n: number): string {
  return Array.from({ length: n }, () => Math.floor(Math.random() * 16).toString(16)).join('').toUpperCase();
}
export function rn(a: number, b: number): number { return Math.random() * (b - a) + a; }
export function ri(a: number, b: number): number { return Math.floor(rn(a, b)); }
export function rAmt(): string { return rn(2.5, 450).toFixed(2); }
export function rCard() { return { brand: BRANDS[ri(0, 4)], last4: String(ri(1000, 9999)) }; }
export function rMerch(): string { return MERCHANTS[ri(0, MERCHANTS.length)]; }
export function rDecline(): DeclineReason {
  return DECLINE_POOL[ri(0, DECLINE_POOL.length)];
}
export function tNow(): string { return new Date().toTimeString().slice(0, 8); }

export function buildMockTransaction(method: EntryMethod): Transaction {
  const approved = Math.random() > 0.22;
  return {
    id:           'TXN-' + rHex(10),
    time:         tNow(),
    merchant:     rMerch(),
    amt:          rAmt(),
    card:         rCard(),
    method,
    approved,
    decline:      approved ? null : rDecline(),
    auth:         rHex(6),
    emv:          [],
    storeForward: false,
  };
}

export function buildEmvSteps(amount: number): EmvStep[] {
  return EMV_TEMPLATE.map(s => ({
    phase: s.ph, tag: s.tag, value: s.val(amount), desc: s.desc,
  }));
}

export function buildSampleRecords(count = 20): Record<string, unknown>[] {
  const methods: EntryMethod[] = ['Contactless','Chip','Swipe','Manual Entry'];
  return Array.from({ length: count }, (_, i) => {
    const amt   = rAmt();
    const card  = rCard();
    const appr  = Math.random() > 0.22;
    const dec   = appr ? null : rDecline();
    return {
      txn_id:        'TXN-' + rHex(8),
      timestamp:     new Date(Date.now() - i * 900_000).toISOString(),
      merchant:      rMerch(),
      amount_usd:    parseFloat(amt),
      card_brand:    card.brand,
      last4:         card.last4,
      entry_method:  methods[ri(0, 4)],
      status:        appr ? 'APPROVED' : 'DECLINED',
      decline_code:  dec?.code ?? '',
      decline_reason:dec?.label ?? '',
      offline_auth:  Math.random() < 0.12,
      cfpb_compliant:true,
      source:        'Synthetic — Real Rails PoC #12',
    };
  });
}
