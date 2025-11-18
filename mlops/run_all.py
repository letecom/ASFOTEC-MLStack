#!/usr/bin/env python
"""End-to-end pipeline: train → evaluate → gate/tag Production."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mlops.config import get_settings
from mlops.eval_classifier import evaluate_run
from mlops.quality_gate import enforce_quality
from mlops.training.train_classifier import train_model


def main() -> None:
    settings = get_settings()
    Path('mlops/artifacts').mkdir(parents=True, exist_ok=True)

    print('🚀 Training classifier...')
    run_id, train_metrics = train_model(settings)
    print(f'✅ Training finished. Run: {run_id}')

    print('🔎 Evaluating run...')
    eval_metrics, report_path = evaluate_run(settings, run_id)
    print(f'📄 Eval report saved to {report_path}')

    combined_metrics = {**train_metrics, **eval_metrics}
    Path('mlops/artifacts/train_eval_summary.json').write_text(json.dumps(combined_metrics, indent=2))

    print('🛡️  Checking quality gate...')
    enforce_quality(settings, eval_metrics, run_id)
    print('🏷️  Tagged Production run successfully.')

    print('🎉 Pipeline complete! Latest metrics:')
    for key, value in eval_metrics.items():
        if key in {'run_id', 'confusion_matrix'}:
            continue
        print(f'- {key}: {value:.3f}')


if __name__ == '__main__':
    main()
