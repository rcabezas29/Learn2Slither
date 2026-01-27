import random

class State:
	def __init__(self):
		pass

class Snake:
	def __init__(self, length: int = 3, position: tuple = (0, 0), board_width: int = 10, board_height: int = 10):
		"""
		Initialize a snake with a given length and starting position.
		The snake body is represented as a list of positions, starting from the head.
		All segments are placed contiguously and within board bounds.
		
		Args:
			length: Length of the snake (default 3)
			position: Head position as a tuple (x, y)
			board_width: Width of the game board (default 10)
			board_height: Height of the game board (default 10)
		"""
		
		self.length = length
		self.board_width = board_width
		self.board_height = board_height
		
		# Generate random direction for body extension (up, down, left, right)
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		direction = random.choice(directions)
		
		# Keep trying until we find a valid placement
		valid_placement = False
		while not valid_placement:
			self.body = [position]
			valid_placement = True
			
			# Add remaining segments contiguously
			for i in range(1, length):
				next_x = position[0] + direction[0] * i
				next_y = position[1] + direction[1] * i
				
				# Check if segment is within bounds
				if next_x < 0 or next_x >= board_width or next_y < 0 or next_y >= board_height:
					valid_placement = False
					# Try a new direction
					direction = random.choice(directions)
					break
				
				self.body.append((next_x, next_y))

		self.state = State()
	
	def update_position(self, new_head_position: tuple):
		"""
		Update the snake's position by moving the head to a new position
		and shifting the body segments accordingly.
		
		Args:
			new_head_position: New position for the snake's head as a tuple (x, y)
		"""
		
		# Insert new head position at the front of the body list
		self.body.insert(0, new_head_position)
		# Remove the last segment to maintain length
		self.body.pop()
