#! /usr/bin/env python3

from Environment import Environment
import argparse
import pygame
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
        default=1,
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
    if args.load:
        agent.load_q_table(args.load)
    if args.dontlearn:
        agent.exploration_rate = 0.01

    max_length, max_duration = 0, 0
    for session in tqdm(range(args.sessions)):
        environment = Environment(size=args.size)
        state = State(environment)
        duration = 0
        if args.visual:
            # Pygame visualization
            pygame.init()
            board_w = environment.board.width
            board_h = environment.board.height

            # Compute cell size and window size
            base_win = 600
            cell_size = max(8, min(48, base_win // max(board_w, board_h)))
            win_w = cell_size * board_w
            win_h = cell_size * board_h + 40  # extra for info bar

            screen = pygame.display.set_mode((win_w, win_h))
            pygame.display.set_caption(f"Snake Game - Session {session + 1}")
            font = pygame.font.SysFont(None, 20)

            refresh_rate = 100  # milliseconds per frame
            game_running = True

            # Colors
            BLACK = (0, 0, 0)
            RED = (255, 0, 0)
            GREEN = (0, 200, 0)
            BLUE = (0, 0, 200)
            YELLOW = (255, 255, 0)
            GRID_COLOR = (30, 30, 30)
            INFO_BG = (20, 20, 20)
            INFO_TEXT = (220, 220, 220)

            while game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        args.visual = False
                    elif event.type == pygame.KEYDOWN:
                        # '+' to decrease delay (faster),
                        # '-' to increase delay (slower)
                        if event.key in (
                             pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                            refresh_rate = max(10, refresh_rate - 10)
                        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            refresh_rate = min(1000, refresh_rate + 10)
                # Clear screen
                screen.fill(BLACK)

                # Draw grid (optional subtle lines)
                for x in range(board_w):
                    for y in range(board_h):
                        rect = pygame.Rect(x * cell_size,
                                           y * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, GRID_COLOR, rect, 1)

                # Draw red apple
                try:
                    ra = environment.board.red_apple
                    ra_row = ra[1]
                    ra_col = ra[0]
                    rect = pygame.Rect(
                         ra_col * cell_size,
                         ra_row * cell_size,
                         cell_size, cell_size)
                    pygame.draw.rect(screen, RED, rect)
                except Exception:
                    pass

                # Draw green apples
                try:
                    for apple in environment.board.green_apples:
                        a_row = apple[1]
                        a_col = apple[0]
                        rect = pygame.Rect(
                            a_col * cell_size,
                            a_row * cell_size,
                            cell_size, cell_size)
                        pygame.draw.rect(screen, GREEN, rect)
                except Exception:
                    pass

                # Draw snake
                try:
                    for idx, snake_part in enumerate(environment.snake.body):
                        part_row = snake_part[1]
                        part_col = snake_part[0]
                        rect = pygame.Rect(
                            part_col * cell_size,
                            part_row * cell_size,
                            cell_size, cell_size)
                        color = YELLOW if idx == 0 else BLUE
                        pygame.draw.rect(screen, color, rect)
                except Exception:
                    pass

                # Info bar
                info_rect = pygame.Rect(0, board_h * cell_size, win_w, 40)
                pygame.draw.rect(screen, INFO_BG, info_rect)
                info_text = f"Session {session + 1}  |  " \
                    f"Refresh {refresh_rate} ms  |  " \
                    f"Score {len(environment.snake.body)}  |  " \
                    f"Press +/- to change speed"
                img = font.render(info_text, True, INFO_TEXT)
                screen.blit(img, (6, board_h * cell_size + 10))

                pygame.display.flip()

                # Agent action and environment update
                action = agent.choose_action(state)
                try:
                    reward = environment.execute_action(action)
                    if not args.dontlearn:
                        next_state = State(environment)
                        agent.update_q_value(state, action, reward, next_state)
                        agent.exploration_rate = max(
                            0.01, agent.exploration_rate * 0.99)
                    state.update(environment)
                except Exception:
                    agent.update_q_value(state, action, -42, None)
                    game_running = False
                    try:
                        pygame.quit()
                    except Exception:
                        pass
                    break

                duration += 1
                pygame.time.delay(refresh_rate)

            # Ensure pygame is cleaned up
            try:
                pygame.quit()
            except Exception:
                pass

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
                        agent.exploration_rate = max(
                            0.01, agent.exploration_rate * 0.995)
                    state.update(environment)
                except Exception:
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
        print(
            f"Game over, max length = {max_length}, "
            f"max duration = {max_duration}")
        print("\nFinal results:")
        for session_num, score in results[-10:]:
            print(f"Session {session_num}: score {score}")


if __name__ == "__main__":
    main()
