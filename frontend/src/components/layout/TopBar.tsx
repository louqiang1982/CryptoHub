'use client';

import React from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { useRouter, usePathname } from '@/i18n/navigation';
import { Button } from '@/components/ui/button';
import { useSidebarStore } from '@/stores/sidebar';
import { localeNames, type Locale } from '@/i18n/config';
import {
  PanelLeftClose, PanelLeftOpen, RefreshCw, Bell,
  Globe, Sun, Moon, Monitor, Settings, User,
} from 'lucide-react';
import { useTheme } from 'next-themes';
import { cn } from '@/lib/utils';

export function TopBar() {
  const t = useTranslations('topbar');
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();
  const { isOpen, toggle } = useSidebarStore();
  const { theme, setTheme } = useTheme();
  const [showLangMenu, setShowLangMenu] = React.useState(false);

  const handleLocaleChange = (newLocale: string) => {
    router.replace(pathname, { locale: newLocale as Locale });
    setShowLangMenu(false);
  };

  const cycleTheme = () => {
    if (theme === 'light') setTheme('dark');
    else if (theme === 'dark') setTheme('system');
    else setTheme('light');
  };

  return (
    <header className="flex h-14 items-center gap-2 border-b border-[hsl(var(--border))] bg-[hsl(var(--background))] px-4">
      <Button variant="ghost" size="icon" onClick={toggle} title={t('toggleSidebar')}>
        {isOpen ? <PanelLeftClose className="h-5 w-5" /> : <PanelLeftOpen className="h-5 w-5" />}
      </Button>
      <div className="flex-1" />
      <Button variant="ghost" size="icon"><RefreshCw className="h-4 w-4" /></Button>
      <Button variant="ghost" size="icon" title={t('notifications')}><Bell className="h-4 w-4" /></Button>
      <div className="relative">
        <Button variant="ghost" size="icon" onClick={() => setShowLangMenu(!showLangMenu)} title={t('language')}>
          <Globe className="h-4 w-4" />
        </Button>
        {showLangMenu && (
          <div className="absolute end-0 top-full z-50 mt-1 w-40 rounded-md border border-[hsl(var(--border))] bg-[hsl(var(--popover))] p-1 shadow-lg">
            {Object.entries(localeNames).map(([key, name]) => (
              <button key={key} onClick={() => handleLocaleChange(key)} className={cn(
                'flex w-full items-center rounded-sm px-2 py-1.5 text-sm transition-colors',
                locale === key ? 'bg-[hsl(var(--accent))]' : 'hover:bg-[hsl(var(--accent))]'
              )}>{name}</button>
            ))}
          </div>
        )}
      </div>
      <Button variant="ghost" size="icon" onClick={cycleTheme} title={t('theme')}>
        {theme === 'dark' ? <Moon className="h-4 w-4" /> : theme === 'light' ? <Sun className="h-4 w-4" /> : <Monitor className="h-4 w-4" />}
      </Button>
      <Button variant="ghost" size="icon"><Settings className="h-4 w-4" /></Button>
      <Button variant="ghost" size="icon"><User className="h-4 w-4" /></Button>
    </header>
  );
}