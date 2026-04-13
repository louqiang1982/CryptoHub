import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Wallet, TrendingUp, TrendingDown, DollarSign,
  PieChart, BarChart3, History
} from 'lucide-react';

export default async function PortfolioPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('portfolio');

  const positions = [
    {
      asset: 'BTC',
      name: 'Bitcoin',
      quantity: 2.15,
      avgPrice: 42500,
      currentPrice: 45230,
      value: 97244.50,
      pnl: 5869.50,
      pnlPercent: 6.43
    },
    {
      asset: 'ETH',
      name: 'Ethereum',
      quantity: 18.5,
      avgPrice: 2890,
      currentPrice: 3150,
      value: 58275,
      pnl: 4810,
      pnlPercent: 9.00
    },
    {
      asset: 'ADA',
      name: 'Cardano',
      quantity: 12500,
      avgPrice: 0.42,
      currentPrice: 0.45,
      value: 5625,
      pnl: 375,
      pnlPercent: 7.14
    },
    {
      asset: 'SOL',
      name: 'Solana',
      quantity: 145,
      avgPrice: 102.30,
      currentPrice: 98.50,
      value: 14282.50,
      pnl: -551,
      pnlPercent: -3.71
    }
  ];

  const tradeHistory = [
    {
      id: 1,
      type: 'buy',
      asset: 'BTC',
      quantity: 0.5,
      price: 44800,
      value: 22400,
      time: '2024-01-15 14:30',
      status: 'completed'
    },
    {
      id: 2,
      type: 'sell',
      asset: 'ETH',
      quantity: 2.0,
      price: 3200,
      value: 6400,
      time: '2024-01-15 12:15',
      status: 'completed'
    },
    {
      id: 3,
      type: 'buy',
      asset: 'ADA',
      quantity: 2500,
      price: 0.44,
      value: 1100,
      time: '2024-01-15 10:45',
      status: 'completed'
    },
    {
      id: 4,
      type: 'sell',
      asset: 'SOL',
      quantity: 25,
      price: 99.20,
      value: 2480,
      time: '2024-01-14 16:20',
      status: 'completed'
    }
  ];

  const totalValue = positions.reduce((sum, pos) => sum + pos.value, 0);
  const totalPnl = positions.reduce((sum, pos) => sum + pos.pnl, 0);
  const unrealizedPnl = totalPnl;
  const realizedPnl = 2450.30;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">{t('overview')}</Button>
          <Button variant="outline">{t('positions')}</Button>
          <Button variant="default">{t('history')}</Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t('totalValue')}</CardTitle>
            <DollarSign className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalValue.toLocaleString()}</div>
            <p className="text-xs text-[hsl(var(--muted-foreground))]">
              Portfolio balance
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t('unrealizedPnl')}</CardTitle>
            <TrendingUp className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${unrealizedPnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {unrealizedPnl >= 0 ? '+' : ''}${unrealizedPnl.toLocaleString()}
            </div>
            <p className="text-xs text-[hsl(var(--muted-foreground))]">
              Open positions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t('realizedPnl')}</CardTitle>
            <BarChart3 className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${realizedPnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              +${realizedPnl.toLocaleString()}
            </div>
            <p className="text-xs text-[hsl(var(--muted-foreground))]">
              Closed positions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">24h Change</CardTitle>
            <PieChart className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+3.24%</div>
            <p className="text-xs text-[hsl(var(--muted-foreground))]">
              Daily performance
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('positions')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-8 gap-2 text-sm font-medium text-[hsl(var(--muted-foreground))] pb-2 border-b">
                  <div>{t('asset')}</div>
                  <div>{t('quantity')}</div>
                  <div>{t('avgPrice')}</div>
                  <div>{t('currentPrice')}</div>
                  <div>Value</div>
                  <div>24h</div>
                  <div>{t('pnl')}</div>
                  <div>%</div>
                </div>
                {positions.map((position) => (
                  <div key={position.asset} className="grid grid-cols-8 gap-2 text-sm items-center">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-[hsl(var(--muted))] rounded-full flex items-center justify-center">
                        <span className="text-xs font-bold">{position.asset}</span>
                      </div>
                      <div>
                        <div className="font-medium">{position.asset}</div>
                        <div className="text-xs text-[hsl(var(--muted-foreground))]">{position.name}</div>
                      </div>
                    </div>
                    <div>{position.quantity}</div>
                    <div>${position.avgPrice.toLocaleString()}</div>
                    <div>${position.currentPrice.toLocaleString()}</div>
                    <div className="font-medium">${position.value.toLocaleString()}</div>
                    <div className={position.pnl >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {position.pnl >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                    </div>
                    <div className={`font-medium ${position.pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {position.pnl >= 0 ? '+' : ''}${position.pnl.toFixed(2)}
                    </div>
                    <div className={position.pnlPercent >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {position.pnlPercent >= 0 ? '+' : ''}{position.pnlPercent.toFixed(2)}%
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t('history')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="grid grid-cols-6 gap-2 text-sm font-medium text-[hsl(var(--muted-foreground))] pb-2 border-b">
                  <div>Type</div>
                  <div>Asset</div>
                  <div>Quantity</div>
                  <div>Price</div>
                  <div>Value</div>
                  <div>Time</div>
                </div>
                {tradeHistory.map((trade) => (
                  <div key={trade.id} className="grid grid-cols-6 gap-2 text-sm items-center">
                    <div className="flex items-center gap-2">
                      <Badge variant={trade.type === 'buy' ? 'default' : 'secondary'}>
                        {trade.type.toUpperCase()}
                      </Badge>
                    </div>
                    <div className="font-medium">{trade.asset}</div>
                    <div>{trade.quantity}</div>
                    <div>${trade.price.toLocaleString()}</div>
                    <div className="font-medium">${trade.value.toLocaleString()}</div>
                    <div className="text-xs text-[hsl(var(--muted-foreground))]">{trade.time}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Portfolio Allocation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[200px] flex items-center justify-center border border-[hsl(var(--border))] rounded-lg text-[hsl(var(--muted-foreground))]">
                Pie Chart Placeholder
              </div>
              <div className="mt-4 space-y-2">
                {positions.map((position) => {
                  const percentage = ((position.value / totalValue) * 100).toFixed(1);
                  return (
                    <div key={position.asset} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-[hsl(var(--primary))] rounded-full"></div>
                        <span>{position.asset}</span>
                      </div>
                      <span className="font-medium">{percentage}%</span>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[200px] flex items-center justify-center border border-[hsl(var(--border))] rounded-lg text-[hsl(var(--muted-foreground))]">
                Performance Chart Placeholder
              </div>
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>1D:</span>
                  <span className="text-green-600">+3.24%</span>
                </div>
                <div className="flex justify-between">
                  <span>1W:</span>
                  <span className="text-green-600">+8.91%</span>
                </div>
                <div className="flex justify-between">
                  <span>1M:</span>
                  <span className="text-green-600">+15.67%</span>
                </div>
                <div className="flex justify-between">
                  <span>3M:</span>
                  <span className="text-red-600">-2.45%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button className="w-full" variant="outline">
                <Wallet className="mr-2 h-4 w-4" />
                Deposit Funds
              </Button>
              <Button className="w-full" variant="outline">
                <TrendingUp className="mr-2 h-4 w-4" />
                Buy Crypto
              </Button>
              <Button className="w-full" variant="outline">
                <History className="mr-2 h-4 w-4" />
                Export History
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}