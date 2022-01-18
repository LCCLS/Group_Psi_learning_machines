##helper functions##

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


starting_pos = [-3.4506836128234863, 0.9749576449394226, 0.03710094094276428]
stop = False

while not stop:

    if rob.position() == starting_pos:
        stop = True

    sensor_values = input_processing(np.array(rob.read_irs()))
    front_sensors = sensor_values[3:]

    if any(front_sensors):
        rob.move(10, -10, 1000)

    else:
        rob.move(20, 20, 1000)



