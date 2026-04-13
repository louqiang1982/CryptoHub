import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CryptoHub - Crypto AI Trading Platform',
  description: 'Professional crypto AI quantitative trading platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children;
}