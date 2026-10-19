package main

import (
"math"
)

// Layers 22-27: Planet-Scale Map Evaluation Metrics (Accuracy, Freshness, Coverage,
// Global Consistency, and Downstream Autonomous Driving Impact)
type MapTileTelemetry struct {
TileQuadKey                string
RelativeAccuracyRmseMeters float64
HoursSinceLastFleetPass    float64
ObservedLanesCount         int
ExpectedLanesCount         int
LoopClosureResidualMeters  float64
}

type MapTileEvaluationReport struct {
TileQuadKey          string
FreshnessScore       float64
CoverageRatio        float64
AutonomyReady        bool
TriageActionRequired string
}

func EvaluateMapTileQuality(tile MapTileTelemetry) MapTileEvaluationReport {
// Exponential freshness decay with 72-hour half-life
freshness := math.Exp(-tile.HoursSinceLastFleetPass / 72.0)

coverage := 0.0
if tile.ExpectedLanesCount > 0 {
coverage = float64(tile.ObservedLanesCount) / float64(tile.ExpectedLanesCount)
if coverage > 1.0 {
coverage = 1.0
}
}

autonomyReady := tile.RelativeAccuracyRmseMeters <= 0.15 &&
freshness >= 0.50 &&
coverage >= 0.95 &&
tile.LoopClosureResidualMeters <= 0.20

triage := "PUBLISH_TO_AUTONOMOUS_FLEET"
if !autonomyReady {
if tile.LoopClosureResidualMeters > 0.20 {
triage = "TRIGGER_GLOBAL_BUNDLE_ADJUSTMENT_REOPTIMIZATION"
} else if freshness < 0.50 {
triage = "REQUEST_PRIORITY_CROWDSOURCED_FLEET_COLLECTION"
} else {
triage = "QUARANTINE_TILE_FOR_3D_RECONSTRUCTION_TRIAGE"
}
}

return MapTileEvaluationReport{
TileQuadKey:          tile.TileQuadKey,
FreshnessScore:       math.Round(freshness*1000) / 1000,
CoverageRatio:        math.Round(coverage*1000) / 1000,
AutonomyReady:        autonomyReady,
TriageActionRequired: triage,
}
}
