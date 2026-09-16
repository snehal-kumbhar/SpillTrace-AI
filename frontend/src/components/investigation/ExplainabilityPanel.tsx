import { CheckCircle2 } from 'lucide-react';
import { Badge, statusVariant } from '../ui/Badge';
import type { CandidateVesselMatch } from '../../types';

export function ExplainabilityPanel({ candidate }: { candidate: CandidateVesselMatch }) {
  return (
    <div className="space-y-4">
      <div>
        <h4 className="text-sm font-semibold text-white mb-2">Why this vessel ranked highly</h4>
        <p className="text-xs text-text-muted mb-3">
          Evidence-based forensic explanation. Rankings reflect probabilistic assessments, not definitive conclusions.
        </p>
        <ul className="space-y-2">
          {candidate.evidence_bullets.map((bullet, i) => (
            <li key={i} className="flex gap-2 text-sm text-text">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="flex items-center gap-2 pt-2 border-t border-panel-border">
        <span className="text-xs text-text-muted">Evidence strength:</span>
        <Badge variant={statusVariant(candidate.evidence_strength)}>{candidate.evidence_strength}</Badge>
      </div>
    </div>
  );
}
