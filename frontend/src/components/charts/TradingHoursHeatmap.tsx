'use client';

import { useMemo } from 'react';

const HOURS = Array.from({ length: 24 }, (_, i) => i);
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

function generateHeatmapData(): number[][] {
  return DAYS.map(() =>
    HOURS.map(() => Math.round((Math.random() * 200 - 50) * 100) / 100)
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
  const data = useMemo(() => generateHeatmapData(), []);
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
      {DAYS.map((day, di) => (
        <div key={day} className="flex items-center">
          <div className="w-10 text-xs text-muted-foreground">{day}</div>
          <div className="flex-1 grid grid-cols-24 gap-px">
            {HOURS.map((h) => (
              <div
                key={h}
                className="aspect-square rounded-sm cursor-pointer transition-transform hover:scale-125"
                style={{ backgroundColor: getHeatColor(data[di][h], maxVal) }}
                title={`${day} ${h}:00 — ${data[di][h] >= 0 ? '+' : ''}${data[di][h].toFixed(2)} USDT`}
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
