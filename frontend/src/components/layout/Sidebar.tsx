'use client';

import React from 'react';
import { useTranslations } from 'next-intl';
import { usePathname, Link } from '@/i18n/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard, Brain, LineChart, Store, Bot,
  Wallet, User, Crown, Shield, HelpCircle,
} from 'lucide-react';
import { useSidebarStore } from '@/stores/sidebar';

const mainNavItems = [
  { key: 'dashboard', href: '/dashboard', icon: LayoutDashboard },
  { key: 'aiAnalysis', href: '/ai-analysis', icon: Brain },
  { key: 'indicator', href: '/indicator', icon: LineChart },
  { key: 'indicatorMarket', href: '/indicator-market', icon: Store },
  { key: 'trading', href: '/trading', icon: Bot },
  { key: 'portfolio', href: '/portfolio', icon: Wallet },
  { key: 'profile', href: '/profile', icon: User },
  { key: 'membership', href: '/membership', icon: Crown },
  { key: 'admin', href: '/admin', icon: Shield },
];

export function Sidebar() {
  const t = useTranslations('nav');
  const pathname = usePathname();
  const { isOpen } = useSidebarStore();

  return (
    <aside className={cn(
      'hidden md:flex flex-col border-e border-[hsl(var(--sidebar-border))] bg-[hsl(var(--sidebar-background))] transition-all duration-300',
      isOpen ? 'w-64' : 'w-16'
    )}>
      <div className="flex h-14 items-center gap-2 border-b border-[hsl(var(--sidebar-border))] px-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[hsl(var(--sidebar-primary))]">
          <span className="text-sm font-bold text-[hsl(var(--sidebar-primary-foreground))]">C</span>
        </div>
        {isOpen && <span className="text-lg font-bold text-[hsl(var(--sidebar-foreground))]">CryptoHub</span>}
      </div>
      <nav className="flex-1 space-y-1 p-2 overflow-y-auto">
        {mainNavItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link key={item.key} href={item.href} className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors',
              isActive
                ? 'bg-[hsl(var(--sidebar-accent))] text-[hsl(var(--sidebar-primary))] font-medium'
                : 'text-[hsl(var(--sidebar-foreground))] hover:bg-[hsl(var(--sidebar-accent))]'
            )}>
              <Icon className="h-5 w-5 shrink-0" />
              {isOpen && <span>{t(item.key)}</span>}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-[hsl(var(--sidebar-border))] p-2">
        <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-[hsl(var(--sidebar-foreground))] hover:bg-[hsl(var(--sidebar-accent))] transition-colors">
          <HelpCircle className="h-5 w-5 shrink-0" />
          {isOpen && <span>{t('settings')}</span>}
        </button>
      </div>
    </aside>
  );
}