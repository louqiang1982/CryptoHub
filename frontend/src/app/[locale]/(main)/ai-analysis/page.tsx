import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Brain, TrendingUp, TrendingDown, Star, Plus } from 'lucide-react';

export default async function AIAnalysisPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('aiAnalysis');

  const marketTabs = ['crypto', 'commodities', 'sectors', 'forex'];
  const assets = [
    { symbol: 'BTC', name: 'Bitcoin', price: 45230, change: 2.3, signal: 'buy', confidence: 85 },
    { symbol: 'ETH', name: 'Ethereum', price: 3150, change: -1.2, signal: 'hold', confidence: 72 },
    { symbol: 'ADA', name: 'Cardano', price: 0.45, change: 5.8, signal: 'buy', confidence: 91 },
    { symbol: 'SOL', name: 'Solana', price: 98.5, change: -0.8, signal: 'sell', confidence: 78 },
  ];

  const watchlist = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 185.20, change: 1.2 },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 245.80, change: -2.1 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <Button>
          <Brain className="mr-2 h-4 w-4" />
          {t('startAnalysis')}
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('opportunityRadar')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] flex items-center justify-center text-[hsl(var(--muted-foreground))]">
                AI Opportunity Radar Chart Placeholder
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('globalIndex')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <span className="font-medium">S&P 500:</span>
                  <span className="text-green-600">4,285.50 (+0.8%)</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium">NASDAQ:</span>
                  <span className="text-red-600">13,240.80 (-0.3%)</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-medium">DXY:</span>
                  <span className="text-green-600">104.25 (+0.2%)</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Market Analysis</CardTitle>
                <div className="flex gap-1">
                  {marketTabs.map((tab) => (
                    <Button key={tab} variant={tab === 'crypto' ? 'default' : 'outline'} size="sm">
                      {t(`marketTabs.${tab}` as keyof typeof t)}
                    </Button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {assets.map((asset) => (
                  <div key={asset.symbol} className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-[hsl(var(--muted))] rounded-full flex items-center justify-center">
                        <span className="text-sm font-bold">{asset.symbol.slice(0, 2)}</span>
                      </div>
                      <div>
                        <div className="font-medium">{asset.symbol}</div>
                        <div className="text-sm text-[hsl(var(--muted-foreground))]">{asset.name}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">${asset.price.toLocaleString()}</div>
                      <div className={`text-sm ${asset.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {asset.change >= 0 ? '+' : ''}{asset.change}%
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={asset.signal === 'buy' ? 'default' : asset.signal === 'sell' ? 'destructive' : 'secondary'}>
                        {t(asset.signal as keyof typeof t)}
                      </Badge>
                      <div className="text-sm text-[hsl(var(--muted-foreground))]">
                        {asset.confidence}%
                      </div>
                      <Button size="sm" variant="ghost">
                        <Star className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>{t('watchlist')}</CardTitle>
                <Button size="sm" variant="outline">
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {watchlist.map((item) => (
                <div key={item.symbol} className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">{item.symbol}</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">{item.name}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">${item.price}</div>
                    <div className={`text-sm ${item.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {item.change >= 0 ? <TrendingUp className="h-3 w-3 inline" /> : <TrendingDown className="h-3 w-3 inline" />}
                      {item.change >= 0 ? '+' : ''}{item.change}%
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Analysis Panel</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Button className="w-full">
                  <Brain className="mr-2 h-4 w-4" />
                  {t('startAnalysis')}
                </Button>
                <div className="p-4 bg-[hsl(var(--muted))] rounded-lg">
                  <div className="text-sm font-medium mb-2">Latest Analysis</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">
                    BTC shows strong bullish momentum with 85% confidence. Recommended entry around $45,000 with target at $52,000.
                  </div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))] mt-2">
                    2 hours ago
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}