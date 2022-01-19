import math

import robobo
from enum import Enum
from dataclasses import dataclass
import numpy as np
import random
import sys

from flags import FLAGS


@dataclass
class Movement:
    l_speed: int
    r_speed: int
    duration: int


class SensorStates(Enum):
    NONE = 0
    MIDDLE = 1
    CLOSE = 2


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
AMOUNT_SENSOR_STATES = 3
AMOUNT_ACTIONS = 3

LEARNING_RATE = 0.8
DISCOUNT_FACTOR = 0.95

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 5000


class Robot:

    def __init__(self):
        if FLAGS.simulated:
            self.rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)
        else:
            self.rob = robobo.HardwareRobobo(camera=True).connect(address="10.15.3.150")

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
            # Epsilon greedy learning
            if FLAGS.train:
                eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * i / EPS_DECAY)
                if random.random() < eps_threshold:
                    next_action = random.choice(list(Actions))
                    action_index = next_action.value
            if i % 10 == 0:
                print(f"Iteration {i + 1}/10000")
                if FLAGS.train:
                    print(f"Current Epsilon: {eps_threshold}")
            self.do_action(action=next_action)
            if FLAGS.train:
                reward = self.calculate_reward()
                if next_action != Actions.STRAIGHT:
                    reward -= 1
                else:
                    reward += 3
                # print(f"Total Reward: {reward}")
                next_state = self.get_current_state_index()
                self._update_state_value(state_idx=current_state, next_state_idx=next_state, action_idx=action_index,
                                         reward=reward)
        # Save Q-Matrix after learning
        if FLAGS.train:
            np.save('q_matrix.npy', self.q_matrix)
        if FLAGS.simulated:
            self.rob.pause_simulation()
            self.rob.stop_world()
        print("Run finished!")

    def do_action(self, action: Actions):
        movement = actions_movement_mapping[action]
        self.rob.move(
            left=movement.l_speed,
            right=movement.r_speed,
            millis=movement.duration
        )

    def calculate_reward(self) -> int:
        sensor_values = [int(x) for x in self.get_sensor_values()]
        reward = sum([-(2 ** x) + 1 for x in sensor_values])
        # Take the middle one again because why not?
        #reward -= sensor_values[2]
        return reward

    @staticmethod
    def process_sensor_input(sensor_value):
        if not sensor_value:
            return '0'
        normalized = sensor_value / 0.2
        if normalized < 0.5:
            return '2'
        return '1'

    def get_sensor_values(self):
        return [Robot.process_sensor_input(x) for x in self.rob.read_irs()[3:]]

    def get_current_state_index(self) -> int:
        sensor_values = self.get_sensor_values()
        base_val = ''.join(sensor_values)
        state_idx = int(base_val, AMOUNT_SENSOR_STATES)
        return state_idx

    def _update_state_value(self, state_idx: int, next_state_idx: int, action_idx: int, reward: int) -> None:
        old_value = self.q_matrix[state_idx][action_idx]
        next_q_value = np.amax(self.q_matrix[next_state_idx], axis=0)

        updated_value = (1-LEARNING_RATE) * old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_q_value)
        self.q_matrix[state_idx, action_idx] = updated_value

    def reset(self):
        self.rob.pause_simulation()
        self.rob.stop_world()


def main():
    # Print chosen options
    print(FLAGS)
    if FLAGS.simulated:
        print("Run simulated...")
    else:
        print("Run in real world...")
    if FLAGS.train:
        print("Run in training mode...")
    else:
        print("Run in regular mode...")
    robobo = Robot()
    robobo.learn()


if __name__ == "__main__":
    main()
