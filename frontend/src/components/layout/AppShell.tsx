import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

const pageTitles: Record<string, { title: string; breadcrumb?: string }> = {
  '/': { title: 'Command Center', breadcrumb: 'SpillTrace AI' },
  '/investigations': { title: 'Investigations', breadcrumb: 'Forensic Cases' },
  '/spill-detection': { title: 'Spill Detection', breadcrumb: 'SAR Analysis' },
  '/maritime-map': { title: 'Maritime Intelligence Map', breadcrumb: 'GIS Investigation' },
  '/vessels': { title: 'Vessel Registry', breadcrumb: 'AIS Intelligence' },
  '/drift-analysis': { title: 'Drift Analysis', breadcrumb: 'Lagrangian Reconstruction' },
  '/evidence': { title: 'Evidence Panel', breadcrumb: 'Forensic Evidence' },
  '/reports': { title: 'Investigation Reports', breadcrumb: 'Reporting' },
  '/data-sources': { title: 'Data Sources', breadcrumb: 'System Monitoring' },
  '/settings': { title: 'Settings', breadcrumb: 'Configuration' },
};

export function AppShell() {
  const location = useLocation();
  const basePath = location.pathname.split('/').slice(0, 2).join('/') || '/';
  const meta = pageTitles[location.pathname] ?? pageTitles[basePath] ?? { title: 'SpillTrace AI' };

  return (
    <div className="flex h-full bg-navy-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar title={meta.title} breadcrumb={meta.breadcrumb} />
        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
