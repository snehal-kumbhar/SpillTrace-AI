import { Routes, Route } from 'react-router-dom';
import { AppShell } from '../../components/layout/AppShell';
import { DashboardPage } from '../../features/dashboard/DashboardPage';
import { InvestigationsPage } from '../../features/investigations/InvestigationsPage';
import { InvestigationDetailPage } from '../../features/investigations/InvestigationDetailPage';
import { SpillDetectionPage } from '../../features/spills/SpillDetectionPage';
import { MaritimeMapPage } from '../../features/map/MaritimeMapPage';
import { VesselsPage } from '../../features/vessels/VesselsPage';
import { VesselDetailPage } from '../../features/vessels/VesselDetailPage';
import { DriftAnalysisPage } from '../../features/drift/DriftAnalysisPage';
import { EvidencePage } from '../../features/evidence/EvidencePage';
import { ReportsPage } from '../../features/reports/ReportsPage';
import { DataSourcesPage } from '../../features/data-sources/DataSourcesPage';
import { SettingsPage } from '../../features/settings/SettingsPage';

export function AppRouter() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<DashboardPage />} />
        <Route path="investigations" element={<InvestigationsPage />} />
        <Route path="investigations/:id" element={<InvestigationDetailPage />} />
        <Route path="spill-detection" element={<SpillDetectionPage />} />
        <Route path="maritime-map" element={<MaritimeMapPage />} />
        <Route path="vessels" element={<VesselsPage />} />
        <Route path="vessels/:id" element={<VesselDetailPage />} />
        <Route path="drift-analysis" element={<DriftAnalysisPage />} />
        <Route path="evidence" element={<EvidencePage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="data-sources" element={<DataSourcesPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  );
}
