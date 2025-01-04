# Flappy Bird with Hand Gesture Control

This project implements a simple version of the classic Flappy Bird game using Pygame, where the player controls the bird's movement with hand gestures. The game utilizes OpenCV and MediaPipe to track hand gestures, allowing players to "flap" the bird by closing their fist.

## Features

- **Flappy Bird Gameplay**: The player controls the bird by making a fist to flap and avoiding obstacles (pipes).
- **Hand Gesture Control**: The bird flaps when the player makes a fist with their hand, using a webcam to track the hand.
- **Pipe Generation**: Pipes are randomly generated and move from right to left. The player must navigate the bird through the gaps in the pipes.
- **Score System**: Points are earned for successfully passing through each set of pipes.
- **Game Over Screen**: The game ends when the bird collides with a pipe or the ground. Players can restart the game or quit.

## Requirements

To run this game, you need to have the following libraries installed:

- **Pygame**: For game development.
- **OpenCV**: For accessing the webcam and handling video frames.
- **MediaPipe**: For hand tracking.

You can install the required libraries by running:

```bash
pip install pygame opencv-python mediapipe
```
# Setup

Clone this repository:

```bash
git clone https://github.com/your-username/flappy-bird-hand-gesture.git
cd flappy-bird-hand-gesture
```

The game will open in a window and use your webcam to track your hand gestures. To play:

- **Close your fist** to make the bird flap and move upwards.
- The bird will fall due to gravity if no gesture is detected.
- **Avoid colliding with pipes** by moving the bird through the gaps.

## Controls

- **Fist Gesture**: Make a fist to make the bird flap upwards.
- **'Space'**: Start the game.
- **'R'**: Restart the game after it ends.
- **'Q'**: Quit the game.

## Code Explanation

- **Main Game Loop**: The main game loop runs continuously, updating the bird's position and checking for collisions with pipes. Hand gestures are detected using the webcam, and the bird's velocity is adjusted accordingly.
- **Hand Gesture Detection**: The webcam feed is processed using OpenCV and MediaPipe to detect hand landmarks. If a fist gesture is detected (fingers curled towards the palm), the bird flaps.
- **Collision Detection**: If the bird collides with a pipe or the ground, the game ends, and a game over screen is displayed.
- **Pipe Movement**: Pipes move leftward and are recreated once they go off-screen to keep the game challenging.

## Screenshots

### Gameplay Screenshot:
![Gameplay Screenshot](path/to/gameplay_screenshot.png)

### Hand Tracking Window:
![Hand Tracking Window](path/to/hand_tracking_window.png)

## Troubleshooting

- **No webcam detected**: Ensure that your webcam is properly connected and accessible.
- **Hand gestures not detected**: Ensure good lighting and a clear view of your hands in the webcam frame.
- **Performance issues**: Lower the frame rate by adjusting the clock.tick() value in the main game loop if necessary.
