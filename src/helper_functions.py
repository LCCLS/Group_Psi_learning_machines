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


for i in range(50):
    # print("ROB Irs: {}".format(np.log(np.array(rob.read_irs())) / 10))
    sensor_values = input_processing(np.array(rob.read_irs()))
    if any(sensor_values):
        rob.move(0, 0, 1000)
        rob.move(10, 0, 1000)
        rob.move(10, 10, 1000)
    else:
        rob.move(10, 10, 1000)
