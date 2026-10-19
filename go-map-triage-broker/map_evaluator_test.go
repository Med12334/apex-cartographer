package main

import "testing"

func TestEvaluateMapTileQualityApprovesFreshAccurateTile(t *testing.T) {
goodTile := MapTileTelemetry{
TileQuadKey:                "12021023312",
RelativeAccuracyRmseMeters: 0.08,
HoursSinceLastFleetPass:    6.0,
ObservedLanesCount:         4,
ExpectedLanesCount:         4,
LoopClosureResidualMeters:  0.05,
}

report := EvaluateMapTileQuality(goodTile)
if !report.AutonomyReady || report.TriageActionRequired != "PUBLISH_TO_AUTONOMOUS_FLEET" {
t.Fatalf("Expected high-precision fresh map tile to be published, got %+v", report)
}
}

func TestEvaluateMapTileQualityFlagsLoopClosureDrift(t *testing.T) {
driftedTile := MapTileTelemetry{
TileQuadKey:                "12021023399",
RelativeAccuracyRmseMeters: 0.09,
HoursSinceLastFleetPass:    4.0,
ObservedLanesCount:         4,
ExpectedLanesCount:         4,
LoopClosureResidualMeters:  0.85,
}

report := EvaluateMapTileQuality(driftedTile)
if report.AutonomyReady || report.TriageActionRequired != "TRIGGER_GLOBAL_BUNDLE_ADJUSTMENT_REOPTIMIZATION" {
t.Fatalf("Expected loop-closure drift to trigger global bundle adjustment, got %+v", report)
}
}
