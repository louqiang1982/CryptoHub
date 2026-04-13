'use client';

import { useEffect, useRef, useCallback, useState } from 'react';
import { init, dispose, CandleType, type Chart } from 'klinecharts';
import { marketApi } from '@/lib/api/client';

interface KLineChartProps {
  symbol?: string;
  interval?: string;
}

function generateKlineData(count: number) {
  const data = [];
  let basePrice = 45000;
  const now = Date.now();

  for (let i = 0; i < count; i++) {
    const timestamp = now - (count - i) * 3600000;
    const open = basePrice + (Math.random() - 0.5) * 500;
    const close = open + (Math.random() - 0.5) * 800;
    const high = Math.max(open, close) + Math.random() * 300;
    const low = Math.min(open, close) - Math.random() * 300;
    const volume = Math.random() * 1000 + 200;
    basePrice = close;

    data.push({ timestamp, open, high, low, close, volume });
  }
  return data;
}

export default function KLineChart({ symbol = 'BTC/USDT', interval = '1H' }: KLineChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<Chart | null>(null);
  const [, setLoading] = useState(true);

  const loadData = useCallback(async (chart: Chart) => {
    try {
      const resp = await marketApi.getKlines(symbol, interval, 200);
      if (Array.isArray(resp) && resp.length > 0) {
        const data = resp.map((k: Record<string, unknown>) => ({
          timestamp: Number(k.timestamp) || 0,
          open: Number(k.open) || 0,
          high: Number(k.high) || 0,
          low: Number(k.low) || 0,
          close: Number(k.close) || 0,
          volume: Number(k.volume) || 0,
        }));
        chart.applyNewData(data);
        return;
      }
    } catch {
      // fall through to generated data
    }
    chart.applyNewData(generateKlineData(200));
  }, [symbol, interval]);

  const initChart = useCallback(() => {
    if (!containerRef.current) return;

    // Dispose previous chart
    if (chartRef.current) {
      dispose(containerRef.current);
      chartRef.current = null;
    }

    const chart = init(containerRef.current, {
      styles: {
        grid: {
          show: true,
          horizontal: { color: 'rgba(150, 150, 150, 0.1)' },
          vertical: { color: 'rgba(150, 150, 150, 0.1)' },
        },
        candle: {
          type: CandleType.CandleSolid,
          priceMark: {
            show: true,
            high: { show: true, color: '#16a34a' },
            low: { show: true, color: '#dc2626' },
            last: { show: true },
          },
          bar: {
            upColor: '#16a34a',
            downColor: '#dc2626',
            upBorderColor: '#16a34a',
            downBorderColor: '#dc2626',
            upWickColor: '#16a34a',
            downWickColor: '#dc2626',
          },
        },
      },
    });

    if (chart) {
      chartRef.current = chart;

      // Create MA indicator
      chart.createIndicator('MA', false, { id: 'candle_pane' });
      chart.createIndicator('VOL');

      // Load data from API or fallback
      loadData(chart).finally(() => setLoading(false));
    }
  }, [loadData]);

  useEffect(() => {
    initChart();
    const container = containerRef.current;

    return () => {
      if (container) {
        dispose(container);
      }
    };
  }, [initChart, symbol, interval]);

  return (
    <div className="w-full">
      <div className="flex items-center gap-2 mb-2 text-sm text-muted-foreground">
        <span className="font-semibold text-foreground">{symbol}</span>
        <span className="text-xs bg-muted px-2 py-0.5 rounded">{interval}</span>
      </div>
      <div ref={containerRef} className="w-full h-[460px]" />
    </div>
  );
}
