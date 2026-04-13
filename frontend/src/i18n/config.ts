export const locales = ['en', 'zh-CN', 'zh-TW', 'ja', 'ko', 'ar', 'ru', 'de'] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = 'en';

export const localeNames: Record<Locale, string> = {
  en: 'English',
  'zh-CN': '简体中文',
  'zh-TW': '繁體中文',
  ja: '日本語',
  ko: '한국어',
  ar: 'العربية',
  ru: 'Русский',
  de: 'Deutsch',
};

export const rtlLocales: Locale[] = ['ar'];

export function isRtlLocale(locale: Locale): boolean {
  return rtlLocales.includes(locale);
}