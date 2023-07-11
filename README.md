20201082 박현빈 final project.

## description of my application.

This application is a game developed with the Pygame library in Python. In this game, a ball bounces around the screen and interacts with various objects. The player controls two paddles to direct the ball and earns points by colliding with different obstacles.

Components and Mechanics
The Ball

The ball is represented by a circle on the screen, and its movement is governed by a velocity vector vxy and an acceleration vector axy. The acceleration vector simulates the effect of gravity and is applied to the velocity vector on every frame. The ball bounces off the walls of the game window and the various obstacles.

Paddles

Two paddles are located at the bottom of the screen. The player can move these paddles up and down by pressing the left and right arrow keys respectively. These paddles are used to redirect the ball's trajectory.

Obstacles

There are various obstacles scattered around the screen. These include static circles, rectangles, and triangles. When the ball collides with an obstacle, the ball's velocity vector is updated to make the ball bounce away. Each type of obstacle also gives different amounts of points when hit.

Score

The player's score is displayed at the top of the screen. The score increases when the ball collides with an obstacle. Different obstacles provide different amounts of points. Sound effects play when the ball collides with an obstacle or when the player's score reaches a certain threshold.

Collision Detection

The game includes advanced collision detection between the ball and the various obstacles:

Circle Collision: The distance between the center of the ball and the center of the obstacle is calculated. If the distance is less than the sum of the radii of the ball and the obstacle, a collision has occurred.
Rectangle Collision: The game calculates the closest point on the rectangle to the ball, then determines if a collision has occurred based on the distance from this point to the ball.
Triangle Collision: The ball's position is projected onto the axes of the triangle. A collision is registered if the ball falls within the triangle's range on all axes.
Requirements
To run this game, Python and the Pygame library must be installed on your machine. You also need to ensure the sound and image files used in the game are in the correct locations.

## description of files on Github repo.

final_1.py : This is the python file that contaions application. If you run this file, you can enjoy my application.

1.png : Background screen image file.

impressive.wav / collide.wav / gameover.wav : Sound files.
