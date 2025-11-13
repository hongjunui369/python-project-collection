from tkinter import *
import time


class Ball:
    def __init__(self, canvas, color, size, x, y, xspeed, yspeed):
        self.canvas = canvas		# 캔버스 객체 #a.b = canavs
        self.color = color		# Ball의 색상
        self.size = size		# Ball의 크기
        self.x = x			# Ball의 x좌표
        self.y = y			# Ball의 y좌표
        self.xspeed = xspeed		# Ball의 수평방향 속도
        self.yspeed = yspeed		# Ball의 수직방향 속도
        self.id = canvas.create_oval(x, y, x+size, y+size, fill=color)

    def move(self):  # Ball을 이동시키는 함수
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        (x1, y1, x2, y2) = self.canvas.coords(self.id)  # 공의 현재 위치를 얻는다.
        (self.x, self.y) = (x1, y1)
        if x1 <= 0 or x2 >= WIDTH:  # 공의 x좌표가 음수이거나 x좌표가 오른쪽 경계를 넘으면
            self.xspeed = - self.xspeed  # 속도의 부호를 반전시킨다.
        if y1 <= 0 or y2 >= HEIGHT:  # 공의 x좌표가 음수이거나오른쪽 경계를 넘으면
            self.yspeed = - self.yspeed

WIDTH = 800		# 윈도우의 가로 크기를 저장한다.
HEIGHT = 400		# 윈도우의 세로 크기를 저장한다.

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()
ballA = Ball(canvas, "red", 30, 1, 1, 2, 1)

while True:
    ballA.move()
    window.update()
    time.sleep(0.03)
