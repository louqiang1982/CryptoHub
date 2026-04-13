import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  User, Key, Bell, Shield, Plus, Edit,
  Trash2, Eye, Settings
} from 'lucide-react';

export default async function ProfilePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('profile');

  const apiKeys = [
    {
      id: 1,
      name: 'Binance Main',
      exchange: 'Binance',
      permissions: ['read', 'trade'],
      created: '2024-01-15',
      lastUsed: '2 hours ago',
      status: 'active'
    },
    {
      id: 2,
      name: 'Coinbase Pro',
      exchange: 'Coinbase',
      permissions: ['read'],
      created: '2024-01-10',
      lastUsed: '1 day ago',
      status: 'active'
    },
    {
      id: 3,
      name: 'Kraken Trading',
      exchange: 'Kraken',
      permissions: ['read', 'trade', 'withdraw'],
      created: '2024-01-05',
      lastUsed: 'Never',
      status: 'inactive'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <Button variant="outline">
          <Settings className="mr-2 h-4 w-4" />
          Account Settings
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                {t('personalInfo')}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="text-sm font-medium">{t('username')}</label>
                  <Input defaultValue="cryptotrader_pro" />
                </div>
                <div>
                  <label className="text-sm font-medium">{t('email')}</label>
                  <Input defaultValue="trader@example.com" />
                </div>
                <div>
                  <label className="text-sm font-medium">First Name</label>
                  <Input defaultValue="John" />
                </div>
                <div>
                  <label className="text-sm font-medium">Last Name</label>
                  <Input defaultValue="Doe" />
                </div>
                <div>
                  <label className="text-sm font-medium">Phone Number</label>
                  <Input defaultValue="+1 (555) 123-4567" />
                </div>
                <div>
                  <label className="text-sm font-medium">Country</label>
                  <Input defaultValue="United States" />
                </div>
              </div>
              <div className="flex gap-2">
                <Button>Save Changes</Button>
                <Button variant="outline">Cancel</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Key className="h-5 w-5" />
                  {t('apiKeys')}
                </CardTitle>
                <Button size="sm">
                  <Plus className="mr-2 h-4 w-4" />
                  {t('addApiKey')}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {apiKeys.map((apiKey) => (
                  <div key={apiKey.id} className="p-4 border border-[hsl(var(--border))] rounded-lg">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-medium">{apiKey.name}</h3>
                          <Badge variant={apiKey.status === 'active' ? 'default' : 'secondary'}>
                            {apiKey.status}
                          </Badge>
                        </div>
                        <div className="text-sm text-[hsl(var(--muted-foreground))] space-y-1">
                          <div>Exchange: {apiKey.exchange}</div>
                          <div>Permissions: {apiKey.permissions.join(', ')}</div>
                          <div>Created: {apiKey.created}</div>
                          <div>Last used: {apiKey.lastUsed}</div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="destructive">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                {t('notifications')}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                {[
                  { id: 'email_alerts', label: 'Email Alerts', description: 'Receive trading alerts via email' },
                  { id: 'sms_alerts', label: 'SMS Alerts', description: 'Receive urgent alerts via SMS' },
                  { id: 'push_notifications', label: 'Push Notifications', description: 'Browser notifications for trades' },
                  { id: 'price_alerts', label: 'Price Alerts', description: 'Notifications when prices reach targets' },
                  { id: 'strategy_alerts', label: 'Strategy Alerts', description: 'Alerts for strategy status changes' },
                  { id: 'system_updates', label: 'System Updates', description: 'Platform updates and maintenance' }
                ].map((notification) => (
                  <div key={notification.id} className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                    <div>
                      <div className="font-medium">{notification.label}</div>
                      <div className="text-sm text-[hsl(var(--muted-foreground))]">{notification.description}</div>
                    </div>
                    <div className="flex items-center">
                      <input type="checkbox" defaultChecked className="mr-2" />
                    </div>
                  </div>
                ))}
              </div>
              <Button>Save Notification Settings</Button>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                {t('security')}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">{t('changePassword')}</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">Last changed 30 days ago</div>
                  </div>
                  <Button size="sm" variant="outline">Change</Button>
                </div>

                <div className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">{t('twoFactor')}</div>
                    <div className="text-sm text-green-600">Enabled</div>
                  </div>
                  <Button size="sm" variant="outline">Manage</Button>
                </div>

                <div className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">Login Sessions</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">3 active sessions</div>
                  </div>
                  <Button size="sm" variant="outline">View</Button>
                </div>

                <div className="flex items-center justify-between p-3 border border-[hsl(var(--border))] rounded">
                  <div>
                    <div className="font-medium">Device Management</div>
                    <div className="text-sm text-[hsl(var(--muted-foreground))]">Manage trusted devices</div>
                  </div>
                  <Button size="sm" variant="outline">Manage</Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Account Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between text-sm">
                <span>Member Since:</span>
                <span className="font-medium">January 2024</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Account Type:</span>
                <span className="font-medium">Professional</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Verification Level:</span>
                <span className="font-medium text-green-600">Verified</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>API Keys:</span>
                <span className="font-medium">{apiKeys.length}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Trading Volume (30d):</span>
                <span className="font-medium">$125,430</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button className="w-full" variant="outline">
                Download Account Data
              </Button>
              <Button className="w-full" variant="outline">
                Export Trading History
              </Button>
              <Button className="w-full" variant="outline">
                Contact Support
              </Button>
              <Button className="w-full" variant="destructive">
                Delete Account
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}