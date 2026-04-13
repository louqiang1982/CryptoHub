'use client';

import React from 'react';
import { useTranslations } from 'next-intl';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Sun, Moon, Monitor } from 'lucide-react';

const presetColors = [
  { name: 'blue', value: '221.2 83.2% 53.3%' },
  { name: 'orange', value: '24.6 95% 53.1%' },
  { name: 'green', value: '142.1 76.2% 36.3%' },
  { name: 'purple', value: '262.1 83.3% 57.8%' },
  { name: 'red', value: '0 84.2% 60.2%' },
  { name: 'teal', value: '172.5 66% 50.4%' },
  { name: 'pink', value: '330 81% 60%' },
  { name: 'amber', value: '38 92% 50%' },
];

export function ThemeCustomizer() {
  const t = useTranslations('theme');
  const { theme, setTheme } = useTheme();
  const [primaryColor, setPrimaryColor] = React.useState(presetColors[0].value);

  const applyColor = (color: string) => {
    setPrimaryColor(color);
    document.documentElement.style.setProperty('--primary', color);
    localStorage.setItem('cryptohub-primary-color', color);
  };

  React.useEffect(() => {
    const saved = localStorage.getItem('cryptohub-primary-color');
    if (saved) { setPrimaryColor(saved); document.documentElement.style.setProperty('--primary', saved); }
  }, []);

  return (
    <div className="space-y-6 p-4">
      <div>
        <h3 className="mb-3 text-sm font-medium">{t('mode')}</h3>
        <div className="flex gap-2">
          <Button variant={theme === 'light' ? 'default' : 'outline'} size="sm" onClick={() => setTheme('light')}>
            <Sun className="me-2 h-4 w-4" />{t('light')}
          </Button>
          <Button variant={theme === 'dark' ? 'default' : 'outline'} size="sm" onClick={() => setTheme('dark')}>
            <Moon className="me-2 h-4 w-4" />{t('dark')}
          </Button>
          <Button variant={theme === 'system' ? 'default' : 'outline'} size="sm" onClick={() => setTheme('system')}>
            <Monitor className="me-2 h-4 w-4" />{t('system')}
          </Button>
        </div>
      </div>
      <div>
        <h3 className="mb-3 text-sm font-medium">{t('presetColors')}</h3>
        <div className="flex flex-wrap gap-2">
          {presetColors.map((color) => (
            <button key={color.name} onClick={() => applyColor(color.value)}
              className={cn('h-8 w-8 rounded-full border-2 transition-transform hover:scale-110',
                primaryColor === color.value ? 'border-[hsl(var(--foreground))] scale-110' : 'border-transparent'
              )} style={{ backgroundColor: `hsl(${color.value})` }} title={color.name} />
          ))}
        </div>
      </div>
      <div>
        <h3 className="mb-3 text-sm font-medium">{t('customColor')}</h3>
        <input type="color" onChange={(e) => {
          const hex = e.target.value;
          const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
          const max = Math.max(r, g, b) / 255, min = Math.min(r, g, b) / 255;
          const l = (max + min) / 2, d = max - min;
          const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));
          let h = 0;
          if (d !== 0) { if (max === r / 255) h = ((g / 255 - b / 255) / d) % 6; else if (max === g / 255) h = (b / 255 - r / 255) / d + 2; else h = (r / 255 - g / 255) / d + 4; }
          h = Math.round(h * 60); if (h < 0) h += 360;
          applyColor(`${h} ${Math.round(s * 100)}% ${Math.round(l * 100)}%`);
        }} className="h-10 w-20 cursor-pointer rounded border border-[hsl(var(--border))]" />
      </div>
    </div>
  );
}