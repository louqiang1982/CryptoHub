import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Plus, Play, Pause, Square, Copy, BarChart3,
  Settings, Filter, Bot, TrendingUp, TrendingDown 
} from 'lucide-react';

export default async function TradingPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('trading');

  const strategies = [
    {
      id: 1,
      name: 'BTC Momentum Strategy',
      symbol: 'BTC/USDT',
      status: 'running',
      pnl: 2450.30,
      winRate: 68.5,
      trades: 24,
      description: 'RSI + MACD momentum strategy with dynamic position sizing'
    },
    {
      id: 2,
      name: 'ETH Grid Trading',
      symbol: 'ETH/USDT',
      status: 'paused',
      pnl: -125.80,
      winRate: 45.2,
      trades: 12,
      description: 'Grid trading with 0.5% intervals and automatic rebalancing'
    },
    {
      id: 3,
      name: 'Multi-Pair Arbitrage',
      symbol: 'Multiple',
      status: 'running',
      pnl: 1890.45,
      winRate: 82.3,
      trades: 156,
      description: 'Cross-exchange arbitrage opportunities across major pairs'
    },
    {
      id: 4,
      name: 'DCA Bitcoin',
      symbol: 'BTC/USDT',
      status: 'stopped',
      pnl: 567.20,
      winRate: 100,
      trades: 8,
      description: 'Dollar cost averaging with weekly purchases'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter className="mr-2 h-4 w-4" />
            Filter
          </Button>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            {t('createStrategy')}
          </Button>
        </div>
      </div>

      <div className="flex gap-4">
        <Card className="flex-1">
          <CardHeader>
            <CardTitle className="text-lg">{t('groupBy.strategy')}</CardTitle>
          </CardHeader>
        </Card>
        <Card className="flex-1">
          <CardHeader>
            <CardTitle className="text-lg">{t('groupBy.symbol')}</CardTitle>
          </CardHeader>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t('strategyList')}</CardTitle>
            </CardHeader>
            <CardContent>
              {strategies.length > 0 ? (
                <div className="space-y-4">
                  {strategies.map((strategy) => (
                    <div key={strategy.id} className="p-4 border border-[hsl(var(--border))] rounded-lg space-y-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-semibold">{strategy.name}</h3>
                          <p className="text-sm text-[hsl(var(--muted-foreground))]">{strategy.symbol}</p>
                        </div>
                        <Badge variant={
                          strategy.status === 'running' ? 'default' :
                          strategy.status === 'paused' ? 'secondary' : 'outline'
                        }>
                          {t(`status.${strategy.status}` as keyof typeof t)}
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-[hsl(var(--muted-foreground))]">
                        {strategy.description}
                      </p>
                      
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <div className="text-[hsl(var(--muted-foreground))]">P&L</div>
                          <div className={`font-medium ${strategy.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {strategy.pnl >= 0 ? '+' : ''}${strategy.pnl.toFixed(2)}
                          </div>
                        </div>
                        <div>
                          <div className="text-[hsl(var(--muted-foreground))]">Win Rate</div>
                          <div className="font-medium">{strategy.winRate}%</div>
                        </div>
                        <div>
                          <div className="text-[hsl(var(--muted-foreground))]">Trades</div>
                          <div className="font-medium">{strategy.trades}</div>
                        </div>
                      </div>
                      
                      <div className="flex gap-2">
                        {strategy.status === 'running' && (
                          <Button size="sm" variant="outline">
                            <Pause className="h-4 w-4" />
                          </Button>
                        )}
                        {strategy.status === 'paused' && (
                          <Button size="sm" variant="outline">
                            <Play className="h-4 w-4" />
                          </Button>
                        )}
                        {strategy.status === 'stopped' && (
                          <Button size="sm" variant="outline">
                            <Play className="h-4 w-4" />
                          </Button>
                        )}
                        <Button size="sm" variant="outline">
                          <Square className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <BarChart3 className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Copy className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Settings className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Bot className="h-16 w-16 mx-auto mb-4 opacity-50" />
                  <p className="text-[hsl(var(--muted-foreground))] mb-4">{t('emptyState')}</p>
                  <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    {t('createStrategy')}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t('strategyDetail')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold mb-2">BTC Momentum Strategy</h3>
                  <p className="text-sm text-[hsl(var(--muted-foreground))] mb-4">
                    Advanced momentum trading strategy combining RSI and MACD indicators with dynamic position sizing.
                  </p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-[hsl(var(--muted-foreground))]">Symbol</div>
                      <div className="font-medium">BTC/USDT</div>
                    </div>
                    <div>
                      <div className="text-[hsl(var(--muted-foreground))]">Timeframe</div>
                      <div className="font-medium">1H</div>
                    </div>
                    <div>
                      <div className="text-[hsl(var(--muted-foreground))]">Capital</div>
                      <div className="font-medium">$10,000</div>
                    </div>
                    <div>
                      <div className="text-[hsl(var(--muted-foreground))]">Risk</div>
                      <div className="font-medium">2% per trade</div>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">Performance Chart</h4>
                  <div className="h-[200px] flex items-center justify-center border border-[hsl(var(--border))] rounded-lg text-[hsl(var(--muted-foreground))]">
                    Performance Chart Placeholder
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">Recent Trades</h4>
                  <div className="space-y-2">
                    {[
                      { side: 'buy', price: 45230, quantity: 0.021, pnl: 145.30, time: '2h ago' },
                      { side: 'sell', price: 44890, quantity: 0.018, pnl: -23.50, time: '4h ago' },
                      { side: 'buy', price: 44560, quantity: 0.025, pnl: 89.20, time: '6h ago' }
                    ].map((trade, index) => (
                      <div key={index} className="flex items-center justify-between p-2 text-sm border border-[hsl(var(--border))] rounded">
                        <div className="flex items-center gap-2">
                          {trade.side === 'buy' ? 
                            <TrendingUp className="h-4 w-4 text-green-600" /> :
                            <TrendingDown className="h-4 w-4 text-red-600" />
                          }
                          <span className="capitalize">{trade.side}</span>
                          <span>{trade.quantity} BTC</span>
                        </div>
                        <div className="text-right">
                          <div>${trade.price.toLocaleString()}</div>
                          <div className={`text-xs ${trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                          </div>
                        </div>
                        <div className="text-[hsl(var(--muted-foreground))] text-xs">
                          {trade.time}
                        </div>
                      </div>
                    ))}
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