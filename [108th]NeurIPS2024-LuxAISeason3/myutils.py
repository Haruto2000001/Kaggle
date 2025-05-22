def is_target_in_sap_range(unit_sap_range, unit_pos, tar_pos):
    delta_x = abs(tar_pos[0] - unit_pos[0])
    delta_y = abs(tar_pos[1] - unit_pos[1])
    return delta_x < unit_sap_range and delta_y < unit_sap_range

def pos_abs2rel(unit_pos, tar_pos):
    return (tar_pos[0]-unit_pos[0], tar_pos[1]-unit_pos[1])

