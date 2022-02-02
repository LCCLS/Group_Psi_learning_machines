from dataclasses import dataclass
from enum import Enum


class Task(Enum):
    COLLECT_FOOD = 0
    REACH_GOAL = 1


@dataclass
class Movement:
    l_speed: int
    r_speed: int
    duration: int


class Actions(Enum):
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2
    # STRONG_LEFT = 3
    # STRONG_RIGHT = 4


actions_movement_mapping = {
    Actions.STRAIGHT: Movement(15, 15, 1000),
    Actions.LEFT: Movement(-4, 4, 1000),
    Actions.RIGHT: Movement(4, -4, 1000),
    # Actions.STRONG_LEFT: Movement(-10, 10, 1000),
    # Actions.STRONG_RIGHT: Movement(10, -10, 1000)
}
