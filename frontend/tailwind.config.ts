import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        rr: {
          bg:       '#030712',
          surface:  '#0B1117',
          surface2: '#0d1520',
          surface3: '#111c2a',
          border:   '#1F2937',
          border2:  '#263447',
          border3:  '#2d3f55',
          cyan:     '#38BDF8',
          indigo:   '#818CF8',
          green:    '#4ADE80',
          red:      '#F87171',
          amber:    '#FBBF24',
          violet:   '#C084FC',
          text:     '#F1F5F9',
          text2:    '#94A3B8',
          text3:    '#475569',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
