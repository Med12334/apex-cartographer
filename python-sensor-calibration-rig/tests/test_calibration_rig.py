import math
from calibration.extrinsics_and_uncertainty import SensorCalibrationAndUncertaintyRig

def test_se3_camera_to_global_enu_frame_transformation():
    rig = SensorCalibrationAndUncertaintyRig()
    enu = rig.transform_camera_to_global_enu(
        pt_camera_xyz=(10.0, 0.0, 1.2),
        extrinsic_translation_m=(1.5, 0.0, 0.5),
        vehicle_yaw_rad=math.pi / 2.0
    )
    assert abs(enu[0] - 0.0) < 1e-3
    assert abs(enu[1] - 11.5) < 1e-3
    assert abs(enu[2] - 1.7) < 1e-3

def test_covariance_error_propagation_and_imu_sync():
    rig = SensorCalibrationAndUncertaintyRig()
    unc = rig.propagate_landmark_uncertainty(
        depth_meters=20.0,
        pose_position_variance_m2=0.004,
        heading_variance_rad2=0.00001,
        pixel_depth_variance_m2=0.005
    )
    assert unc["meets_hd_map_prior_spec"] is True
    assert unc["uncertainty_tier"] == "HIGH_PRECISION_HD_PRIOR"

    sync = rig.synchronize_camera_imu_timestamp(1710000000000, -2500000, 0.12)
    assert sync["calibration_locked"] is True
