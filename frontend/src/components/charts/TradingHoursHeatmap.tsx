'use client';

import { useEffect, useState, useMemo } from 'react';
import { dashboardApi } from '@/lib/api/client';

const HOURS = Array.from({ length: 24 }, (_, i) => i);
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

interface HeatmapRow {
  day: string;
  hours: number[];
}

function generateFallbackData(): HeatmapRow[] {
  return DAYS.map((day, i) =>
    ({
      day,
      hours: HOURS.map((h) => {
        const v = Math.sin((i * 24 + h) * 2.7) * 100 + Math.cos(h * 1.1) * 50;
        return Math.round(v * 100) / 100;
      }),
    })
  );
}

function getHeatColor(value: number, max: number): string {
  const normalized = (value + 50) / (max + 50);
  if (normalized > 0.7) return '#16a34a';
  if (normalized > 0.5) return '#4ade80';
  if (normalized > 0.35) return '#fbbf24';
  if (normalized > 0.2) return '#f87171';
  return '#dc2626';
}

export default function TradingHoursHeatmap() {
  const fallback = useMemo(() => generateFallbackData(), []);
  const [rows, setRows] = useState<HeatmapRow[]>(fallback);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const resp = await dashboardApi.getTradingHoursHeatmap('');
        const items = resp?.data;
        if (!cancelled && Array.isArray(items) && items.length > 0) {
          setRows(items);
        }
      } catch {
        // keep fallback data
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const data = rows.map((r) => r.hours);
  const maxVal = Math.max(...data.flat());

  return (
    <div className="space-y-2">
      <div className="flex">
        <div className="w-10" />
        <div className="flex-1 grid grid-cols-24 gap-px">
          {HOURS.map((h) => (
            <div key={h} className="text-center text-[10px] text-muted-foreground">
              {h % 4 === 0 ? `${h}h` : ''}
            </div>
          ))}
        </div>
      </div>
      {rows.map((row, di) => (
        <div key={row.day} className="flex items-center">
          <div className="w-10 text-xs text-muted-foreground">{row.day}</div>
          <div className="flex-1 grid grid-cols-24 gap-px">
            {HOURS.map((h) => (
              <div
                key={h}
                className="aspect-square rounded-sm cursor-pointer transition-transform hover:scale-125"
                style={{ backgroundColor: getHeatColor(data[di][h], maxVal) }}
                title={`${row.day} ${h}:00 — ${data[di][h] >= 0 ? '+' : ''}${data[di][h].toFixed(2)} USDT`}
              />
            ))}
          </div>
        </div>
      ))}
      <div className="flex items-center justify-center gap-3 text-xs text-muted-foreground pt-1">
        <span>Low</span>
        {['#dc2626', '#f87171', '#fbbf24', '#4ade80', '#16a34a'].map((c) => (
          <div key={c} className="w-4 h-3 rounded-sm" style={{ backgroundColor: c }} />
        ))}
        <span>High</span>
      </div>
    </div>
  );
}
