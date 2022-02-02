import argparse

parser = argparse.ArgumentParser(description='Run Robobo')

parser.add_argument('-s', '--simulated', help='Run Robobo in the simulator', action='store_false')
parser.add_argument('-d', '--debug', help='Run in debug mode', action='store_true')
parser.add_argument('-t', '--train', help='Train using epsilon greedy', action='store_false')

FLAGS = parser.parse_args()



