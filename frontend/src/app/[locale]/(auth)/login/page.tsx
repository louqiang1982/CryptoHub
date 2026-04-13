import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Link } from '@/i18n/navigation';
import { LogIn, Github, Mail } from 'lucide-react';

export default async function LoginPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('auth');

  return (
    <Card className="w-full">
      <CardHeader className="space-y-1 text-center">
        <div className="flex items-center justify-center mb-4">
          <div className="w-12 h-12 bg-[hsl(var(--primary))] rounded-lg flex items-center justify-center">
            <span className="text-xl font-bold text-[hsl(var(--primary-foreground))]">C</span>
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">{t('login')}</CardTitle>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">
          Sign in to access your trading dashboard
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
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
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="remember"
              className="rounded border-gray-300"
            />
            <label htmlFor="remember" className="text-sm">
              {t('rememberMe')}
            </label>
          </div>
          <Link
            href="/forgot-password"
            className="text-sm text-[hsl(var(--primary))] hover:underline"
          >
            {t('forgotPassword')}
          </Link>
        </div>
        <Button type="submit" className="w-full">
          <LogIn className="mr-2 h-4 w-4" />
          {t('login')}
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
            {t('noAccount')}{' '}
          </span>
          <Link
            href="/register"
            className="text-[hsl(var(--primary))] hover:underline"
          >
            {t('register')}
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}