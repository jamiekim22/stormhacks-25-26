'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Target,
  Users,
  BarChart3,
  PhoneCall,
  GraduationCap,
  Settings,
  HelpCircle,
  Shield
} from 'lucide-react';

const navigationItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Employees', href: '/employees', icon: Users },
  { name: 'Campaigns', href: '/campaigns', icon: Target },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Voice Simulations', href: '/voice-simulations', icon: PhoneCall },
  { name: 'Training Modules', href: '/training-modules', icon: GraduationCap },
  { name: 'Settings', href: '/settings', icon: Settings },
  { name: 'Help & Support', href: '/help', icon: HelpCircle },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-68 max-w-[18rem] bg-[var(--color-sidebar-background)] border-r border-[var(--color-border)] flex flex-col shadow-[0_20px_45px_rgba(5,12,25,0.45)]">
      {/* Logo / Brand */}
      <div className="px-6 pt-8 pb-6 border-b border-[rgba(255,255,255,0.04)] paddingClass">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-xl bg-[var(--color-accent)]/20 text-[var(--color-accent)] flex items-center justify-center">
            <Shield className="h-6 w-6" />
          </div>
          <div className="leading-tight">
            <p className="text-xl font-semibold text-white">PhishPatrol</p>
            <p className="text-sm text-[var(--color-text-muted)]">Enterprise Version</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-4 py-6 paddingClass">
        <ul className="space-y-1.5">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`group relative flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'text-white bg-[var(--color-sidebar-active)] shadow-[0_12px_32px_rgba(59,130,246,0.15)] before:absolute before:left-0 before:top-1/2 before:h-[70%] before:w-[3px] before:-translate-y-1/2 before:rounded-full before:bg-[var(--color-accent)]'
                      : 'text-[var(--color-text-muted)] hover:text-white hover:bg-[var(--color-sidebar-hover)]/90'
                  }`}
                >
                  <span className="flex h-9 w-9 items-center justify-center">
                    <Icon className={`h-5 w-5 transition-colors duration-200 ${
                      isActive 
                        ? 'text-[var(--color-accent)]' 
                        : 'text-[var(--color-text-muted)] group-hover:text-[var(--color-accent)]'
                    }`} />
                  </span>
                  <span>{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User footer */}
      <div className="px-6 py-5 border-t border-[rgba(255,255,255,0.04)] bg-[var(--color-sidebar-background)]/92 paddingClass">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-full bg-[var(--color-accent)]/25 flex items-center justify-center text-[var(--color-accent)]">
            <Users className="h-4 w-4" />
          </div>
          <div className="leading-tight text-sm">
            <p className="text-white font-medium">John Doe</p>
            <p className="text-[var(--color-text-muted)] text-xs">Security Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}