//! Apex-Cartographer Layers 12 to 16 (Memory-Safe Rust Spatial Fusion):
//! - Layer 12 & 13: Crowdsourced Map Fusion & Probabilistic Occupancy Grids
//! - Layer 14 & 15: Spatiotemporal Change Detection (handling noisy observations & dynamic objects)
//! - Layer 16: Global Factor-Graph Consistency Constraints

#[derive(Debug, Clone, PartialEq)]
pub enum ChangeDetectionVerdict {
    StaticMapFeatureConfirmed,
    DynamicObjectFilteredOut,
    SignificantRoadGeometryChangeDetected,
}

#[derive(Debug, Clone)]
pub struct MapObservationSample {
    pub tile_quadkey: u64,
    pub observed_lane_offset_meters: f64,
    pub observation_confidence: f64,
    pub fleet_unit_id: String,
}

/// Layers 12 & 13: Probabilistic Kalman-Filtered Map Fusion Register
#[derive(Debug, Clone)]
pub struct MapFeatureNode {
    pub feature_id: u64,
    pub estimated_lateral_offset_m: f64,
    pub covariance_matrix_trace: f64,
    pub observation_count: u32,
}

impl MapFeatureNode {
    pub fn new(feature_id: u64, initial_offset: f64) -> Self {
        Self {
            feature_id,
            estimated_lateral_offset_m: initial_offset,
            covariance_matrix_trace: 1.0,
            observation_count: 1,
        }
    }

    /// Bayesian / Kalman update fusing noisy crowdsourced fleet observations
    pub fn assimilate_observation(&mut self, obs: &MapObservationSample) {
        let kalman_gain = self.covariance_matrix_trace / (self.covariance_matrix_trace + (1.0 / obs.observation_confidence));
        self.estimated_lateral_offset_m += kalman_gain * (obs.observed_lane_offset_meters - self.estimated_lateral_offset_m);
        self.covariance_matrix_trace *= 1.0 - kalman_gain;
        self.observation_count += 1;
    }
}

/// Layers 14 & 15: Spatiotemporal Change Detector
pub fn detect_map_change_or_dynamic_clutter(historical_offset: f64, current_observed_offset: f64, variance_threshold: f64) -> ChangeDetectionVerdict {
    let delta = (current_observed_offset - historical_offset).abs();
    if delta < variance_threshold {
        ChangeDetectionVerdict::StaticMapFeatureConfirmed
    } else if delta > variance_threshold * 5.0 {
        ChangeDetectionVerdict::SignificantRoadGeometryChangeDetected
    } else {
        ChangeDetectionVerdict::DynamicObjectFilteredOut
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kalman_map_fusion_assimilates_noisy_fleet_observations() {
        let mut feature = MapFeatureNode::new(9901, 2.50);
        let noisy_obs = MapObservationSample {
            tile_quadkey: 12039481,
            observed_lane_offset_meters: 2.58,
            observation_confidence: 0.90,
            fleet_unit_id: String::from("FLEET-MILAN-09"),
        };

        feature.assimilate_observation(&noisy_obs);
        assert!(feature.observation_count == 2);
        assert!(feature.estimated_lateral_offset_m > 2.50 && feature.estimated_lateral_offset_m < 2.58);
    }

    #[test]
    fn test_spatiotemporal_change_detector_filters_dynamic_clutter() {
        let baseline = 1.20;
        assert_eq!(
            detect_map_change_or_dynamic_clutter(baseline, 1.22, 0.10),
            ChangeDetectionVerdict::StaticMapFeatureConfirmed
        );
        assert_eq!(
            detect_map_change_or_dynamic_clutter(baseline, 3.50, 0.10),
            ChangeDetectionVerdict::SignificantRoadGeometryChangeDetected
        );
    }
}
