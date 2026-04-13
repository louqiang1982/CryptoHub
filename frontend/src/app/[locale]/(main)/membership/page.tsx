import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Crown, CheckCircle, Star, Zap, Shield, 
  CreditCard, Receipt, Gift
} from 'lucide-react';

export default async function MembershipPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('membership');

  const plans = [
    {
      name: 'free',
      displayName: 'Free Trader',
      price: 0,
      period: 'forever',
      current: false,
      features: [
        '3 Trading Strategies',
        'Basic AI Analysis',
        'Standard Indicators',
        'Email Support',
        'Mobile App Access'
      ],
      limits: {
        strategies: 3,
        indicators: 10,
        apiCalls: 1000,
        support: 'Email'
      }
    },
    {
      name: 'pro',
      displayName: 'Professional',
      price: 29.99,
      period: 'month',
      current: true,
      popular: true,
      features: [
        'Unlimited Strategies',
        'Advanced AI Analysis',
        'Premium Indicators',
        'Priority Support',
        'Advanced Analytics',
        'Portfolio Management',
        'Risk Management Tools'
      ],
      limits: {
        strategies: 'Unlimited',
        indicators: 100,
        apiCalls: 50000,
        support: 'Priority'
      }
    },
    {
      name: 'enterprise',
      displayName: 'Enterprise',
      price: 99.99,
      period: 'month',
      current: false,
      features: [
        'Everything in Pro',
        'Custom Indicators',
        'White-label Solutions',
        'Dedicated Support',
        'Advanced API Access',
        'Multi-user Management',
        'Custom Integrations',
        'SLA Guarantee'
      ],
      limits: {
        strategies: 'Unlimited',
        indicators: 'Unlimited',
        apiCalls: 'Unlimited',
        support: 'Dedicated'
      }
    }
  ];

  const billingHistory = [
    {
      id: 1,
      date: '2024-01-15',
      description: 'Professional Plan - Monthly',
      amount: 29.99,
      status: 'paid',
      invoice: 'INV-001234'
    },
    {
      id: 2,
      date: '2023-12-15',
      description: 'Professional Plan - Monthly',
      amount: 29.99,
      status: 'paid',
      invoice: 'INV-001233'
    },
    {
      id: 3,
      date: '2023-11-15',
      description: 'Professional Plan - Monthly',
      amount: 29.99,
      status: 'paid',
      invoice: 'INV-001232'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">{t('billing')}</Button>
          <Button variant="outline">{t('credits')}</Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>{t('currentPlan')}</CardTitle>
            <Badge className="bg-green-100 text-green-800">
              <Crown className="mr-1 h-3 w-3" />
              Professional
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Next billing date: February 15, 2024
              </p>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                $29.99/month • Auto-renewal enabled
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline">Manage Plan</Button>
              <Button>Upgrade</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-3">
        {plans.map((plan) => (
          <Card key={plan.name} className={`relative ${plan.current ? 'border-[hsl(var(--primary))] shadow-lg' : ''}`}>
            {plan.popular && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <Badge className="bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]">
                  Most Popular
                </Badge>
              </div>
            )}
            <CardHeader className="text-center">
              <div className="flex justify-center mb-2">
                {plan.name === 'free' && <Gift className="h-8 w-8 text-[hsl(var(--muted-foreground))]" />}
                {plan.name === 'pro' && <Star className="h-8 w-8 text-[hsl(var(--primary))]" />}
                {plan.name === 'enterprise' && <Crown className="h-8 w-8 text-yellow-500" />}
              </div>
              <CardTitle className="text-xl">{plan.displayName}</CardTitle>
              <div className="text-3xl font-bold">
                ${plan.price}
                <span className="text-lg font-normal text-[hsl(var(--muted-foreground))]">
                  /{plan.period}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                {plan.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
              
              <div className="pt-4 border-t space-y-2">
                <div className="text-sm font-medium">Plan Limits:</div>
                <div className="space-y-1 text-sm text-[hsl(var(--muted-foreground))]">
                  <div>Strategies: {plan.limits.strategies}</div>
                  <div>Indicators: {plan.limits.indicators}</div>
                  <div>API Calls: {plan.limits.apiCalls}</div>
                  <div>Support: {plan.limits.support}</div>
                </div>
              </div>

              <Button 
                className="w-full" 
                variant={plan.current ? 'outline' : 'default'}
                disabled={plan.current}
              >
                {plan.current ? 'Current Plan' : plan.price === 0 ? 'Downgrade' : 'Upgrade'}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Receipt className="h-5 w-5" />
              {t('billing')} History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {billingHistory.map((bill) => (
                <div key={bill.id} className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">{bill.description}</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">
                      {bill.date} • {bill.invoice}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">${bill.amount}</div>
                    <Badge variant="secondary">Paid</Badge>
                  </div>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              View All Invoices
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CreditCard className="h-5 w-5" />
              Payment Method
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 border border-[hsl(var(--border))] rounded">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-6 bg-gradient-to-r from-blue-600 to-blue-400 rounded text-white text-xs flex items-center justify-center font-bold">
                    VISA
                  </div>
                  <div>
                    <div className="font-medium">•••• •••• •••• 4242</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">Expires 12/25</div>
                  </div>
                </div>
                <Button size="sm" variant="outline">Edit</Button>
              </div>
            </div>
            <Button className="w-full" variant="outline">
              Add Payment Method
            </Button>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-green-600" />
                <span className="text-sm">Payments secured by Stripe</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-green-600" />
                <span className="text-sm">Cancel anytime</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Usage Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-[hsl(var(--primary))]">8</div>
              <div className="text-sm text-[hsl(var(--muted-foreground))]">Active Strategies</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-[hsl(var(--primary))]">42</div>
              <div className="text-sm text-[hsl(var(--muted-foreground))]">Indicators Used</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-[hsl(var(--primary))]">15.2K</div>
              <div className="text-sm text-[hsl(var(--muted-foreground))]">API Calls (30d)</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-[hsl(var(--primary))]">98.5%</div>
              <div className="text-sm text-[hsl(var(--muted-foreground))]">Uptime</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}