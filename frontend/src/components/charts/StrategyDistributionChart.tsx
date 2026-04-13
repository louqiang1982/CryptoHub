'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const data = [
  { name: 'Trend Following', value: 35, color: '#3b82f6' },
  { name: 'Mean Reversion', value: 25, color: '#8b5cf6' },
  { name: 'Scalping', value: 20, color: '#06b6d4' },
  { name: 'Arbitrage', value: 12, color: '#f59e0b' },
  { name: 'Grid Trading', value: 8, color: '#10b981' },
];

export default function StrategyDistributionChart() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={3}
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          labelLine={false}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} strokeWidth={0} />
          ))}
        </Pie>
        <Tooltip
          formatter={(value: number) => [`${value}%`, 'Allocation']}
          contentStyle={{
            backgroundColor: 'hsl(var(--popover))',
            border: '1px solid hsl(var(--border))',
            borderRadius: '8px',
            color: 'hsl(var(--popover-foreground))',
          }}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          formatter={(value: string) => (
            <span style={{ color: 'hsl(var(--foreground))', fontSize: '12px' }}>{value}</span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
