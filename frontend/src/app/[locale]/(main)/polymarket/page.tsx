import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default async function PolymarketPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('polymarket');

  // Mock markets data – in production this is fetched from /api/polymarket/markets
  const mockMarkets = [
    {
      id: '1',
      question: 'Will Bitcoin reach $100,000 by end of 2025?',
      yesPrice: 0.62,
      noPrice: 0.38,
      volume: 1_250_000,
      liquidity: 85_000,
      endDate: '2025-12-31',
      tags: ['crypto', 'bitcoin'],
    },
    {
      id: '2',
      question: 'Will the Federal Reserve cut rates in Q2 2025?',
      yesPrice: 0.45,
      noPrice: 0.55,
      volume: 3_400_000,
      liquidity: 220_000,
      endDate: '2025-06-30',
      tags: ['macro', 'fed'],
    },
    {
      id: '3',
      question: 'Will Ethereum ETF inflows exceed $1B in April 2025?',
      yesPrice: 0.71,
      noPrice: 0.29,
      volume: 890_000,
      liquidity: 65_000,
      endDate: '2025-04-30',
      tags: ['crypto', 'ethereum', 'etf'],
    },
    {
      id: '4',
      question: 'Will S&P 500 close above 6000 in May 2025?',
      yesPrice: 0.53,
      noPrice: 0.47,
      volume: 2_100_000,
      liquidity: 150_000,
      endDate: '2025-05-31',
      tags: ['stocks', 'sp500'],
    },
    {
      id: '5',
      question: 'Will NVIDIA stock exceed $1000 in 2025?',
      yesPrice: 0.39,
      noPrice: 0.61,
      volume: 1_780_000,
      liquidity: 105_000,
      endDate: '2025-12-31',
      tags: ['stocks', 'ai', 'nvidia'],
    },
    {
      id: '6',
      question: 'Will Gold price exceed $3500 by Q3 2025?',
      yesPrice: 0.28,
      noPrice: 0.72,
      volume: 650_000,
      liquidity: 42_000,
      endDate: '2025-09-30',
      tags: ['commodities', 'gold'],
    },
  ];

  const formatCurrency = (value: number): string => {
    if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
    return `$${value}`;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <p className="text-muted-foreground mt-1">{t('subtitle')}</p>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">{t('trending')}</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {mockMarkets.map((market) => (
            <Card key={market.id} className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium leading-snug">
                  {market.question}
                </CardTitle>
                <div className="flex flex-wrap gap-1 mt-2">
                  {market.tags.map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Probability bar */}
                <div className="space-y-1">
                  <div className="flex justify-between text-sm font-medium">
                    <span className="text-green-600">
                      {t('yesOdds')} {(market.yesPrice * 100).toFixed(0)}%
                    </span>
                    <span className="text-red-600">
                      {t('noOdds')} {(market.noPrice * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-red-200 overflow-hidden">
                    <div
                      className="h-full bg-green-500 rounded-full transition-all"
                      style={{ width: `${market.yesPrice * 100}%` }}
                    />
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
                  <div>
                    <span className="font-medium">{t('volume')}:</span>{' '}
                    {formatCurrency(market.volume)}
                  </div>
                  <div>
                    <span className="font-medium">{t('liquidity')}:</span>{' '}
                    {formatCurrency(market.liquidity)}
                  </div>
                  <div className="col-span-2">
                    <span className="font-medium">{t('endDate')}:</span>{' '}
                    {market.endDate}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
