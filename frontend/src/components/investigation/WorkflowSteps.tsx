import clsx from 'clsx';
import { WORKFLOW_STAGES } from '../../types';

export function WorkflowSteps({ currentStage }: { currentStage: number }) {
  return (
    <div className="flex flex-wrap gap-1">
      {WORKFLOW_STAGES.map((stage, i) => {
        const step = i + 1;
        const isComplete = step < currentStage;
        const isCurrent = step === currentStage;
        return (
          <div
            key={stage}
            className={clsx(
              'flex items-center gap-1.5 px-2.5 py-1.5 rounded text-xs border',
              isComplete && 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
              isCurrent && 'bg-accent/10 border-accent/40 text-accent',
              !isComplete && !isCurrent && 'bg-navy-800 border-panel-border text-text-muted',
            )}
          >
            <span className="font-mono w-4 text-center">{step}</span>
            <span className="hidden sm:inline">{stage}</span>
          </div>
        );
      })}
    </div>
  );
}
