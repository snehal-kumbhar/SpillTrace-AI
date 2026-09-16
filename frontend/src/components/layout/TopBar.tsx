import { Bell, Search, User } from 'lucide-react';

export function TopBar({ title, breadcrumb }: { title: string; breadcrumb?: string }) {
  return (
    <header className="h-14 flex-shrink-0 bg-navy-900/80 border-b border-panel-border flex items-center justify-between px-6 backdrop-blur-sm">
      <div>
        {breadcrumb && (
          <p className="text-[10px] text-text-muted uppercase tracking-widest mb-0.5">{breadcrumb}</p>
        )}
        <h1 className="text-base font-semibold text-white">{title}</h1>
      </div>
      <div className="flex items-center gap-4">
        <div className="relative hidden md:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="search"
            placeholder="Search investigations, vessels, IMO..."
            className="pl-9 pr-4 py-1.5 w-72 bg-navy-800 border border-panel-border rounded text-sm text-text placeholder:text-text-muted focus:outline-none focus:border-accent/50"
          />
        </div>
        <div className="flex items-center gap-1.5 text-xs text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-subtle" />
          Data Fresh
        </div>
        <button type="button" className="p-1.5 text-text-muted hover:text-text transition-colors">
          <Bell className="w-4 h-4" />
        </button>
        <button type="button" className="p-1.5 text-text-muted hover:text-text transition-colors">
          <User className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
