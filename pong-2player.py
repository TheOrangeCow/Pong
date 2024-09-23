import tkinter as tk
import random

WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 15
PADDLE_SPEED = 10
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

class Pong(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.paddle1 = self.canvas.create_rectangle(50, 150, 50 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT, fill="white")
        self.paddle2 = self.canvas.create_rectangle(550, 150, 550 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT, fill="white")

        self.ball = self.canvas.create_oval(300, 200, 300 + BALL_SIZE, 200 + BALL_SIZE, fill="white")

        self.ball_speed_x = BALL_SPEED_X
        self.ball_speed_y = BALL_SPEED_Y

        self.bind("<KeyPress>", self.on_key_press)

        self.score1 = 0
        self.score2 = 0

        self.score_display1 = self.canvas.create_text(100, 50, text="Player 1: 0", fill="white", font=("Helvetica", 16))
        self.score_display2 = self.canvas.create_text(500, 50, text="Player 2: 0", fill="white", font=("Helvetica", 16))

        self.after(20, self.update)

    def on_key_press(self, event):
        if event.keysym == "w":
            self.move_paddle(self.paddle1, -PADDLE_SPEED)
        elif event.keysym == "s":
            self.move_paddle(self.paddle1, PADDLE_SPEED)
        elif event.keysym == "Up":
            self.move_paddle(self.paddle2, -PADDLE_SPEED)
        elif event.keysym == "Down":
            self.move_paddle(self.paddle2, PADDLE_SPEED)

    def move_paddle(self, paddle, dy):
        coords = self.canvas.coords(paddle)
        if coords[1] + dy >= 0 and coords[3] + dy <= HEIGHT:
            self.canvas.move(paddle, 0, dy)

    def update(self):
        ball_coords = self.canvas.coords(self.ball)
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
            self.ball_speed_y *= -1

        if ball_coords[0] <= 0:
            self.score2 += 1
            self.canvas.itemconfig(self.score_display2, text="Player 2: " + str(self.score2))
            self.reset_ball()
        elif ball_coords[2] >= WIDTH:
            self.score1 += 1
            self.canvas.itemconfig(self.score_display1, text="Player 1: " + str(self.score1))
            self.reset_ball()

        if ball_coords[0] <= paddle1_coords[2] and paddle1_coords[1] <= ball_coords[1] <= paddle1_coords[3]:
            self.ball_speed_x *= -1
        elif ball_coords[2] >= paddle2_coords[0] and paddle2_coords[1] <= ball_coords[1] <= paddle2_coords[3]:
            self.ball_speed_x *= -1

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        self.after(20, self.update)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH/2 - BALL_SIZE/2, HEIGHT/2 - BALL_SIZE/2,
                           WIDTH/2 + BALL_SIZE/2, HEIGHT/2 + BALL_SIZE/2)
        self.ball_speed_x = BALL_SPEED_X if random.randint(0, 1) == 0 else -BALL_SPEED_X
        self.ball_speed_y = BALL_SPEED_Y if random.randint(0, 1) == 0 else -BALL_SPEED_Y



pong = Pong()
pong.title("Pong")
pong.mainloop()

