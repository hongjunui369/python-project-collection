from tkinter import *
import time, random


class Ball:
    def __init__(self, canvas, color, size, x, y, xspeed, yspeed):
        self.canvas = canvas
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.id = canvas.create_oval(x, y, x + size, y + size, fill=color)

    def move(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        (x1, y1, x2, y2) = self.canvas.coords(self.id)
        (self.x, self.y) = (x1, y1)
        if x1 <= 0 or x2 >= WIDTH:  # 공의 x좌표 음수이거나 x좌표가 오른쪽 경계를 넘으면
            self.xspeed = - self.xspeed  # 속도의 부호 반전시킨다.
        if y1 <= 0 or y2 >= HEIGHT:  # 공의 y좌표 음수이거나 오른쪽 경계를 넘으면
            self.yspeed = - self.yspeed


def add_random_ball(event=None):
    color = random.choice(color_list)
    size = random.randrange(10, 100)
    xspeed = random.randrange(1, 10)
    yspeed = random.randrange(1, 10)
    x = random.randrange(0, WIDTH - size)
    y = random.randrange(0, HEIGHT - size)

    new_ball = Ball(canvas, color, size, x, y, xspeed, yspeed)
    balls_list.append(new_ball)
    print(f"새 공 추가! 총 공 개수: {len(balls_list)}")


WIDTH = 800
HEIGHT = 400
color_list = ["yellow", "green", "blue", "red", "orange", "pink", "grey", "black"]
balls_list = []
window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

#바인딩
window.bind("<space>", add_random_ball)
canvas.bind("<Button-1>", add_random_ball)

#초기값
for i in range(10):
    color = random.choice(color_list)
    size = random.randrange(10, 100)
    xspeed = random.randrange(1, 10)
    yspeed = random.randrange(1, 10)
    balls_list.append(Ball(canvas, color, size, 0, 0, xspeed, yspeed))

while True:
    for ball in balls_list:
        ball.move()
    window.update()
    time.sleep(0.03)