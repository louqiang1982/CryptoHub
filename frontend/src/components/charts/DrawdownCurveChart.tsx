'use client';

import { useEffect, useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { dashboardApi } from '@/lib/api/client';

function generateFallbackData() {
  return Array.from({ length: 90 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (90 - i));
    const drawdown = -(Math.abs(Math.sin(i / 10)) * 12 * Math.abs(Math.sin(i / 10)));
    return {
      date: `${date.getMonth() + 1}/${date.getDate()}`,
      drawdown: Number(drawdown.toFixed(2)),
    };
  });
}

interface DrawdownPoint {
  date: string;
  drawdown: number;
}

export default function DrawdownCurveChart() {
  const [data, setData] = useState<DrawdownPoint[]>(generateFallbackData);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const resp = await dashboardApi.getDrawdownCurve('');
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

  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <defs>
          <linearGradient id="drawdownGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
          tickLine={false}
          interval={14}
        />
        <YAxis
          tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
          tickLine={false}
          tickFormatter={(v) => `${v}%`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'hsl(var(--popover))',
            border: '1px solid hsl(var(--border))',
            borderRadius: '8px',
            color: 'hsl(var(--popover-foreground))',
          }}
          formatter={(value: number) => [`${value.toFixed(2)}%`, 'Drawdown']}
        />
        <Area
          type="monotone"
          dataKey="drawdown"
          stroke="#ef4444"
          fill="url(#drawdownGradient)"
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
