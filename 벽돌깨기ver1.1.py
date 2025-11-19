import tkinter as tk


class BrickBreaker:
    def __init__(self, root):
        self.root = root
        self.width = 640
        self.height = 480

        self.canvas = tk.Canvas(root, bg='blue', width=self.width, height=self.height)
        self.canvas.pack()

        self.shapes = {}
        self.game_active = False
        self.bricks_count = 27

        self.create_objects()
        self.setup_bindings()

    def create_objects(self):
        self.ball = Ball(self.canvas, self.width / 2, self.height / 2)
        self.paddle = Paddle(self.canvas, self.width / 2, self.height - 30)

        self.shapes[self.ball.item] = self.ball
        self.shapes[self.paddle.item] = self.paddle

        for r in range(3):
            for c in range(9):
                brick = Brick(self.canvas, c * 60 + 30, r * 30 + 15)
                self.shapes[brick.item] = brick

    def setup_bindings(self):
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda e: self.paddle.move(-20))
        self.canvas.bind('<Right>', lambda e: self.paddle.move(20))
        self.canvas.bind('<space>', lambda e: self.start())
        self.canvas.bind('y', lambda e: self.restart())
        self.canvas.bind('n', lambda e: self.root.quit())

    def start(self):
        if not self.game_active:
            self.game_active = True
            self.game_loop()

    def restart(self):
        if not self.game_active:
            self.canvas.delete("all")
            self.shapes.clear()
            self.bricks_count = 27
            self.create_objects()
            self.start()

    def game_loop(self):
        if not self.game_active:
            return

        self.ball.update()
        self.ball.move()

        coords = self.ball.get_coords()
        items = self.canvas.find_overlapping(*coords)

        for item in items:
            if item in self.shapes and item != self.ball.item:
                obj = self.shapes[item]
                self.ball.handle_collision(obj)

                if isinstance(obj, Brick):
                    obj.delete()
                    del self.shapes[obj.item]
                    self.bricks_count -= 1

        ball_x, ball_y = self.ball.get_position()

        if ball_y >= self.height:
            self.game_over()
            return

        if self.bricks_count <= 0:
            self.you_win()
            return

        self.root.after(30, self.game_loop)

    def game_over(self):
        self.game_active = False
        self.canvas.create_text(self.width / 2, self.height / 2,
                                text="GAME OVER\nRestart? (Y/N)",
                                fill="white", font=("Arial", 20))

    def you_win(self):
        self.game_active = False
        self.canvas.create_text(self.width / 2, self.height / 2,
                                text="YOU WIN!\nRestart? (Y/N)",
                                fill="white", font=("Arial", 20))


class Sprite:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_coords(self):
        return self.canvas.coords(self.item)

    def get_position(self):
        pos = self.canvas.coords(self.item)
        if pos:
            return (pos[0] + pos[2]) / 2, (pos[1] + pos[3]) / 2
        return 0, 0

    def move(self, dx=0, dy=0):
        self.canvas.move(self.item, dx, dy)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(Sprite):
    def __init__(self, canvas, x, y):
        item = canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')
        super().__init__(canvas, item)
        self.speedx = 5
        self.speedy = -5

    def update(self):
        width = self.canvas.winfo_width()
        coords = self.get_coords()
        if not coords:
            return

        x1, y1, x2, y2 = coords

        if x1 <= 0 or x2 >= width:
            self.speedx *= -1
        if y1 <= 0:
            self.speedy *= -1

    def move(self):
        self.canvas.move(self.item, self.speedx, self.speedy)

    def handle_collision(self, obj):
        if isinstance(obj, Paddle):
            self.speedy = -abs(self.speedy)
        elif isinstance(obj, Brick):
            self.speedy *= -1


class Paddle(Sprite):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 20
        item = canvas.create_rectangle(x - 50, y - 10, x + 50, y + 10, fill='white')
        super().__init__(canvas, item)
        self.x = x
        self.y = y

    def move(self, dx):
        width = self.canvas.winfo_width()
        new_x = self.x + dx

        if 50 <= new_x <= width - 50:
            actual_dx = new_x - self.x
            self.x = new_x
            self.canvas.move(self.item, actual_dx, 0)


class Brick(Sprite):
    def __init__(self, canvas, x, y):
        item = canvas.create_rectangle(x - 26, y - 12, x + 26, y + 12, fill='yellow')
        super().__init__(canvas, item)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brick Breaker")
    root.resizable(False, False)
    game = BrickBreaker(root)
    root.mainloop()