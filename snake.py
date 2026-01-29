#! /usr/bin/env python3

from Environment import Environment
import argparse
import tkinter as tk
from tqdm import tqdm
from Agent import Agent
from State import State
	

def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Snake Game with Q-learning AI training"
	)
	
	parser.add_argument(
		'-sessions',
		type=int,
		default=100,
		help='Number of training sessions (default: 100)'
	)
	
	parser.add_argument(
		'-save',
		type=str,
		default=None,
		help='File path to save the Q-table'
	)
	
	parser.add_argument(
		'-visual',
		action='store_true',
		default=False,
		help='Enable visualization during training'
	)
	
	parser.add_argument(
		'-dontlearn',
		action='store_true',
		help='Skip the training phase'
	)
	
	parser.add_argument(
		'-load',
		type=str,
		default=None,
		help='Path to trained model file to load'
	)

	parser.add_argument(
		'-size',
		type=int,
		default=10,
		help='Size of the game board (default: 10x10)'
	)
	
	return parser.parse_args()

def main():
	args = parse_arguments()
	agent = Agent()

	for session in tqdm(range(args.sessions)):
		environment = Environment()
		state = State(environment)
		if args.visual:
			root = tk.Tk()
			root.title(f"Snake Game - Session {session + 1}")
			
			# Create a dictionary to store cell widgets for easy updates
			cells = {}
			
			# Initialize the grid with all cells
			for row in range(environment.board.height):
				for col in range(environment.board.width):
					cell = tk.Label(root, width=6, height=3, borderwidth=1, relief="sunken", bg="white")
					cell.grid(row=row, column=col)
					cells[(row, col)] = cell
			
			# Handle window close button
			def on_closing():
				nonlocal game_running
				game_running = False
				args.visual = False
				root.quit()
				root.destroy()
			root.protocol("WM_DELETE_WINDOW", on_closing)
			
			game_running = True
			def update_display():
				nonlocal game_running

				if not game_running:
					root.quit()
					return
				
				# Reset all cells to white
				for cell in cells.values():
					cell.config(bg="gray")
				
				# Draw red apple
				red_cell = cells[(environment.board.red_apple[1], environment.board.red_apple[0])]
				red_cell.config(bg="red")
				
				# Draw green apples
				for apple in environment.board.green_apples:
					green_cell = cells[(apple[1], apple[0])]
					green_cell.config(bg="green")
				
				# Draw snake
				for snake_part in environment.snake.body:
					snake_cell = cells[(snake_part[1], snake_part[0])]
					snake_cell.config(bg="blue" if snake_part != environment.snake.body[0] else "yellow")
				
				action = agent.choose_action(state)
				try:
					reward = environment.execute_action(action)
					next_state = State(environment)
					agent.update_q_value(state, action, reward, next_state)
					state.update(environment)
					agent.exploration_rate = max(0.01, agent.exploration_rate * 0.995)
				except Exception as e:
					agent.update_q_value(state, action, -42, None)
					game_running = False
					root.quit()
					root.destroy()
					return

				root.after(500, update_display)  # Update every 500ms
			
			update_display()
			root.mainloop()
		else:
			# Non-visual mode: simple game loop without display
			game_running = True
			while game_running:
				action = agent.choose_action(state)
				try:
					reward = environment.execute_action(action)
					next_state = State(environment)
					agent.update_q_value(state, action, reward, next_state)
					state.update(environment)
					agent.exploration_rate = max(0.01, agent.exploration_rate * 0.995)
				except:
					agent.update_q_value(state, action, -42, None)
					game_running = False
	if args.save:
		agent.save_q_table(args.save)

if __name__ == "__main__":
	main()
