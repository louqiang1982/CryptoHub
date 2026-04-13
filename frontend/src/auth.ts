import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';

const GO_API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080';

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        try {
          const res = await fetch(`${GO_API_BASE}/api/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (!res.ok) return null;

          const data = await res.json();
          if (data.code !== 0 || !data.data) return null;

          return {
            id: data.data.user_id ?? (credentials.email as string),
            email: credentials.email as string,
            accessToken: data.data.access_token,
            refreshToken: data.data.refresh_token,
          };
        } catch {
          return null;
        }
      },
    }),
    GitHub({
      clientId: process.env.GITHUB_ID ?? '',
      clientSecret: process.env.GITHUB_SECRET ?? '',
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID ?? '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? '',
    }),
  ],
  pages: {
    signIn: '/login',
  },
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.accessToken = (user as Record<string, unknown>).accessToken as string | undefined;
        token.refreshToken = (user as Record<string, unknown>).refreshToken as string | undefined;
      }
      if (account?.provider === 'github' || account?.provider === 'google') {
        try {
          const res = await fetch(`${GO_API_BASE}/api/v1/auth/oauth`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              provider: account.provider,
              provider_id: account.providerAccountId,
              email: token.email,
              name: token.name,
              avatar: token.picture,
            }),
          });
          if (res.ok) {
            const data = await res.json();
            if (data.code === 0 && data.data) {
              token.accessToken = data.data.access_token;
              token.refreshToken = data.data.refresh_token;
            }
          }
        } catch {
          // OAuth backend sync failed, continue with session-only auth
        }
      }
      return token;
    },
    async session({ session, token }) {
      if (token.accessToken) {
        (session as unknown as Record<string, unknown>).accessToken = token.accessToken;
      }
      return session;
    },
  },
});
