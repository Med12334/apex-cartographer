import React, { useState } from 'react';

export interface QuadKeyDiagnostic {
  quadKey: string;
  reprojectionErrorPx: number;
  localizationDriftMeters: number;
  fleetPasses24h: number;
  status: string;
}

export const CartographyTriageDashboard: React.FC = () => {
  const [tiles] = useState<QuadKeyDiagnostic[]>([
    { quadKey: '12021023312', reprojectionErrorPx: 0.42, localizationDriftMeters: 0.06, fleetPasses24h: 1840, status: 'AUTONOMY_LOCKED' },
    { quadKey: '12021023399', reprojectionErrorPx: 2.85, localizationDriftMeters: 0.91, fleetPasses24h: 410, status: 'BUNDLE_ADJUSTMENT_QUEUED' }
  ]);

  return (
    <main style={{ background: '#070b12', color: '#e6edf3', minHeight: '100vh', padding: '28px', fontFamily: 'monospace' }}>
      <header style={{ borderBottom: '2px solid #388bfd', paddingBottom: '16px' }}>
        <h1 style={{ margin: 0, color: '#58a6ff' }}>APEX-CARTOGRAPHER // Planet-Scale 3D Reconstruction & HD Map Triage Center</h1>
        <p style={{ margin: '6px 0 0', color: '#8b949e' }}>
          C++20 Fleet Ingest & Multi-View SfM | Rust Kalman Map Fusion | Python SE(3) Calibration & Lane Splines | Go Freshness Evaluator
        </p>
      </header>
      <section style={{ marginTop: '24px' }}>
        {tiles.map((t) => (
          <div key={t.quadKey} style={{ background: '#0d1117', border: '1px solid #30363d', padding: '16px', marginBottom: '12px', borderRadius: '8px' }}>
            <strong>QuadKey: {t.quadKey}</strong> | Reprojection Error: {t.reprojectionErrorPx}px | Drift: {t.localizationDriftMeters}m | Status: {t.status}
          </div>
        ))}
      </section>
    </main>
  );
};
