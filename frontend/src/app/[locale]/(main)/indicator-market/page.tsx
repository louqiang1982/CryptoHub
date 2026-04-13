import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Star, Download, TrendingUp, Filter } from 'lucide-react';

export default async function IndicatorMarketPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('indicatorMarket');

  const categories = ['popular', 'newest', 'free', 'premium'];
  
  const indicators = [
    {
      id: 1,
      name: 'Advanced RSI Pro',
      description: 'Enhanced RSI with multiple timeframe analysis and divergence detection',
      author: 'TradingPro',
      rating: 4.8,
      downloads: 15420,
      price: 29.99,
      isFree: false,
      isInstalled: false,
      category: 'momentum'
    },
    {
      id: 2,
      name: 'Volume Profile Master',
      description: 'Professional volume profile analysis with support/resistance levels',
      author: 'VolumeExpert',
      rating: 4.9,
      downloads: 8930,
      price: 0,
      isFree: true,
      isInstalled: true,
      category: 'volume'
    },
    {
      id: 3,
      name: 'Smart Bollinger Bands',
      description: 'AI-enhanced Bollinger Bands with dynamic adaptation',
      author: 'AITrading',
      rating: 4.7,
      downloads: 12350,
      price: 19.99,
      isFree: false,
      isInstalled: false,
      category: 'volatility'
    },
    {
      id: 4,
      name: 'Fibonacci Retracement+',
      description: 'Advanced Fibonacci tool with automatic level detection',
      author: 'FibonacciMaster',
      rating: 4.6,
      downloads: 7650,
      price: 15.99,
      isFree: false,
      isInstalled: false,
      category: 'fibonacci'
    },
    {
      id: 5,
      name: 'MACD Divergence Scanner',
      description: 'Automatic MACD divergence detection and alerts',
      author: 'DivergenceHunter',
      rating: 4.5,
      downloads: 9870,
      price: 0,
      isFree: true,
      isInstalled: false,
      category: 'momentum'
    },
    {
      id: 6,
      name: 'Support & Resistance Zones',
      description: 'Dynamic support and resistance level identification',
      author: 'ZoneAnalyst',
      rating: 4.8,
      downloads: 11250,
      price: 24.99,
      isFree: false,
      isInstalled: true,
      category: 'levels'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <Button variant="outline">
          <Filter className="mr-2 h-4 w-4" />
          Filter
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[hsl(var(--muted-foreground))]" />
              <Input placeholder={t('search')} className="pl-9" />
            </div>
            <div className="flex gap-2">
              {categories.map((category) => (
                <Button key={category} variant={category === 'popular' ? 'default' : 'outline'} size="sm">
                  {t(category as keyof typeof t)}
                </Button>
              ))}
            </div>
          </div>
        </CardHeader>
      </Card>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {indicators.map((indicator) => (
          <Card key={indicator.id} className="flex flex-col">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{indicator.name}</CardTitle>
                  <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
                    by {indicator.author}
                  </p>
                </div>
                <div className="flex items-center gap-1">
                  {indicator.isFree && (
                    <Badge variant="secondary">{t('free')}</Badge>
                  )}
                  {!indicator.isFree && (
                    <Badge variant="default">{t('premium')}</Badge>
                  )}
                </div>
              </div>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                {indicator.description}
              </p>
            </CardHeader>
            <CardContent className="flex-1 space-y-4">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-1">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="font-medium">{indicator.rating}</span>
                </div>
                <div className="flex items-center gap-1 text-[hsl(var(--muted-foreground))]">
                  <Download className="h-4 w-4" />
                  <span>{indicator.downloads.toLocaleString()}</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="text-lg font-bold">
                  {indicator.isFree ? t('free') : `$${indicator.price}`}
                </div>
                <div className="flex gap-2">
                  {indicator.isInstalled ? (
                    <Badge variant="outline" className="text-green-600 border-green-600">
                      {t('installed')}
                    </Badge>
                  ) : (
                    <Button size="sm">
                      {indicator.isFree ? t('install') : `$${indicator.price}`}
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex justify-center">
        <Button variant="outline">
          Load More Indicators
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Featured Authors</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {['TradingPro', 'VolumeExpert', 'AITrading'].map((author) => (
              <div key={author} className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-[hsl(var(--muted))] rounded-full flex items-center justify-center">
                    <span className="text-sm font-bold">{author[0]}</span>
                  </div>
                  <div>
                    <div className="font-medium">{author}</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">Verified Developer</div>
                  </div>
                </div>
                <Button size="sm" variant="outline">Follow</Button>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Trending Categories</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { name: 'AI & Machine Learning', count: 42 },
              { name: 'Volume Analysis', count: 38 },
              { name: 'Pattern Recognition', count: 31 },
              { name: 'Risk Management', count: 24 }
            ].map((category) => (
              <div key={category.name} className="flex items-center justify-between p-2 border border-[hsl(var(--border))] rounded">
                <div>
                  <div className="font-medium">{category.name}</div>
                  <div className="text-sm text-[hsl(var(--muted-foreground))]">{category.count} indicators</div>
                </div>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}