import { ScoreBar } from '../ui/Panel';
import { Badge, statusVariant } from '../ui/Badge';
import type { CandidateVesselMatch } from '../../types';

const SCORE_LABELS: Array<{ key: keyof CandidateVesselMatch; label: string }> = [
  { key: 'temporal_compatibility', label: 'Temporal compatibility' },
  { key: 'spatial_proximity', label: 'Spatial proximity' },
  { key: 'drift_consistency', label: 'Drift consistency' },
  { key: 'trajectory_compatibility', label: 'Trajectory compatibility' },
  { key: 'behaviour_anomaly', label: 'Behaviour anomaly' },
  { key: 'counterfactual_similarity', label: 'Counterfactual similarity' },
];

export function AttributionBreakdown({ candidate }: { candidate: CandidateVesselMatch }) {
  const level = candidate.confidence_level.toUpperCase().includes('HIGH')
    ? 'HIGH ATTRIBUTION LIKELIHOOD'
    : candidate.confidence_level.toUpperCase().includes('MEDIUM')
      ? 'MODERATE ATTRIBUTION LIKELIHOOD'
      : 'LOW ATTRIBUTION LIKELIHOOD';

  return (
    <div className="space-y-4">
      <div className="text-center py-4 border border-panel-border rounded-sm bg-navy-800/30">
        <p className="font-mono text-4xl font-bold text-accent">{candidate.overall_score.toFixed(1)}</p>
        <p className="text-xs text-text-muted mt-1">/ 100</p>
        <p className="text-sm font-semibold text-white mt-3">{level}</p>
        <Badge variant={statusVariant(candidate.confidence_level)} className="mt-2">
          {candidate.confidence_level} confidence
        </Badge>
      </div>

      <div className="space-y-3">
        {SCORE_LABELS.map(({ key, label }) => (
          <ScoreBar key={key} label={label} value={candidate[key] as number} />
        ))}
      </div>
    </div>
  );
}
