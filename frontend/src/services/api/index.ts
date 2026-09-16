import { apiFetch } from './client';
import type {
  Investigation, SpillEvent, Vessel, DriftSimulation,
  AttributionResult, EvidenceItem, ForensicReport, DataSource, Dashboard,
} from '../../types';

export const api = {
  dashboard: () => apiFetch<Dashboard>('/dashboard'),

  investigations: {
    list: () => apiFetch<{ items: Investigation[]; total: number }>('/investigations'),
    get: (id: string) => apiFetch<Investigation>(`/investigations/${id}`),
    spills: (id: string) => apiFetch<SpillEvent[]>(`/investigations/${id}/spills`),
    drift: (id: string) => apiFetch<DriftSimulation>(`/investigations/${id}/drift`),
    attribution: (id: string) => apiFetch<AttributionResult>(`/investigations/${id}/attribution`),
    evidence: (id: string) => apiFetch<{ items: EvidenceItem[]; total: number }>(`/investigations/${id}/evidence`),
    report: (id: string) => apiFetch<ForensicReport>(`/investigations/${id}/report`),
  },

  spills: {
    list: () => apiFetch<{ items: SpillEvent[]; total: number }>('/spills'),
    get: (id: string) => apiFetch<SpillEvent>(`/spills/${id}`),
    detect: (investigationId: string) =>
      apiFetch<SpillEvent>('/spills/detect', {
        method: 'POST',
        body: JSON.stringify({ investigation_id: investigationId }),
      }),
  },

  vessels: {
    list: () => apiFetch<{ items: Vessel[]; total: number }>('/vessels'),
    get: (id: string) => apiFetch<Vessel>(`/vessels/${id}`),
    trajectory: (id: string) => apiFetch<Vessel & { trajectories: import('../../types').TrajectoryPoint[] }>(`/vessels/${id}/trajectory`),
  },

  drift: {
    simulate: (investigationId: string) =>
      apiFetch<DriftSimulation>('/drift/simulate', {
        method: 'POST',
        body: JSON.stringify({ investigation_id: investigationId }),
      }),
  },

  attribution: {
    analyze: (investigationId: string) =>
      apiFetch<AttributionResult>('/attribution/analyze', {
        method: 'POST',
        body: JSON.stringify({ investigation_id: investigationId }),
      }),
  },

  evidence: {
    list: (investigationId?: string) =>
      apiFetch<{ items: EvidenceItem[]; total: number }>(
        investigationId ? `/evidence?investigation_id=${investigationId}` : '/evidence',
      ),
  },

  reports: {
    generate: (investigationId: string) =>
      apiFetch<ForensicReport>('/reports', {
        method: 'POST',
        body: JSON.stringify({ investigation_id: investigationId }),
      }),
  },

  dataSources: () => apiFetch<DataSource[]>('/data-sources'),
};
