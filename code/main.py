import robobo
from enum import Enum
from dataclasses import dataclass
import numpy as np


@dataclass
class Movement:
    l_speed: int
    r_speed: int
    duration: int


class SensorStates(Enum):
    NONE = 0
    FAR = 1
    MIDDLE = 2
    CLOSE = 3


class Actions(Enum):
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2


actions_movement_mapping = {
    Actions.STRAIGHT: Movement(10, 10, 1000),
    Actions.LEFT: Movement(-5, 5, 1000),
    Actions.RIGHT: Movement(5, -5, 1000)
}

AMOUNT_SENSORS = 5
AMOUNT_SENSOR_STATES = 4
AMOUNT_ACTIONS = 3

LEARNING_RATE = 0.9
DISCOUNT_FACTOR = 0.99


class Robot:

    def __init__(self):
        self.rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)
        self.rob.play_simulation()

        #self.q_matrix = np.zeros((AMOUNT_SENSOR_STATES ** AMOUNT_SENSORS, AMOUNT_ACTIONS))
        # Load Q-Matrix
        self.q_matrix = np.load('q_matrix.npy')

    def move_straight(self):
        self.rob.move(20, 20, 5000)

    def learn(self, iterations: int = 10000):
        for i in range(iterations):
            current_state = self.get_current_state_index()
            action_index = np.argmax(self.q_matrix[current_state])
            next_action = Actions(action_index)
            reward = self.do_action(action=next_action)
            # TODO: Continue with this only after action is finished
            next_state = self.get_current_state_index()
            self._update_state_value(state_idx=current_state, next_state_idx=next_state, action_idx=action_index,
                                     reward=reward)
        # Save Q-Matrix after learning
        np.save('q_matrix.npy', self.q_matrix)

    def do_action(self, action: Actions) -> int:
        movement = actions_movement_mapping[action]
        self.rob.move(
            left=movement.l_speed,
            right=movement.r_speed,
            millis=movement.duration
        )
        reward = -5
        return reward

    @staticmethod
    def process_sensor_input(sensor_value):
        if not sensor_value:
            return '0'
        normalized = (sensor_value - 0.14) / 0.14
        if normalized < 0.25:
            return '1'
        elif normalized < 0.75:
            return '2'
        return '3'


    @staticmethod
    def input_processing(sensor_data):
        return [Robot.process_sensor_input(x) for x in sensor_data]

    def get_current_state_index(self) -> int:
        sensor_values = Robot.input_processing(np.array(self.rob.read_irs()))
        base_val = ''.join(sensor_values)
        state_idx = int(base_val, 4)
        return state_idx

    def _update_state_value(self, state_idx: int, next_state_idx: int, action_idx: int, reward: int) -> None:
        old_value = self.q_matrix((state_idx, action_idx))
        next_q_value = np.amax(self.q_matrix[next_state_idx], axis=0)

        updated_value = old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_q_value - old_value)
        self.q_matrix[state_idx, action_idx] = updated_value


def main():
    robobo = Robot()
    robobo.move_straight()


if __name__ == "__main__":
    main()
