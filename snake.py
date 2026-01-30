#! /usr/bin/env python3

from time import sleep
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
	results = []
	initial_visual = args.visual
	if args.load:
		agent.load_q_table(args.load)

	max_length, max_duration = 0, 0
	for session in tqdm(range(args.sessions)):
		environment = Environment(size=args.size)
		state = State(environment)
		duration = 0
		if args.visual:
			refresh_rate = 100
			root = tk.Tk()
			root.title(f"Snake Game - Session {session + 1}")
			w = tk.Scale(root, from_=10, to=500, label="Refresh Rate (ms)", orient=tk.HORIZONTAL)
			w.set(refresh_rate)
			w.grid(row=environment.board.height, column=0, columnspan=environment.board.width, sticky="ew")
			
			# Create a dictionary to store cell widgets for easy updates
			cells = {}
			# Initialize the grid with all cells
			for row in range(environment.board.height):
				for col in range(environment.board.width):
					cell = tk.Label(root, width=6, height=3, borderwidth=1, relief="sunken", bg="black")
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
					cell.config(bg="black")
				
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
					if not args.dontlearn:
						next_state = State(environment)
						agent.update_q_value(state, action, reward, next_state)
						agent.exploration_rate = max(0.01, agent.exploration_rate * 0.99)
					state.update(environment)
				except:
					agent.update_q_value(state, action, -42, None)
					game_running = False
					root.quit()
					root.destroy()
					return
				nonlocal duration
				duration += 1

				root.after(w.get(), update_display)  # Update with slider-controlled interval
			
			update_display()
			root.mainloop()
		else:
			# Non-visual mode: simple game loop without display
			game_running = True
			while game_running:
				action = agent.choose_action(state)
				try:
					reward = environment.execute_action(action)
					if not args.dontlearn:
						next_state = State(environment)
						agent.update_q_value(state, action, reward, next_state)
						agent.exploration_rate = max(0.01, agent.exploration_rate * 0.995)
					state.update(environment)
				except:
					agent.update_q_value(state, action, -42, None)
					game_running = False
				duration += 1
		if len(environment.snake.body) > max_length:
			max_length = len(environment.snake.body)
		if duration > max_duration:
			max_duration = duration
		session_score = len(environment.snake.body)
		results.append((session + 1, session_score))
	if args.save:
		agent.save_q_table(args.save)

	if results:
		if initial_visual:
			results_root = tk.Tk()
			results_root.title("Training Results")
			text = tk.Text(results_root, width=40, height=20)
			text.pack(fill="both", expand=True)
			text.insert("end", f"Game over, max length = {max_length}, max duration = {max_duration}\n\nFinal results:\n")
			for session_num, score in results[-10:]:
				text.insert("end", f"Session {session_num}: score {score}\n")
			text.config(state="disabled")
			results_root.mainloop()
		else:
			print(f"Game over, max length = {max_length}, max duration = {max_duration}")
			print("\nFinal results:")
			for session_num, score in results[-10:]:
				print(f"Session {session_num}: score {score}")

if __name__ == "__main__":
	main()
