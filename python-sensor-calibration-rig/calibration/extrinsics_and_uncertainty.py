import math
from typing import Dict, Any, List, Tuple

class SensorCalibrationAndUncertaintyRig:
    """
    Layers 17-21: Handles SE(3) coordinate frame transformations (Camera <-> IMU <-> Global ENU),
    temporal synchronization between multi-camera video and IMU/GPS, and covariance error propagation.
    """

    def transform_camera_to_global_enu(
        self,
        pt_camera_xyz: Tuple[float, float, float],
        extrinsic_translation_m: Tuple[float, float, float],
        vehicle_yaw_rad: float
    ) -> Tuple[float, float, float]:
        # 1. Transform from Camera frame to Vehicle/IMU body frame via calibrated extrinsics
        bx = pt_camera_xyz[0] + extrinsic_translation_m[0]
        by = pt_camera_xyz[1] + extrinsic_translation_m[1]
        bz = pt_camera_xyz[2] + extrinsic_translation_m[2]

        # 2. Rotate from Vehicle body frame into Global East-North-Up (ENU) map frame
        cos_y = math.cos(vehicle_yaw_rad)
        sin_y = math.sin(vehicle_yaw_rad)
        enu_x = bx * cos_y - by * sin_y
        enu_y = bx * sin_y + by * cos_y
        enu_z = bz
        return (round(enu_x, 4), round(enu_y, 4), round(enu_z, 4))

    def propagate_landmark_uncertainty(
        self,
        depth_meters: float,
        pose_position_variance_m2: float,
        heading_variance_rad2: float,
        pixel_depth_variance_m2: float
    ) -> Dict[str, Any]:
        """
        First-order uncertainty propagation: Sigma_landmark = J * Sigma_sensor * J^T
        """
        lateral_error_from_heading = (depth_meters ** 2) * heading_variance_rad2
        total_trace_variance = pose_position_variance_m2 + lateral_error_from_heading + pixel_depth_variance_m2
        std_dev_meters = math.sqrt(max(0.0, total_trace_variance))

        return {
            "depth_meters": depth_meters,
            "propagated_std_dev_m": round(std_dev_meters, 4),
            "meets_hd_map_prior_spec": std_dev_meters < 0.25,
            "uncertainty_tier": "HIGH_PRECISION_HD_PRIOR" if std_dev_meters < 0.15 else "STANDARD_FLEET_PRIOR"
        }

    def synchronize_camera_imu_timestamp(
        self,
        camera_frame_ts_ns: int,
        imu_Rolling_offset_ns: int,
        angular_velocity_rad_s: float
    ) -> Dict[str, Any]:
        corrected_ts_ns = camera_frame_ts_ns + imu_Rolling_offset_ns
        motion_blur_deg = math.degrees(abs(angular_velocity_rad_s) * (abs(imu_Rolling_offset_ns) / 1e9))
        return {
            "synchronized_timestamp_ns": corrected_ts_ns,
            "rolling_shutter_angular_compensation_deg": round(motion_blur_deg, 5),
            "calibration_locked": motion_blur_deg < 0.5
        }
