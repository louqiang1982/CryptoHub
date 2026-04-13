'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface QuickTradePanelProps {
  symbol?: string;
  price?: number;
}

export default function QuickTradePanel({ symbol = 'BTC/USDT', price = 45230.50 }: QuickTradePanelProps) {
  const [side, setSide] = useState<'buy' | 'sell'>('buy');
  const [orderType, setOrderType] = useState<'market' | 'limit'>('market');
  const [amount, setAmount] = useState('');
  const [limitPrice, setLimitPrice] = useState('');

  const percentages = [25, 50, 75, 100];

  const estimatedTotal = (() => {
    const qty = parseFloat(amount) || 0;
    const p = orderType === 'limit' ? (parseFloat(limitPrice) || price) : price;
    return (qty * p).toFixed(2);
  })();

  return (
    <div className="space-y-4">
      {/* Side toggle */}
      <div className="grid grid-cols-2 gap-2">
        <Button
          variant={side === 'buy' ? 'default' : 'outline'}
          className={side === 'buy' ? 'bg-green-600 hover:bg-green-700 text-white' : ''}
          onClick={() => setSide('buy')}
        >
          <ArrowUpRight className="h-4 w-4 mr-1" />
          Buy
        </Button>
        <Button
          variant={side === 'sell' ? 'default' : 'outline'}
          className={side === 'sell' ? 'bg-red-600 hover:bg-red-700 text-white' : ''}
          onClick={() => setSide('sell')}
        >
          <ArrowDownRight className="h-4 w-4 mr-1" />
          Sell
        </Button>
      </div>

      {/* Order type */}
      <div className="flex gap-2">
        <Button
          variant={orderType === 'market' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setOrderType('market')}
        >
          Market
        </Button>
        <Button
          variant={orderType === 'limit' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setOrderType('limit')}
        >
          Limit
        </Button>
      </div>

      {/* Price display or input */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">Price</span>
          <Badge variant="outline">{symbol}</Badge>
        </div>
        {orderType === 'market' ? (
          <div className="flex items-center h-9 px-3 rounded-md border border-[hsl(var(--input))] bg-[hsl(var(--muted))] text-sm">
            <span className="text-muted-foreground mr-1">≈</span>
            <span className="font-medium">${price.toLocaleString()}</span>
          </div>
        ) : (
          <Input
            type="number"
            placeholder="Limit price"
            value={limitPrice}
            onChange={(e) => setLimitPrice(e.target.value)}
          />
        )}
      </div>

      {/* Amount */}
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground">Amount</label>
        <Input
          type="number"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          step="0.001"
          min="0"
        />
        <div className="flex gap-1">
          {percentages.map((pct) => (
            <Button
              key={pct}
              variant="outline"
              size="sm"
              className="flex-1 text-xs"
              onClick={() => setAmount((10000 / price * pct / 100).toFixed(6))}
            >
              {pct}%
            </Button>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="space-y-1 text-sm">
        <div className="flex justify-between">
          <span className="text-muted-foreground">Total</span>
          <span className="font-medium">${estimatedTotal}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted-foreground">Fee (est.)</span>
          <span className="font-medium">${(parseFloat(estimatedTotal) * 0.001).toFixed(2)}</span>
        </div>
      </div>

      {/* Submit */}
      <Button
        className={`w-full ${
          side === 'buy'
            ? 'bg-green-600 hover:bg-green-700 text-white'
            : 'bg-red-600 hover:bg-red-700 text-white'
        }`}
        disabled={!amount || parseFloat(amount) <= 0}
      >
        {side === 'buy' ? 'Buy' : 'Sell'} {symbol.split('/')[0]}
      </Button>
    </div>
  );
}
