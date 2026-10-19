import test from 'node:test';
import assert from 'node:assert/strict';
import { classifyReconstructionTile } from './triage_selector.mjs';

test('Layer 34: React Cartography Triage selector flags high bundle-adjustment reprojection residuals and fleet gaps', () => {
  const drifted = classifyReconstructionTile({
    reprojectionErrorPx: 2.4,
    localizationDriftMeters: 0.45,
    fleetPasses24h: 500
  });
  assert.equal(drifted.autonomySafe, false);
  assert.equal(drifted.action, 'RETRIGGER_INCREMENTAL_SfM_AND_BUNDLE_ADJUSTMENT');

  const sparse = classifyReconstructionTile({
    reprojectionErrorPx: 0.5,
    localizationDriftMeters: 0.08,
    fleetPasses24h: 4
  });
  assert.equal(sparse.autonomySafe, false);
  assert.equal(sparse.severity, 'FLEET_COVERAGE_GAP');

  const nominal = classifyReconstructionTile({
    reprojectionErrorPx: 0.41,
    localizationDriftMeters: 0.06,
    fleetPasses24h: 1200
  });
  assert.equal(nominal.autonomySafe, true);
  assert.equal(nominal.severity, 'NOMINAL_HD_MAP_PRIOR');
});
