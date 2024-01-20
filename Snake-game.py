import turtle
import time
import random

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake class
class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.direction = "Right"

    def create_snake(self):
        for i in range(3):
            self.add_segment(-20 * i, 0)

    def add_segment(self, x, y):
        segment = turtle.Turtle()
        segment.shape("square")
        segment.color("white")
        segment.penup()
        segment.goto(x, y)
        self.segments.append(segment)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        if self.direction == "Up":
            self.head.sety(self.head.ycor() + 20)
        elif self.direction == "Down":
            self.head.sety(self.head.ycor() - 20)
        elif self.direction == "Left":
            self.head.setx(self.head.xcor() - 20)
        elif self.direction == "Right":
            self.head.setx(self.head.xcor() + 20)

    def change_direction(self, new_direction):
        if (
            (new_direction == "Up" and not self.direction == "Down")
            or (new_direction == "Down" and not self.direction == "Up")
            or (new_direction == "Left" and not self.direction == "Right")
            or (new_direction == "Right" and not self.direction == "Left")
        ):
            self.direction = new_direction

# Food class
class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("red")
        self.food.shapesize(stretch_wid=0.7, stretch_len=0.7)
        self.food.penup()
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.food.goto(x, y)

# Score class
class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.speeds = {"slow": 0.2, "medium": 0.1, "fast": 0.05}
        self.current_speed = "medium"
        self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.goto(0, 260)

    def update_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score

    def reset_score(self):
        self.score = 0

    def display_score(self):
        self.score_pen.clear()
        self.score_pen.write(
            f"Score: {self.score}  High Score: {self.high_score}",
            align="center",
            font=("Courier", 24, "normal"),
        )

# Game speed class
class GameSpeed:
    def __init__(self, score):
        self.score = score

    def increase_speed(self):
        if self.score.score % 5 == 0 and self.score.score != 0:
            self.score.current_speed = "fast"
        elif self.score.score % 3 == 0 and self.score.score != 0:
            self.score.current_speed = "medium"
        else:
            self.score.current_speed = "slow"

# Game Over class
class GameOver:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 0)

    def show_message(self, message):
        self.pen.clear()
        self.pen.write(
            message,
            align="center",
            font=("Courier", 24, "normal"),
        )
        time.sleep(1)

# Initialize game objects
snake = Snake()
food = Food()
score = Score()
game_speed = GameSpeed(score)
game_over = GameOver()

# Keyboard bindings
wn.listen()
wn.onkey(lambda: snake.change_direction("Up"), "Up")
wn.onkey(lambda: snake.change_direction("Down"), "Down")
wn.onkey(lambda: snake.change_direction("Left"), "Left")
wn.onkey(lambda: snake.change_direction("Right"), "Right")

# Main game loop
while True:
    wn.update()

    # Check for collision with food
    if snake.head.distance(food.food) < 15:
        food.spawn_food()
        snake.add_segment(snake.segments[-1].xcor(), snake.segments[-1].ycor())
        score.update_score()
        print("Yummy!")  # Added "Yummy!" print statement

    # Move the snake
    snake.move()

    # Check for collision with walls
    if (
        snake.head.xcor() > 290
        or snake.head.xcor() < -290
        or snake.head.ycor() > 290
        or snake.head.ycor() < -290
    ):
        game_over.show_message("Game Over\nPress 'R' to Restart or 'Q' to Quit")
        response = wn.textinput("Game Over", "Press 'R' to Restart or 'Q' to Quit")
        if response and response.lower() == "r":
            for segment in snake.segments:
                segment.goto(1000, 1000)
            snake.segments.clear()
            snake.create_snake()
            snake.head = snake.segments[0]
            snake.direction = "Right"
            score.reset_score()
            game_speed = GameSpeed(score)  # Reset game speed

    # Check for collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_over.show_message("Game Over\nPress 'R' to Restart or 'Q' to Quit")
            response = wn.textinput("Game Over", "Press 'R' to Restart or 'Q' to Quit")
            if response and response.lower() == "r":
                for segment in snake.segments:
                    segment.goto(1000, 1000)
                snake.segments.clear()
                snake.create_snake()
                snake.head = snake.segments[0]
                snake.direction = "Right"
                score.reset_score()
                game_speed = GameSpeed(score)  # Reset game speed

    # Display score
    score.display_score()

    # Check for
    game_speed.increase_speed()  # Moved this line outside of the Game Over check
    time.sleep(score.speeds[score.current_speed])
