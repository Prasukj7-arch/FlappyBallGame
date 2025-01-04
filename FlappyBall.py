import pygame
import random
import cv2
import mediapipe as mp
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game variables
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.3  # Reduced gravity for easier control
flap_strength = -10
pipe_width = 50
pipe_gap = 200  # Increased gap for easier passage
pipe_velocity = 4  # Slower pipe movement
pipes = [{'x': WIDTH, 'y': random.randint(pipe_gap, HEIGHT - pipe_gap)}]
score = 0

# Initialize Pygame clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

# Initialize camera
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Game state variables
initial_hand_y = None


def draw_bird(screen, x, y):
    pygame.draw.circle(screen, BLUE, (x, y), 20)


def draw_pipes(screen, pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['y'] - pipe_gap // 2))  # Top pipe
        pygame.draw.rect(screen, GREEN, (
        pipe['x'], pipe['y'] + pipe_gap // 2, pipe_width, HEIGHT - pipe['y'] - pipe_gap // 2))  # Bottom pipe


def display_score(screen, score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


def is_collision(bird_x, bird_y, pipes):
    if bird_y <= 0 or bird_y >= HEIGHT:
        return True
    for pipe in pipes:
        if bird_x + 20 > pipe['x'] and bird_x - 20 < pipe['x'] + pipe_width:
            if bird_y - 20 < pipe['y'] - pipe_gap // 2 or bird_y + 20 > pipe['y'] + pipe_gap // 2:
                return True
    return False


def show_start_screen():
    screen.fill(WHITE)
    start_text = font.render("Press 'Space' to Start", True, BLACK)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_rect.topleft)
    pygame.display.flip()


def show_game_over_screen():
    screen.fill(WHITE)

    # Render game over text
    game_over_text = font.render("Game Over!", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(game_over_text, game_over_rect.topleft)

    # Render restart/quit instructions
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_rect.topleft)

    pygame.display.flip()


def reset_game():
    global bird_y, bird_velocity, pipes, score, initial_hand_y
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [{'x': WIDTH, 'y': random.randint(pipe_gap, HEIGHT - pipe_gap)}]
    score = 0
    initial_hand_y = None  # Reset the hand position


def is_fist_closed(hand_landmarks):
    # Get fingertip landmarks (thumb, index, middle, ring, pinky)
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]

    # Get palm landmarks (base of fingers)
    palm_center = hand_landmarks.landmark[9]

    # Check if fingertips are closer to palm center (indicating a fist)
    if (thumb_tip.y > palm_center.y and
            index_tip.y > palm_center.y and
            middle_tip.y > palm_center.y and
            ring_tip.y > palm_center.y and
            pinky_tip.y > palm_center.y):
        return True
    return False


def main():
    global bird_y, bird_velocity, pipes, score, initial_hand_y

    # Show start screen and wait for 'Space' key press
    show_start_screen()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space key to start the game
                    waiting = False

    running = True
    while running:
        # Read camera frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand tracking
        hand_up = False
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Check for fist gesture
                if is_fist_closed(hand_landmarks):
                    hand_up = True  # Fist is closed, bird should flap

                # Draw hand landmarks on the camera frame
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Update game logic
        if hand_up:
            bird_velocity = flap_strength
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipes
        for pipe in pipes:
            pipe['x'] -= pipe_velocity
        if pipes[0]['x'] + pipe_width < 0:
            pipes.pop(0)
            pipes.append({'x': WIDTH, 'y': random.randint(pipe_gap, HEIGHT - pipe_gap)})
            score += 1

        # Collision check
        if is_collision(bird_x, bird_y, pipes):
            show_game_over_screen()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # 'R' to restart
                            reset_game()  # Reset game state
                            main()  # Restart the game
                        elif event.key == pygame.K_q:  # 'Q' to quit
                            pygame.quit()
                            sys.exit()

        # Draw everything
        screen.fill(WHITE)
        draw_bird(screen, bird_x, bird_y)
        draw_pipes(screen, pipes)
        display_score(screen, score)
        pygame.display.flip()

        # Show the hand tracking feed in a separate window
        cv2.imshow("Hand Tracking", frame)

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cap frame rate
        clock.tick(30)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
