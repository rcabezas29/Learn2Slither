#! /usr/bin/env python3

from Environment import Environment
import argparse
import tkinter as tk
from tqdm import tqdm
from Agent import Action
import numpy as np

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

	for session in tqdm(range(args.sessions)):
		environment = Environment()
		snake = environment.snake
		board = environment.board
		
		if args.visual:
			root = tk.Tk()
			root.title(f"Snake Game - Session {session + 1}")
			
			# Create a dictionary to store cell widgets for easy updates
			cells = {}
			
			# Initialize the grid with all cells
			for row in range(board.height):
				for col in range(board.width):
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
				red_cell = cells[(board.red_apple[1], board.red_apple[0])]
				red_cell.config(bg="red")
				
				# Draw green apples
				for apple in board.green_apples:
					green_cell = cells[(apple[1], apple[0])]
					green_cell.config(bg="green")
				
				# Draw snake
				for snake_part in snake.body:
					snake_cell = cells[(snake_part[1], snake_part[0])]
					snake_cell.config(bg="blue" if snake_part != snake.body[0] else "yellow")
				
				# Move snake with random action
				action = np.random.choice(list(Action))
				try:
					environment.execute_action(action)
				except:
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
				try:
					action = np.random.choice(list(Action))
					environment.execute_action(action)
				except:
					game_running = False

if __name__ == "__main__":
	main()
