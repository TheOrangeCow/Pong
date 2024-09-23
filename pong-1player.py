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
        global difficulty_level, Pong, root
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
        global difficulty_level, Pong, root
        if event.keysym == "w":
            self.move_paddle(self.paddle1, -PADDLE_SPEED)
        elif event.keysym == "s":
            self.move_paddle(self.paddle1, PADDLE_SPEED)
        elif event.keysym == "Up":
            self.move_paddle(self.paddle2, -PADDLE_SPEED)
        elif event.keysym == "Down":
            self.move_paddle(self.paddle2, PADDLE_SPEED)

    def move_paddle(self, paddle, dy):
        global difficulty_level, Pong, root
        coords = self.canvas.coords(paddle)
        if coords[1] + dy >= 0 and coords[3] + dy <= HEIGHT:
            self.canvas.move(paddle, 0, dy)

    def update(self):
        global difficulty_level, Pong, root
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

        self.move_bot_paddle(self.paddle2)

        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        self.after(20, self.update)

    def move_bot_paddle(self, paddle):
        global difficulty_level, Pong, root
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(paddle)
        paddle_center = (paddle_coords[1] + paddle_coords[3]) / 2

        if difficulty_level == "easy":
            reaction_time = 5
        elif difficulty_level == "medium":
            reaction_time =   10
        elif difficulty_level == "hard":
            reaction_time = 2000
        else:
            raise ValueError("Invalid difficulty level")
        
        if ball_coords[1] < paddle_center:
            self.move_paddle(paddle, -reaction_time)
        elif ball_coords[3] > paddle_center:
            self.move_paddle(paddle, reaction_time)

    def reset_ball(self):
        global difficulty_level, Pong, root
        self.canvas.coords(self.ball, WIDTH/2 - BALL_SIZE/2, HEIGHT/2 - BALL_SIZE/2,
                           WIDTH/2 + BALL_SIZE/2, HEIGHT/2 + BALL_SIZE/2)
        self.ball_speed_x = BALL_SPEED_X if random.randint(0, 1) == 0 else -BALL_SPEED_X
        self.ball_speed_y = BALL_SPEED_Y if random.randint(0, 1) == 0 else -BALL_SPEED_Y
def go():
    global Pong, root, difficulty_level
    root.destroy()
    pong = Pong()
    pong.title("Pong")
    pong.mainloop()
def easy():
    global difficulty_level, Pong, root
    difficulty_level = "easy"
    go()

def medium():
    global difficulty_level, Pong, root
    difficulty_level = "medium"
    go()

def hard():
    global difficulty_level, Pong, root
    difficulty_level = "hard"
    go()


root = tk.Tk()
root.title("Pong - setup")
title = tk.Label(root, text= "Pong", font=('normal', 40) )
subtiele = tk.Label(root, text= "Choose your difficulty", font=('normal', 20))  
line = tk.Label(root, text="\n")
easyb = tk.Button(root, text= "Easy", command= easy, font=('normal', 20))
mediumb = tk.Button(root, text= "Medium", command= easy, font=('normal', 20))
hardb = tk.Button(root, text= "Hard", command= easy, font=('normal', 20))

title.grid(row=0, column=0, columnspan=4)
subtiele.grid(row=1,column=0, columnspan=4)
line.grid(row=2,column=0)
easyb.grid(row=3,column=0)
mediumb.grid(row=3,column=1)
hardb.grid(row=3, column=3)
root.mainloop()



