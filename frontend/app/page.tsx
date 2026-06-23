'use client';
import type { CSSProperties } from 'react';
import Header  from '@/components/shared/Header';
import Stage   from '@/components/shared/Stage';
import Sidebar from '@/components/shared/Sidebar';

const outerStyle: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  height: '100vh',
  overflow: 'hidden',
};

const innerStyle: CSSProperties = {
  display: 'flex',
  flex: 1,
  overflow: 'hidden',
};

export default function Home() {
  return (
    <div style={outerStyle}>
      <Header />
      <div style={innerStyle}>
        <Stage />
        <Sidebar />
      </div>
    </div>
  );
}
