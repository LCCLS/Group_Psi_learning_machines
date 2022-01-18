import numpy as np


def input_processing(sensor_data):
    sensors = []
    for i in range(len(sensor_data)):
        if not sensor_data[i]:
            sensors.append(0)
        else:
            normalised_i = (sensor_data[i] - 0.14) / 0.14
            if 0 < normalised_i < 0.25:
                sensors.append(1)
            elif 0 < normalised_i < 0.75:
                sensors.append(2)
            else:
                sensors.append(3)
    return sensors

    pass


def weighted_punishment(sensor_input):
    current_state = sum(sensor_input)
    return 2**current_state


print(weighted_punishment([3, 3, 3, 3, 3]))