import tkinter as tk


class Sprite:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def coords(self):
        return self.canvas.coords(self.item)

    def move(self, dx, dy):
        self.canvas.move(self.item, dx, dy)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(Sprite):
    def __init__(self, canvas, x, y):
        self.r = 8
        item = canvas.create_oval(x - self.r, y - self.r,
                                  x + self.r, y + self.r,
                                  fill="red")
        super().__init__(canvas, item)
        self.speedx = 4
        self.speedy = -4

    def update(self):
        x1, y1, x2, y2 = self.coords()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        # 좌우 벽
        if x1 <= 0 or x2 >= w:
            self.speedx *= -1

        # 위쪽 벽
        if y1 <= 0:
            self.speedy *= -1

        return y2 >= h  # 바닥 닿으면 죽음

    def bounce_y(self):
        self.speedy *= -1

    def speed_up(self):
        # 스페이스 누르면 속도 증가
        if self.speedx > 0:
            self.speedx += 1
        else:
            self.speedx -= 1

        if self.speedy > 0:
            self.speedy += 1
        else:
            self.speedy -= 1


class Paddle(Sprite):
    def __init__(self, canvas, x, y):
        self.w = 120
        self.h = 12
        item = canvas.create_rectangle(x - self.w/2, y - self.h/2,
                                       x + self.w/2, y + self.h/2,
                                       fill="white")
        super().__init__(canvas, item)

    def set_x(self, x):
        half = self.w/2
        w = self.canvas.winfo_width()
        x = max(half, min(w - half, x))  # 화면 안에서만 움직이도록 제한

        y1, y2 = self.coords()[1], self.coords()[3]
        self.canvas.coords(self.item, x - half, y1, x + half, y2)


class Brick(Sprite):
    def __init__(self, canvas, x, y, color):
        self.w = 52
        self.h = 22
        item = canvas.create_rectangle(x - self.w/2, y - self.h/2,
                                       x + self.w/2, y + self.h/2,
                                       fill=color, tags="brick")
        super().__init__(canvas, item)


class Game:
    def __init__(self, root):
        self.root = root
        self.width = 700
        self.height = 500

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.shapes = {}
        self.balls = []
        self.running = False
        self.score = 0

        self.score_text = self.canvas.create_text(80, 20, text="점수: 0",
                                                  fill="white", font=("Arial", 14))

        self.paddle = Paddle(self.canvas, self.width/2, self.height - 40)
        self.shapes[self.paddle.item] = self.paddle

        self.add_ball(self.width/2, self.height - 100)

        self.create_bricks()

        # 마우스 이동
        self.canvas.bind("<Motion>", self.mouse_move)

        # 키 이벤트 (포커스 문제 방지)
        self.root.bind("<space>", self.space_key)

        # canvas가 키 이벤트 받도록 포커스 강제
        self.canvas.focus_set()

    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for r in range(5):
            for c in range(12):
                x = 40 + c * 55
                y = 50 + r * 28
                brick = Brick(self.canvas, x, y, colors[r])
                self.shapes[brick.item] = brick

    def add_ball(self, x, y):
        ball = Ball(self.canvas, x, y)
        self.balls.append(ball)
        self.shapes[ball.item] = ball

    def mouse_move(self, e):
        self.paddle.set_x(e.x)

    def space_key(self, event):
        # 게임 시작 or 속도 증가
        if not self.running:
            self.start()
        else:
            for ball in self.balls:
                ball.speed_up()

    def start(self):
        self.running = True
        self.loop()

    def loop(self):
        if not self.running:
            return

        dead_balls = []

        for ball in self.balls:
            if ball.update():
                dead_balls.append(ball)
                continue

            ball.move(ball.speedx, ball.speedy)

            x1, y1, x2, y2 = ball.coords()

            # 패들 충돌
            px1, py1, px2, py2 = self.paddle.coords()
            if x2 >= px1 and x1 <= px2 and y2 >= py1 and y1 <= py2:
                ball.bounce_y()

            # 벽돌 충돌
            for item in self.canvas.find_overlapping(x1, y1, x2, y2):
                if item in self.shapes and isinstance(self.shapes[item], Brick):
                    brick = self.shapes[item]
                    brick.delete()
                    del self.shapes[item]

                    ball.bounce_y()

                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")

        # 죽은 공 삭제
        for b in dead_balls:
            if b in self.balls:
                self.balls.remove(b)

        if not self.balls:
            self.running = False
            self.canvas.create_text(self.width/2, self.height/2,
                    text="GAME OVER\n스페이스 누르면 재시작",
                    fill="white", font=("Arial", 20))
            return

        if not any(isinstance(obj, Brick) for obj in self.shapes.values()):
            self.running = False
            self.canvas.create_text(self.width/2, self.height/2,
                    text="YOU WIN!\n스페이스 누르면 재시작",
                    fill="white", font=("Arial", 20))
            return

        self.root.after(16, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brick Breaker")
    root.resizable(False, False)
    Game(root)
    root.mainloop()
