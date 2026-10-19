/**
 * Layer 34: Pure diagnostic selector classifying 3D reconstruction reprojection error,
 * GPS/IMU localization drift, and crowdsourced fleet coverage gaps.
 */
export function classifyReconstructionTile({ reprojectionErrorPx, localizationDriftMeters, fleetPasses24h }) {
  if (reprojectionErrorPx > 1.5 || localizationDriftMeters > 0.25) {
    return {
      severity: 'HIGH_GEOMETRIC_RESIDUAL',
      action: 'RETRIGGER_INCREMENTAL_SfM_AND_BUNDLE_ADJUSTMENT',
      autonomySafe: false
    };
  }
  if (fleetPasses24h < 25) {
    return {
      severity: 'FLEET_COVERAGE_GAP',
      action: 'DISPATCH_ACTIVE_FLEET_CAMERA_UPLOAD_QUERY',
      autonomySafe: false
    };
  }
  return {
    severity: 'NOMINAL_HD_MAP_PRIOR',
    action: 'STREAM_TO_AUTONOMOUS_PLANNING_STACK',
    autonomySafe: true
  };
}
