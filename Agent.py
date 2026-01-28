import numpy as np
from Action import Action
from State import State

class Agent:
	def __init__(self):
		pass

	def choose_action(self, state: State) -> Action:
		"""
		Choose an action based on the current state.
		
		Args:
			snake: The current snake object.
		"""
		# Return a random action but it could not be the opposite of the current direction
		possible_actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
		match state.direction:
			case "UP":
				possible_actions.remove(Action.DOWN)
			case "DOWN":
				possible_actions.remove(Action.UP)
			case "LEFT":
				possible_actions.remove(Action.RIGHT)
			case "RIGHT":
				possible_actions.remove(Action.LEFT)
		return np.random.choice(possible_actions)
