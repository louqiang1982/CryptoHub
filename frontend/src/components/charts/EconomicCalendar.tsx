'use client';

import { useState, useMemo } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface CalendarEvent {
  id: string;
  time: string;
  title: string;
  impact: 'high' | 'medium' | 'low';
  currency: string;
  actual?: string;
  forecast?: string;
  previous?: string;
}

function generateEvents(date: Date): CalendarEvent[] {
  const events: CalendarEvent[] = [];
  const d = date.getDate();
  const m = date.getMonth();

  // Generate deterministic events based on date
  const seed = d * 31 + m * 397;
  const count = (seed % 4) + 1;

  const templates = [
    { title: 'CPI (YoY)', currency: 'USD', impact: 'high' as const },
    { title: 'GDP Growth Rate', currency: 'EUR', impact: 'high' as const },
    { title: 'Non-Farm Payrolls', currency: 'USD', impact: 'high' as const },
    { title: 'Interest Rate Decision', currency: 'GBP', impact: 'high' as const },
    { title: 'Retail Sales (MoM)', currency: 'USD', impact: 'medium' as const },
    { title: 'PMI Manufacturing', currency: 'CNY', impact: 'medium' as const },
    { title: 'Unemployment Rate', currency: 'JPY', impact: 'medium' as const },
    { title: 'Trade Balance', currency: 'AUD', impact: 'low' as const },
    { title: 'Building Permits', currency: 'CAD', impact: 'low' as const },
    { title: 'Consumer Confidence', currency: 'EUR', impact: 'medium' as const },
  ];

  for (let i = 0; i < count; i++) {
    const tpl = templates[(seed + i * 7) % templates.length];
    const hour = 8 + ((seed + i * 3) % 12);
    const minute = ((seed + i * 13) % 4) * 15;
    const isPast = date < new Date();

    events.push({
      id: `${d}-${m}-${i}`,
      time: `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`,
      title: tpl.title,
      impact: tpl.impact,
      currency: tpl.currency,
      actual: isPast ? `${(2.5 + (seed + i) % 30 * 0.1).toFixed(1)}%` : undefined,
      forecast: `${(2.3 + (seed + i * 2) % 20 * 0.1).toFixed(1)}%`,
      previous: `${(2.1 + (seed + i * 3) % 25 * 0.1).toFixed(1)}%`,
    });
  }

  return events.sort((a, b) => a.time.localeCompare(b.time));
}

function impactColor(impact: string): string {
  switch (impact) {
    case 'high': return 'destructive';
    case 'medium': return 'default';
    default: return 'secondary';
  }
}

export default function EconomicCalendar() {
  const [selectedDate, setSelectedDate] = useState(new Date());

  const events = useMemo(() => generateEvents(selectedDate), [selectedDate]);

  const weekDates = useMemo(() => {
    const start = new Date(selectedDate);
    start.setDate(start.getDate() - start.getDay() + 1); // Monday
    return Array.from({ length: 7 }, (_, i) => {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      return d;
    });
  }, [selectedDate]);

  const goWeek = (delta: number) => {
    const d = new Date(selectedDate);
    d.setDate(d.getDate() + delta * 7);
    setSelectedDate(d);
  };

  const isToday = (d: Date) => {
    const now = new Date();
    return d.getFullYear() === now.getFullYear() && d.getMonth() === now.getMonth() && d.getDate() === now.getDate();
  };

  const isSameDay = (a: Date, b: Date) =>
    a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

  return (
    <div className="space-y-4">
      {/* Week navigation */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={() => goWeek(-1)}>
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <div className="flex gap-1">
          {weekDates.map((d) => (
            <Button
              key={d.toISOString()}
              variant={isSameDay(d, selectedDate) ? 'default' : isToday(d) ? 'outline' : 'ghost'}
              size="sm"
              className="flex flex-col items-center px-2 py-1 h-auto min-w-[40px]"
              onClick={() => setSelectedDate(d)}
            >
              <span className="text-[10px] uppercase">
                {d.toLocaleDateString('en', { weekday: 'short' })}
              </span>
              <span className="text-sm font-semibold">{d.getDate()}</span>
            </Button>
          ))}
        </div>
        <Button variant="ghost" size="sm" onClick={() => goWeek(1)}>
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      {/* Events list */}
      <div className="space-y-2 max-h-[300px] overflow-y-auto">
        {events.length === 0 ? (
          <div className="text-center text-sm text-muted-foreground py-8">
            No events scheduled
          </div>
        ) : (
          events.map((event) => (
            <div
              key={event.id}
              className="flex items-start gap-3 p-2 rounded-lg border border-[hsl(var(--border))] hover:bg-[hsl(var(--muted))] transition-colors"
            >
              <div className="text-xs text-muted-foreground font-mono min-w-[45px] pt-0.5">
                {event.time}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm truncate">{event.title}</span>
                  <Badge variant={impactColor(event.impact) as 'default' | 'secondary' | 'destructive'} className="text-[10px] px-1.5 py-0">
                    {event.impact}
                  </Badge>
                </div>
                <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                  <span className="font-semibold text-foreground">{event.currency}</span>
                  {event.actual && (
                    <span>Actual: <span className="font-medium text-foreground">{event.actual}</span></span>
                  )}
                  <span>Forecast: {event.forecast}</span>
                  <span>Previous: {event.previous}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
