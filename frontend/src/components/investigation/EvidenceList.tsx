import { Badge, statusVariant } from '../ui/Badge';
import type { EvidenceItem } from '../../types';

const TYPE_LABELS: Record<string, string> = {
  sar_imagery: 'SAR Imagery',
  ais_trajectory: 'AIS Trajectory',
  wind_data: 'Wind Data',
  ocean_current: 'Ocean Current',
  drift_simulation: 'Drift Simulation',
  vessel_behaviour: 'Vessel Behaviour',
  counterfactual: 'Counterfactual Simulation',
  model_prediction: 'Model Prediction',
};

export function EvidenceList({ items }: { items: EvidenceItem[] }) {
  if (items.length === 0) {
    return <p className="text-sm text-text-muted">No evidence items available.</p>;
  }

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div
          key={item.id}
          className="p-3 border border-panel-border rounded-sm bg-navy-800/30 hover:border-accent/20 transition-colors"
        >
          <div className="flex flex-wrap items-start justify-between gap-2">
            <div>
              <p className="text-sm font-medium text-white">{item.title}</p>
              <p className="text-xs text-text-muted mt-0.5">
                {TYPE_LABELS[item.evidence_type] ?? item.evidence_type} · {item.source}
              </p>
            </div>
            <div className="flex gap-2">
              <Badge variant={statusVariant(item.confidence >= 80 ? 'High' : item.confidence >= 60 ? 'Medium' : 'Low')}>
                {item.confidence.toFixed(0)}% conf.
              </Badge>
              <Badge variant="default">{item.relevance.toFixed(0)}% rel.</Badge>
            </div>
          </div>
          {item.description && (
            <p className="text-xs text-text-muted mt-2 leading-relaxed">{item.description}</p>
          )}
          {item.evidence_timestamp && (
            <p className="font-mono text-[10px] text-text-muted mt-2">
              {new Date(item.evidence_timestamp).toUTCString()}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
