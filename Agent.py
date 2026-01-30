import numpy as np
from Action import Action
from State import State
import json

class Agent:
    def __init__(self):
        # Q-table: {state_tuple: np.array([q_up, q_down, q_left, q_right])}
        self.q_table = {}
        self.learning_rate = 0.35
        self.discount_factor = 0.95
        self.exploration_rate = 1.0

    def _state_key(self, state: State):
        """
        Return a hashable state key for the Q-table.
        """
        key = []
        for direction in ["UP", "LEFT", "DOWN", "RIGHT"]:
            i = 0
            while (state.observations[direction][i] == '0'):
                i += 1
            if (state.observations[direction][i] == 'W') or (state.observations[direction][i] == 'S'):
                if i == 0:
                    key.append("DEATH_NEAR")
                elif 1 <= i <= 2:
                    key.append("DEATH_MID")
                else:
                    key.append("DEATH_FAR")
            elif (state.observations[direction][i] == 'G'):
                if i == 0:
                    key.append("GREEN_NEAR")
                elif 1 <= i <= 2:
                    key.append("GREEN_MID")
                else:
                    key.append("GREEN_FAR")
            elif (state.observations[direction][i] == 'R'):
                if i == 0:
                    key.append("RED_NEAR")
                elif 1 <= i <= 2:
                    key.append("RED_MID")
                else:
                    key.append("RED_FAR")
        return tuple(key)

    def _ensure_state(self, state: State):
        """
        Ensure the Q-table has an entry for this state.
        """
        key = self._state_key(state)
        if key not in self.q_table:
            self.q_table[key] = np.zeros(len(Action))
        return key

    def choose_action(self, state: State) -> Action:
        """
        Choose an action based on the current state.
        
        Args:
            state: The current state object.
        """
        state_key = self._ensure_state(state)
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

        if np.random.rand() < self.exploration_rate:
            return np.random.choice(possible_actions)
        else:
            q_values = self.q_table[state_key].copy()
            # Mask invalid actions
            invalid_actions = [a for a in Action if a not in possible_actions]
            for action in invalid_actions:
                q_values[action.value] = -np.inf
            best_value = np.max(q_values)
            best_actions = [a for a in possible_actions if q_values[a.value] == best_value]
            return np.random.choice(best_actions)

    def update_q_value(self, state: State, action: Action, reward: int, next_state: State):
        """
        Update the Q-value for a given state and action.
        
        Args:
            state: The current state object.
            action: The action taken.
            reward: The reward received after taking the action.
            next_state: The resulting state after taking the action.
        """
        state_key = self._ensure_state(state)
        if next_state is None:
            self.q_table[state_key][action.value] = reward
            return
        next_state_key = self._ensure_state(next_state)

        best_next_q = np.max(self.q_table[next_state_key])
        td_target = reward + self.discount_factor * best_next_q
        td_delta = td_target - self.q_table[state_key][action.value]
        self.q_table[state_key][action.value] += self.learning_rate * td_delta

    def save_q_table(self, filename: str):
        """
        Save the Q-table to a file.
        
        Args:
            filename: The file path to save the Q-table.
        """
        with open(filename, 'w') as f:
            json.dump(
                {str(k): v.tolist() for k, v in self.q_table.items()},
                f,
                indent=2,
                sort_keys=True
            )

    def load_q_table(self, filename: str):
        """
        Load the Q-table from a file.
        
        Args:
            filename: The file path to load the Q-table from.
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            self.q_table = {eval(k): np.array(v) for k, v in data.items()}
        self.exploration_rate = 0.01
