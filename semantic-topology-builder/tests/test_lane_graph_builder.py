from topology.lane_graph_builder import SemanticLaneTopologyBuilder

def test_catmull_rom_lane_spline_and_semantic_topology():
    builder = SemanticLaneTopologyBuilder()
    midpoint = builder.interpolate_lane_centerline_spline(
        (0.0, 0.0), (10.0, 0.0), (20.0, 2.0), (30.0, 4.0), t=0.5
    )
    assert 14.5 <= midpoint[0] <= 15.5
    assert 0.5 <= midpoint[1] <= 1.5

    topo = builder.build_semantic_road_topology(
        lane_segments=[
            {"lane_id": "lane_101", "successors": ["lane_102", "lane_103"]},
            {"lane_id": "lane_102", "successors": []}
        ],
        detected_signs=["STOP_SIGN", "SPEED_LIMIT_50"]
    )
    assert topo["total_lanes"] == 2
    assert topo["mandatory_stop_line_prior"] is True
    assert topo["semantic_layer_status"] == "HD_AUTONOMY_PRIORS_LOCKED"
