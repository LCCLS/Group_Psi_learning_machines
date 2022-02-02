import math
import random
from dataclasses import dataclass
from enum import Enum

import time
import numpy as np

import robobo
from ObjectDetector import ObjectDetector
from util import Actions, Task, actions_movement_mapping

LEARNING_RATE = 0.9
DISCOUNT_FACTOR = 0.7

AMOUNT_IMAGE_SPLITS = 5
AMOUNT_ACTIONS = 3

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 7000

PHONE_TILT = 0.5


class Robot:

    def __init__(self, simulated: bool = False, address: str = '127.0.0.1'):
        self.simulated = simulated
        self._address = address
        if simulated:
            self._rob = robobo.SimulationRobobo().connect(address=address, port=19997)
            self._rob.play_simulation()
            self._rob.set_phone_tilt(PHONE_TILT, 100)
        else:
            self._rob = robobo.HardwareRobobo(camera=True).connect(address=address)
            self._rob.set_phone_tilt(PHONE_TILT, 100)

        self._food_q_matrix = np.full((2 ** AMOUNT_IMAGE_SPLITS, AMOUNT_ACTIONS), 0)
        self._goal_q_matrix = np.full((2 ** AMOUNT_IMAGE_SPLITS, AMOUNT_ACTIONS), 0)

    def run(self):
        while True:
            self._do_action(action=Actions.STRAIGHT)
            time.sleep(1)
        # self._food_q_matrix = np.load('food_matrices/food_q_matrix_final.npy')
        # self._goal_q_matrix = np.load('goal_matrices/goal_q_matrix_final.npy')
        #
        # # Collect food first
        # task = Task.COLLECT_FOOD
        # q_matrix_in_use = self._food_q_matrix
        # while True:
        #     current_state_index = self._get_current_state_index(task)
        #     print(f"State: {current_state_index}")
        #     action_index = np.argmax(q_matrix_in_use[current_state_index])
        #     next_action = Actions(action_index)
        #     print(f"Action: {next_action}")
        #     self._do_action(action=next_action)
        #     if self._collected_food():
        #         # Next move food to goal
        #         q_matrix_in_use = self._goal_q_matrix
        #         task = Task.REACH_GOAL

    def train(self, task: Task, iterations: int = 1000):
        print("Started training...")
        print(f"Task: {task}")

        if task == Task.COLLECT_FOOD:
            self._q_matrix = self._food_q_matrix
            save_position = "food_matrices"
        else:
            self._q_matrix = self._goal_q_matrix
            save_position = "goal_matrices"

        current_state_index = self._get_current_state_index(task)
        count = 0
        reached_goal = False
        for i in range(iterations):
            count += 1
            eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * i / EPS_DECAY)
            if random.random() < eps_threshold:
                next_action = random.choice(list(Actions))
                action_index = next_action.value
            else:
                action_index = np.argmax(self._q_matrix[current_state_index])
                next_action = Actions(action_index)
            if i % 10 == 0:
                print(f"Iteration {i + 1}/{iterations}")
                print(f"Current Epsilon: {eps_threshold}")
            self._do_action(action=next_action)
            reward = self._calculate_reward(task)
            next_state_index = self._get_current_state_index(task)
            self._update_state_value(state_idx=current_state_index, next_state_idx=next_state_index,
                                     action_idx=action_index,
                                     reward=reward)
            current_state_index = next_state_index
            if i % 1000 == 0:
                np.save(f"{save_position}/q_matrix_new_{i}.npy", self._q_matrix)
                np.savetxt(f"{save_position}/q_matrix_new_{i}", self._q_matrix)

            if task == Task.COLLECT_FOOD:
                center_sensor_value = self._rob.read_irs()[5]
                reached_goal = center_sensor_value < 0.03 if center_sensor_value else False
            else:
                reached_goal = False
            # Reset if goal is reached
            if reached_goal or count % 1000 == 0:  #
                count = 0
                self._rob.stop_world()
                print("Waiting for stop")
                self._rob.wait_for_stop()
                print("Stopped!")
                self._rob.play_simulation()
                print("Continue with simulation!")
                self._rob.set_phone_tilt(PHONE_TILT, 100)
                current_state_index = self._get_current_state_index(task)
        np.save(f"{save_position}/q_matrix_new_final.npy", self._q_matrix)
        np.savetxt(f"{save_position}/q_matrix_new_final", self._q_matrix)

    def _collected_food(self):
        center_sensor_value = self._rob.read_irs()[5]
        return center_sensor_value < 0.03

    def _update_state_value(self, state_idx: int, next_state_idx: int, action_idx: int, reward: int) -> None:
        old_value = self._q_matrix[state_idx][action_idx]
        next_q_value = np.amax(self._q_matrix[next_state_idx], axis=0)

        updated_value = old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_q_value - old_value)
        self._q_matrix[state_idx, action_idx] = updated_value

    def _calculate_reward(self, task: Task) -> int:
        if task == Task.COLLECT_FOOD:
            center_sensor_value = self._rob.read_irs()[5]
            if center_sensor_value < 0.03:
                return 30
        else:
            return -1
        return -1

    def _do_action(self, action: Actions):
        movement = actions_movement_mapping[action]
        self._rob.move(
            left=movement.l_speed,
            right=movement.r_speed,
            millis=movement.duration
        )

    def _get_current_state_index(self, task: Task):
        # Make picture
        image = self._rob.get_image_front()
        # Get detection results
        detection_results = ObjectDetector.detect_objects(image, task)
        for result in detection_results:
            if result:
                print("DETECT | ", end='')
            else:
                print("______ | ", end='')
        print("")
        # Convert to string and transform base two to base ten for state index
        base_two_val = ''.join([str(int(x)) for x in detection_results])
        state_idx = int(base_two_val, 2)
        return state_idx
