'use client';

import React from 'react';
import { useTranslations } from 'next-intl';
import { usePathname, Link } from '@/i18n/navigation';
import { cn } from '@/lib/utils';
import { LayoutDashboard, Brain, LineChart, Bot, User } from 'lucide-react';

const tabItems = [
  { key: 'dashboard', href: '/dashboard', icon: LayoutDashboard },
  { key: 'aiAnalysis', href: '/ai-analysis', icon: Brain },
  { key: 'indicator', href: '/indicator', icon: LineChart },
  { key: 'trading', href: '/trading', icon: Bot },
  { key: 'profile', href: '/profile', icon: User },
];

export function BottomTabBar() {
  const t = useTranslations('nav');
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 start-0 end-0 z-50 flex border-t border-[hsl(var(--border))] bg-[hsl(var(--background))] md:hidden">
      {tabItems.map((item) => {
        const isActive = pathname.startsWith(item.href);
        const Icon = item.icon;
        return (
          <Link key={item.key} href={item.href} className={cn(
            'flex flex-1 flex-col items-center gap-1 py-2 text-xs transition-colors',
            isActive ? 'text-[hsl(var(--primary))]' : 'text-[hsl(var(--muted-foreground))]'
          )}>
            <Icon className="h-5 w-5" />
            <span>{t(item.key)}</span>
          </Link>
        );
      })}
    </nav>
  );
}