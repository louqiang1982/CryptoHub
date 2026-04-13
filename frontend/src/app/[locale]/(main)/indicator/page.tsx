import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  LineChart, TrendingUp, Maximize2, 
  Settings, PaintBucket, Layers, Zap 
} from 'lucide-react';
import dynamic from 'next/dynamic';

const KLineChart = dynamic(() => import('@/components/charts/KLineChart'), { ssr: false });

export default async function IndicatorPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('indicator');

  const timeframes = ['1m', '5m', '15m', '30m', '1H', '4H', '1D', '1W'];
  const indicators = ['SMA', 'EMA', 'RSI', 'MACD', 'BB', 'ATR', 'CCI', 'WR', 'MFI', 'ADX', 'OBV', 'KDJ'];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">{t('quickTrade')}</Button>
          <Button variant="outline">
            <Maximize2 className="mr-2 h-4 w-4" />
            {t('fullscreen')}
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        <div className="lg:col-span-3 space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>BTC/USDT Chart</CardTitle>
                <div className="flex gap-1">
                  {timeframes.map((tf) => (
                    <Button key={tf} variant={tf === '1H' ? 'default' : 'outline'} size="sm">
                      {t(`timeframes.${tf}` as keyof typeof t)}
                    </Button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <KLineChart symbol="BTC/USDT" interval="1H" />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Indicator Toolbar</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {indicators.map((indicator) => (
                  <Button key={indicator} variant="outline" size="sm">
                    {t(`indicators.${indicator}` as keyof typeof t)}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('drawingTools')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" size="sm" className="w-full justify-start">
                <PaintBucket className="mr-2 h-4 w-4" />
                Trend Line
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <LineChart className="mr-2 h-4 w-4" />
                Horizontal Line
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <TrendingUp className="mr-2 h-4 w-4" />
                Fibonacci
              </Button>
              <Button variant="outline" size="sm" className="w-full justify-start">
                <Layers className="mr-2 h-4 w-4" />
                Rectangle
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('myIndicators')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div>
                  <div className="font-medium">Custom RSI</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">Period: 14</div>
                </div>
                <Button size="sm" variant="ghost">
                  <Settings className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div>
                  <div className="font-medium">MA Cross</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">9/21 EMA</div>
                </div>
                <Button size="sm" variant="ghost">
                  <Settings className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('purchasedIndicators')}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div>
                  <div className="font-medium">Pro Momentum</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">Premium</div>
                </div>
                <div className="flex gap-1">
                  <Button size="sm" variant="ghost">
                    <Settings className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="default">
                    <Zap className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div>
                  <div className="font-medium">Smart Volume</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">Premium</div>
                </div>
                <div className="flex gap-1">
                  <Button size="sm" variant="ghost">
                    <Settings className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="default">
                    <Zap className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Market Data</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Price:</span>
                  <span className="font-medium">$45,230.50</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">24h Change:</span>
                  <span className="text-green-600">+2.3%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Volume:</span>
                  <span className="font-medium">$2.8B</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Market Cap:</span>
                  <span className="font-medium">$885B</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}