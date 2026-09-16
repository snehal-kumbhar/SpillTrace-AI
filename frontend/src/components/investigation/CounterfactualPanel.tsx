import type { CandidateVesselMatch } from '../../types';
import { Panel } from '../ui/Panel';

export function CounterfactualPanel({ candidate }: { candidate: CandidateVesselMatch }) {
  const metrics = [
    { label: 'Spatial overlap', value: candidate.counterfactual_spatial_overlap_pct, unit: '%' },
    { label: 'Centroid error', value: candidate.counterfactual_centroid_error_km, unit: ' km' },
    { label: 'Shape similarity', value: candidate.counterfactual_shape_similarity, unit: '%' },
    { label: 'Drift consistency', value: candidate.drift_consistency, unit: '%' },
    { label: 'Temporal consistency', value: candidate.counterfactual_temporal_consistency, unit: '%' },
    { label: 'Overall similarity', value: candidate.counterfactual_overall_similarity, unit: '%' },
  ];

  return (
    <Panel title="Counterfactual Spill Simulation">
      <p className="text-xs text-text-muted mb-4">
        Simulate the expected spill trajectory assuming this vessel was the source. Observed vs. simulated comparison (mock).
      </p>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="border border-panel-border rounded-sm p-3 bg-navy-800/40">
          <p className="text-[10px] uppercase tracking-wider text-text-muted mb-2">Observed Spill</p>
          <div className="h-24 rounded bg-gradient-to-br from-amber-900/40 to-amber-700/20 border border-amber-500/30 flex items-center justify-center">
            <span className="text-xs text-amber-300 font-mono">SAR-detected slick</span>
          </div>
        </div>
        <div className="border border-panel-border rounded-sm p-3 bg-navy-800/40">
          <p className="text-[10px] uppercase tracking-wider text-text-muted mb-2">Simulated Spill</p>
          <div className="h-24 rounded bg-gradient-to-br from-cyan-900/40 to-cyan-700/20 border border-accent/30 flex items-center justify-center">
            <span className="text-xs text-accent font-mono">Counterfactual model</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {metrics.map(({ label, value, unit }) => (
          value != null && (
            <div key={label} className="p-2 bg-navy-800/50 border border-panel-border rounded-sm">
              <p className="text-[10px] text-text-muted uppercase">{label}</p>
              <p className="font-mono text-sm text-white mt-0.5">
                {typeof value === 'number' ? value.toFixed(1) : value}{unit}
              </p>
            </div>
          )
        ))}
      </div>
    </Panel>
  );
}
