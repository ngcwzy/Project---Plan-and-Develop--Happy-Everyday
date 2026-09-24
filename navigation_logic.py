def navigate(sensor_data):
    if sensor_data['front'] == 'obstacle':
        return 'LEFT'
    elif sensor_data['left'] == 'obstacle':
        return 'RIGHT'
    elif sensor_data['right'] == 'obstacle':
        return 'LEFT'
    elif sensor_data['front'] == 'target' and not sensor_data['left'] == 'obstacle' and not sensor_data['right'] == 'obstacle':
        return 'FORWARD'
    elif sensor_data['goal_reached']:
        return 'STOP'
    else:
        return 'FORWARD'
