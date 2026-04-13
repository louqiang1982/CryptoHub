'use client';

import { useEffect, useState, useMemo } from 'react';
import { dashboardApi } from '@/lib/api/client';

interface DayData {
  date: string;
  profit: number;
}

// Generate fallback month data
function generateMonthData(): DayData[] {
  const data: DayData[] = [];
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  for (let d = 1; d <= daysInMonth; d++) {
    const seed = Math.sin(d * 1.3) * 800 + Math.cos(d * 0.7) * 400;
    data.push({
      date: `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`,
      profit: Math.round(seed * 100) / 100,
    });
  }
  return data;
}

function getColor(value: number): string {
  if (value > 500) return '#16a34a';
  if (value > 0) return '#4ade80';
  if (value === 0) return '#e5e7eb';
  if (value > -300) return '#f87171';
  return '#dc2626';
}

export default function ProfitCalendarChart() {
  const fallback = useMemo(() => generateMonthData(), []);
  const [data, setData] = useState<DayData[]>(fallback);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const resp = await dashboardApi.getProfitCalendar('');
        const items = resp?.data;
        if (!cancelled && Array.isArray(items) && items.length > 0) {
          setData(items);
        }
      } catch {
        // keep fallback data
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const totalProfit = data.reduce((sum, d) => sum + d.profit, 0);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">Monthly P&amp;L</span>
        <span className={totalProfit >= 0 ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'}>
          {totalProfit >= 0 ? '+' : ''}{totalProfit.toFixed(2)} USDT
        </span>
      </div>
      <div className="grid grid-cols-7 gap-1">
        {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((d, i) => (
          <div key={i} className="text-center text-xs text-muted-foreground font-medium py-1">{d}</div>
        ))}
        {data.map((day) => {
          const date = new Date(day.date);
          const dayOfWeek = date.getDay();
          const dayNum = date.getDate();
          return (
            <div
              key={day.date}
              className="aspect-square rounded-sm flex items-center justify-center text-xs font-medium text-white cursor-pointer transition-transform hover:scale-110"
              style={{
                backgroundColor: getColor(day.profit),
                gridColumnStart: dayNum === 1 ? dayOfWeek + 1 : undefined,
              }}
              title={`${day.date}: ${day.profit >= 0 ? '+' : ''}${day.profit.toFixed(2)} USDT`}
            >
              {dayNum}
            </div>
          );
        })}
      </div>
      <div className="flex items-center justify-center gap-4 text-xs text-muted-foreground">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#16a34a' }} />
          <span>&gt;500</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#4ade80' }} />
          <span>0~500</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#f87171' }} />
          <span>-300~0</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#dc2626' }} />
          <span>&lt;-300</span>
        </div>
      </div>
    </div>
  );
}
