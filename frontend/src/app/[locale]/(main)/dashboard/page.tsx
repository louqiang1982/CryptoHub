import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TrendingUp, TrendingDown, DollarSign, Target, Activity, Zap } from 'lucide-react';

export default async function DashboardPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('dashboard');

  const stats = [
    { key: 'totalEquity', value: '$125,430.50', change: '+5.25%', icon: DollarSign, trend: 'up' },
    { key: 'winRate', value: '68.5%', change: '+2.1%', icon: Target, trend: 'up' },
    { key: 'plRatio', value: '2.34', change: '-0.15', icon: TrendingUp, trend: 'down' },
    { key: 'maxDrawdown', value: '8.2%', change: '+0.5%', icon: TrendingDown, trend: 'down' },
    { key: 'totalTrades', value: '1,247', change: '+23', icon: Activity, trend: 'up' },
    { key: 'runningStrategies', value: '8', change: '+2', icon: Zap, trend: 'up' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">{t('todayPnl')}</Button>
          <Button variant="outline">{t('weekPnl')}</Button>
          <Button variant="default">{t('monthPnl')}</Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          const isPositive = stat.trend === 'up';
          return (
            <Card key={stat.key}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{t(stat.key as keyof typeof t)}</CardTitle>
                <Icon className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className={`text-xs ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.change} from last month
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>{t('profitCalendar')}</CardTitle>
            <CardDescription>Monthly performance overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-[hsl(var(--muted-foreground))]">
              Profit Calendar Chart Placeholder
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('strategyDistribution')}</CardTitle>
            <CardDescription>Active strategy breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-[hsl(var(--muted-foreground))]">
              Strategy Distribution Chart Placeholder
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('drawdownCurve')}</CardTitle>
            <CardDescription>Risk management overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-[hsl(var(--muted-foreground))]">
              Drawdown Curve Chart Placeholder
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('tradingHours')}</CardTitle>
            <CardDescription>Best performance times</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-[hsl(var(--muted-foreground))]">
              Trading Hours Heatmap Placeholder
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}