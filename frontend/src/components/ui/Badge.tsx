import clsx from 'clsx';

const variants: Record<string, string> = {
  default: 'bg-navy-600 text-text-muted border-panel-border',
  critical: 'bg-red-500/15 text-red-400 border-red-500/30',
  high: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  medium: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
  low: 'bg-slate-500/15 text-slate-400 border-slate-500/30',
  online: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  success: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  warning: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
};

export function Badge({ children, variant = 'default', className }: {
  children: React.ReactNode;
  variant?: keyof typeof variants;
  className?: string;
}) {
  return (
    <span className={clsx(
      'inline-flex items-center px-2 py-0.5 text-xs font-medium border rounded',
      variants[variant] ?? variants.default,
      className,
    )}>
      {children}
    </span>
  );
}

export function statusVariant(status: string): keyof typeof variants {
  const s = status.toLowerCase();
  if (s.includes('critical')) return 'critical';
  if (s.includes('high') || s.includes('attributed')) return 'high';
  if (s.includes('medium') || s.includes('investigation')) return 'medium';
  if (s.includes('closed') || s.includes('low')) return 'low';
  if (s.includes('online')) return 'online';
  return 'default';
}
