import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Link } from '@/i18n/navigation';
import { UserPlus, Github, Mail, CheckCircle } from 'lucide-react';

export default async function RegisterPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('auth');
  const tCommon = await getTranslations('common');

  return (
    <Card className="w-full">
      <CardHeader className="space-y-1 text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="w-12 h-12 bg-[hsl(var(--primary))] rounded-lg flex items-center justify-center">
            <span className="text-xl font-bold text-[hsl(var(--primary-foreground))]">C</span>
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">{t('register')}</CardTitle>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">
          Create your account to start trading with AI
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label htmlFor="firstName" className="text-sm font-medium">
              First Name
            </label>
            <Input
              id="firstName"
              type="text"
              placeholder="John"
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="lastName" className="text-sm font-medium">
              Last Name
            </label>
            <Input
              id="lastName"
              type="text"
              placeholder="Doe"
              required
            />
          </div>
        </div>
        
        <div className="space-y-2">
          <label htmlFor="email" className="text-sm font-medium">
            {t('email')}
          </label>
          <Input
            id="email"
            type="email"
            placeholder="trader@example.com"
            required
          />
        </div>
        
        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium">
            {t('password')}
          </label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            required
          />
          <div className="text-xs text-[hsl(var(--muted-foreground))]">
            Must be at least 8 characters with numbers and symbols
          </div>
        </div>
        
        <div className="space-y-2">
          <label htmlFor="confirmPassword" className="text-sm font-medium">
            {t('confirmPassword')}
          </label>
          <Input
            id="confirmPassword"
            type="password"
            placeholder="••••••••"
            required
          />
        </div>

        <div className="space-y-3">
          <div className="flex items-start space-x-2">
            <input
              type="checkbox"
              id="terms"
              className="mt-1 rounded border-gray-300"
              required
            />
            <label htmlFor="terms" className="text-sm">
              {t('termsAgree')} and Privacy Policy
            </label>
          </div>
          
          <div className="flex items-start space-x-2">
            <input
              type="checkbox"
              id="marketing"
              className="mt-1 rounded border-gray-300"
            />
            <label htmlFor="marketing" className="text-sm">
              I want to receive marketing emails about new features and updates
            </label>
          </div>
        </div>
        
        <Button type="submit" className="w-full">
          <UserPlus className="mr-2 h-4 w-4" />
          {tCommon('create')} Account
        </Button>
        
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-[hsl(var(--background))] px-2 text-[hsl(var(--muted-foreground))]">
              Or continue with
            </span>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <Button variant="outline" type="button">
            <Github className="mr-2 h-4 w-4" />
            GitHub
          </Button>
          <Button variant="outline" type="button">
            <Mail className="mr-2 h-4 w-4" />
            Google
          </Button>
        </div>
        
        <div className="text-center text-sm">
          <span className="text-[hsl(var(--muted-foreground))]">
            {t('hasAccount')}{' '}
          </span>
          <Link
            href="/login"
            className="text-[hsl(var(--primary))] hover:underline"
          >
            {t('login')}
          </Link>
        </div>

        <div className="mt-6 p-4 bg-[hsl(var(--muted))] rounded-lg">
          <div className="text-sm font-medium mb-2 flex items-center gap-2">
            <CheckCircle className="h-4 w-4 text-green-600" />
            What you get with CryptoHub:
          </div>
          <ul className="text-xs text-[hsl(var(--muted-foreground))] space-y-1">
            <li>• Advanced AI-powered trading strategies</li>
            <li>• Real-time market analysis and insights</li>
            <li>• Professional-grade risk management tools</li>
            <li>• 24/7 customer support</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}