import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Users, UserCheck, Settings, Activity,
  Shield, Database, BarChart3, AlertCircle
} from 'lucide-react';

export default async function AdminPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('admin');

  const recentUsers = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Pro User', status: 'active', joined: '2024-01-15' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Free User', status: 'active', joined: '2024-01-14' },
    { id: 3, name: 'Mike Johnson', email: 'mike@example.com', role: 'Enterprise', status: 'pending', joined: '2024-01-13' },
    { id: 4, name: 'Sarah Wilson', email: 'sarah@example.com', role: 'Pro User', status: 'suspended', joined: '2024-01-12' },
  ];

  const systemLogs = [
    { id: 1, type: 'info', message: 'System backup completed successfully', timestamp: '2024-01-15 10:30:00' },
    { id: 2, type: 'warning', message: 'High API usage detected for user ID 1234', timestamp: '2024-01-15 09:45:00' },
    { id: 3, type: 'error', message: 'Database connection timeout on server 2', timestamp: '2024-01-15 09:15:00' },
    { id: 4, type: 'info', message: 'New user registration: jane@example.com', timestamp: '2024-01-15 08:30:00' },
  ];

  const systemStats = [
    { key: 'totalUsers', value: '12,847', change: '+156', icon: Users },
    { key: 'activeUsers', value: '8,924', change: '+89', icon: UserCheck },
    { key: 'totalRevenue', value: '$45,230', change: '+12%', icon: BarChart3 },
    { key: 'serverUptime', value: '99.9%', change: '0%', icon: Activity },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t('title')}</h1>
        <div className="flex gap-2">
          <Button variant="outline">
            <Settings className="mr-2 h-4 w-4" />
            System Settings
          </Button>
          <Button variant="outline">
            <Database className="mr-2 h-4 w-4" />
            Backup
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {systemStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.key}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{t(stat.key as keyof typeof t)}</CardTitle>
                <Icon className="h-4 w-4 text-[hsl(var(--muted-foreground))]" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-green-600">{stat.change} from last month</p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              {t('users')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-5 gap-2 text-sm font-medium text-[hsl(var(--muted-foreground))] pb-2 border-b">
                <div>Name</div>
                <div>Email</div>
                <div>Role</div>
                <div>Status</div>
                <div>Joined</div>
              </div>
              {recentUsers.map((user) => (
                <div key={user.id} className="grid grid-cols-5 gap-2 text-sm items-center">
                  <div className="font-medium">{user.name}</div>
                  <div className="text-[hsl(var(--muted-foreground))]">{user.email}</div>
                  <div>{user.role}</div>
                  <div>
                    <Badge variant={
                      user.status === 'active' ? 'default' :
                      user.status === 'pending' ? 'secondary' : 'destructive'
                    }>
                      {user.status}
                    </Badge>
                  </div>
                  <div className="text-[hsl(var(--muted-foreground))]">{user.joined}</div>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              View All Users
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5" />
              {t('logs')}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {systemLogs.map((log) => (
                <div key={log.id} className="flex items-start gap-3 p-3 border border-[hsl(var(--border))] rounded">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    log.type === 'error' ? 'bg-red-500' :
                    log.type === 'warning' ? 'bg-yellow-500' : 'bg-green-500'
                  }`}></div>
                  <div className="flex-1">
                    <div className="text-sm">{log.message}</div>
                    <div className="text-xs text-[hsl(var(--muted-foreground))]">{log.timestamp}</div>
                  </div>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              View All Logs
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>User Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center border border-[hsl(var(--border))] rounded-lg text-[hsl(var(--muted-foreground))]">
              User Growth Chart Placeholder
            </div>
            <div className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span>New Users (7d):</span>
                <span className="font-medium">234</span>
              </div>
              <div className="flex justify-between">
                <span>Churn Rate:</span>
                <span className="font-medium">2.3%</span>
              </div>
              <div className="flex justify-between">
                <span>Conversion Rate:</span>
                <span className="font-medium">12.5%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Revenue Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center border border-[hsl(var(--border))] rounded-lg text-[hsl(var(--muted-foreground))]">
              Revenue Chart Placeholder
            </div>
            <div className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span>MRR:</span>
                <span className="font-medium">$23,450</span>
              </div>
              <div className="flex justify-between">
                <span>ARPU:</span>
                <span className="font-medium">$34.20</span>
              </div>
              <div className="flex justify-between">
                <span>LTV:</span>
                <span className="font-medium">$890</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>System Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Database</span>
                <Badge variant="default">Healthy</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">API Services</span>
                <Badge variant="default">Healthy</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Trading Engine</span>
                <Badge variant="secondary">Warning</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Notification Service</span>
                <Badge variant="default">Healthy</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Storage</span>
                <Badge variant="default">Healthy</Badge>
              </div>
            </div>
            <Button variant="outline" className="w-full mt-4">
              <Shield className="mr-2 h-4 w-4" />
              System Monitor
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
              <Users className="h-8 w-8" />
              <div className="text-center">
                <div className="font-medium">User Management</div>
                <div className="text-xs text-[hsl(var(--muted-foreground))]">Manage user accounts</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
              <Settings className="h-8 w-8" />
              <div className="text-center">
                <div className="font-medium">System Config</div>
                <div className="text-xs text-[hsl(var(--muted-foreground))]">Configure settings</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
              <Database className="h-8 w-8" />
              <div className="text-center">
                <div className="font-medium">Database Tools</div>
                <div className="text-xs text-[hsl(var(--muted-foreground))]">Backup & restore</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
              <BarChart3 className="h-8 w-8" />
              <div className="text-center">
                <div className="font-medium">Analytics</div>
                <div className="text-xs text-[hsl(var(--muted-foreground))]">View detailed reports</div>
              </div>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}