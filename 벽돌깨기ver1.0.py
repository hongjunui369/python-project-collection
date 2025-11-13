#벽돌깨기 첫 구현 ver1.0
import tkinter as tk
from tkinter import Frame, Canvas


class BrickBreaker(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.width = 640
        self.height = 480
        self.canvas = Canvas(self, bg='blue', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        # 게임 객체들을 저장할 딕셔너리
        self.shapes = {}

        # 공과 패들 생성
        self.ball = Ball(self.canvas, self.width / 2, self.height / 2, 10)
        self.paddle = Paddle(self.canvas, self.width / 2, self.height - 30)

        # shapes에 공과 패들도 추가
        self.shapes[self.ball.item] = self.ball
        self.shapes[self.paddle.item] = self.paddle

        # Brick 객체를 2차원 모양으로 생성한다.
        for r in range(1, 4):
            for c in range(1, 10):
                brick = Brick(self.canvas, c * 60, r * 30)
                # Brick 객체를 shapes에 저장한다.
                self.shapes[brick.item] = brick

        # 캔버스가 키보드 이벤트를 받을 수 있도록 설정한다.
        self.canvas.focus_set()
        # 화살표키와 스페이스키에 이벤트를 붙인다.
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-20, 0))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(20, 0))
        self.canvas.bind('<space>', lambda _: self.start())

        self.game_active = False
        self.bricks_remaining = 27  # 벽돌 개수 추적

    def start(self):
        """게임을 시작하는 메소드"""
        if not self.game_active:
            self.game_active = True
            self.game_loop()

    def game_loop(self):
        """게임 루프"""
        if not self.game_active:
            return

        # 공 이동
        self.ball.update()
        self.ball.move()

        # 충돌 검사
        coords = self.ball.get_coords()
        items = self.canvas.find_overlapping(*coords)

        # 충돌 처리 (공 자신은 제외)
        collision_objects = []
        for item in items:
            if item in self.shapes and item != self.ball.item:
                collision_objects.append(self.shapes[item])

        # 충돌이 있는 경우 처리
        if collision_objects:
            self.ball.handle_collision(collision_objects)

            # 벽돌 충돌 처리
            for obj in collision_objects:
                if isinstance(obj, Brick) and obj in self.shapes.values():
                    obj.handle_collision()
                    # shapes에서 제거
                    if obj.item in self.shapes:
                        del self.shapes[obj.item]
                    self.bricks_remaining -= 1

        # 게임 종료 조건 확인
        ball_x, ball_y = self.ball.get_position()
        if ball_y >= self.height:
            self.game_active = False
            self.canvas.create_text(self.width / 2, self.height / 2,
                                    text="GAME OVER", fill="white", font=("Arial", 24))
            return

        if self.bricks_remaining <= 0:
            self.game_active = False
            self.canvas.create_text(self.width / 2, self.height / 2,
                                    text="YOU WIN!", fill="white", font=("Arial", 24))
            return

        # 게임 계속 진행
        self.after(30, self.game_loop)


class Sprite():
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item
        self.speedx = 0
        self.speedy = 0
        self.x = 0
        self.y = 0

    def get_coords(self):
        return self.canvas.coords(self.item)

    def get_position(self):
        pos = self.canvas.coords(self.item)
        if pos:
            x = (pos[0] + pos[2]) / 2  # 중심 x 좌표
            y = (pos[1] + pos[3]) / 2  # 중심 y 좌표
            return x, y
        return 0, 0

    def update(self):
        pass

    def move(self):
        self.canvas.move(self.item, self.speedx, self.speedy)
        pos = self.get_position()
        if pos:
            self.x, self.y = pos

    def delete(self):
        self.canvas.delete(self.item)


class Ball(Sprite):
    def __init__(self, canvas, x, y, radius):
        self.radius = radius
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='red')
        super().__init__(canvas, item)
        self.x = x
        self.y = y
        self.speedx = 5
        self.speedy = -5  # 시작시 위로 이동

    def update(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        coords = self.get_coords()
        if not coords:
            return

        x1, y1, x2, y2 = coords

        # 벽 충돌 처리
        if x1 <= 0 or x2 >= width:
            self.speedx *= -1
        if y1 <= 0:
            self.speedy *= -1

    def handle_collision(self, collision_objects):
        """충돌 처리 메소드"""
        if not collision_objects:
            return

        # 패들과의 충돌
        for obj in collision_objects:
            if isinstance(obj, Paddle):
                # 패들의 어느 부분에 충돌했는지에 따라 반사각 조정
                paddle_x, paddle_y = obj.get_position()
                ball_x, ball_y = self.get_position()

                # 패들 중심으로부터의 거리 비율
                offset = (ball_x - paddle_x) / (obj.width / 2)
                self.speedx = offset * 8  # x 속도 조정
                self.speedy = -abs(self.speedy)  # y 방향 반전 (항상 위로)
                break

            elif isinstance(obj, Brick):
                # 벽돌과의 충돌 - y 방향 반전
                self.speedy *= -1
                break


class Paddle(Sprite):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 20
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2,
                                       x + self.width / 2, y + self.height / 2,
                                       fill='white')
        super().__init__(canvas, item)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        width = self.canvas.winfo_width()
        new_x = self.x + dx

        # 패들이 화면 밖으로 나가지 않도록 제한
        if new_x >= self.width / 2 and new_x <= width - self.width / 2:
            actual_dx = new_x - self.x
            self.x = new_x
            self.canvas.move(self.item, actual_dx, dy)


class Brick(Sprite):
    def __init__(self, canvas, x, y):
        self.width = 52
        self.height = 25
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2,
                                       x + self.width / 2, y + self.height / 2,
                                       fill='yellow', tags='brick')
        super().__init__(canvas, item)
        self.x = x
        self.y = y

    def handle_collision(self):
        """벽돌 충돌 처리 - 삭제"""
        self.delete()


# 메인 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brick Breaker")
    root.resizable(False, False)
    game = BrickBreaker(root)
    root.mainloop()