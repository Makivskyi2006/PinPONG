import pygame as pg
import random
import sys
from typing import Tuple

WIN_W, WIN_H = 900, 540
FPS = 60

PADDLE_W, PADDLE_H = 12, 110
BALL_SIZE = 14
PADDLE_SPEED = 7.0
BALL_SPEED = 6.0
SCORE_TO_WIN = 10

WHITE: Tuple[int, int, int] = (245, 245, 245)
BG: Tuple[int, int, int] = (35, 35, 35)
ACCENT: Tuple[int, int, int] = (120, 120, 120)

def clamp(v: float, low: float, high: float) -> float:
    if v < low:
        return low
    if v > high:
        return high
    return v

class Paddle:
    """Обычная ракетка. Храню x/y и скорость; рендерю Rect по запросу."""

    def __init__(self, x: int, y: float, speed: float = PADDLE_SPEED):
        self.x = x
        self.y = y
        self.speed = speed

    @property
    def rect(self) -> pg.Rect:

        return pg.Rect(int(self.x), int(self.y), PADDLE_W, PADDLE_H)

    def move(self, dy: float) -> None:
 
        self.y = clamp(self.y + dy, 0, WIN_H - PADDLE_H)

class Ball:
    """Мяч: позиция, скорость и метод reset(). Ничего экстраординарного."""

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.reset(kick=True)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(int(self.x), int(self.y), BALL_SIZE, BALL_SIZE)

    def reset(self, kick: bool = False) -> None:

        self.x = WIN_W / 2 - BALL_SIZE / 2
        self.y = WIN_H / 2 - BALL_SIZE / 2
        if kick:
            self.vx = BALL_SPEED * random.choice((-1, 1))

            self.vy = random.uniform(-BALL_SPEED * 0.75, BALL_SPEED * 0.75)
            if abs(self.vy) < 1.0:
                self.vy = 1.2 * (1 if random.random() < 0.5 else -1)
        else:
            self.vx = 0.0
            self.vy = 0.0

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy


        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + BALL_SIZE >= WIN_H:
            self.y = WIN_H - BALL_SIZE
            self.vy = -abs(self.vy)


def draw_center_dashes(surf: pg.Surface) -> None:

    for y in range(0, WIN_H, 18):
        surf.fill(ACCENT, rect=pg.Rect(WIN_W // 2 - 2, y, 4, 10))


def handle_input(keys, left: Paddle, right: Paddle) -> None:

    if keys[pg.K_w]:
        left.move(-left.speed)
    if keys[pg.K_s]:
        left.move(+left.speed)

    if keys[pg.K_UP]:
        right.move(-right.speed)
    if keys[pg.K_DOWN]:
        right.move(+right.speed)


def collide_and_spin(ball: Ball, left: Paddle, right: Paddle) -> None:

    if ball.rect.colliderect(left.rect) and ball.vx < 0:
        ball.x = left.rect.right

        ball.vx = abs(ball.vx) * 1.03

        offset = (ball.rect.centery - left.rect.centery) / (PADDLE_H / 2)
        ball.vy += offset * 2.0

    if ball.rect.colliderect(right.rect) and ball.vx > 0:
        ball.x = right.rect.left - BALL_SIZE
        ball.vx = -abs(ball.vx) * 1.03
        offset = (ball.rect.centery - right.rect.centery) / (PADDLE_H / 2)
        ball.vy += offset * 2.0


def draw_score(surf: pg.Surface, font: pg.font.Font, score_l: int, score_r: int) -> None:
    text = font.render(f"{score_l}   {score_r}", True, WHITE)
    surf.blit(text, (WIN_W // 2 - text.get_width() // 2, 18))


def maybe_show_win(surf: pg.Surface, font: pg.font.Font, score_l: int, score_r: int) -> bool:
    if score_l >= SCORE_TO_WIN or score_r >= SCORE_TO_WIN:
        winner = "Left" if score_l > score_r else "Right"
        msg = font.render(f"{winner} wins!  (R — restart)", True, WHITE)
        surf.blit(msg, (WIN_W // 2 - msg.get_width() // 2, WIN_H // 2 - msg.get_height() // 2))
        return True
    return False


def main() -> None:
    random.seed()

    pg.init()
    screen = pg.display.set_mode((WIN_W, WIN_H))
    pg.display.set_caption("Pong — 2 Players (human-ish code)")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 48)
    left = Paddle(30, WIN_H / 2 - PADDLE_H / 2)
    right = Paddle(WIN_W - 30 - PADDLE_W, WIN_H / 2 - PADDLE_H / 2)
    ball = Ball()

    score_l = 0
    score_r = 0
    paused = False

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                elif e.key == pg.K_p:
                    paused = not paused
                elif e.key == pg.K_r:
    
                    ball.reset(kick=True)

        keys = pg.key.get_pressed()
        handle_input(keys, left, right)
        if not paused:
            ball.update()
            collide_and_spin(ball, left, right)

            if ball.x < -BALL_SIZE:
                score_r += 1
                ball.reset(kick=True)
            elif ball.x > WIN_W + BALL_SIZE:
                score_l += 1
                ball.reset(kick=True)

 
        screen.fill(BG)
        draw_center_dashes(screen)

        pg.draw.rect(screen, WHITE, left.rect, border_radius=4)
        pg.draw.rect(screen, WHITE, right.rect, border_radius=4)
        pg.draw.rect(screen, WHITE, ball.rect, border_radius=3)

        draw_score(screen, font, score_l, score_r)

        someone_won = maybe_show_win(screen, font, score_l, score_r)
        if paused and not someone_won:
            msg = font.render("PAUSED (P)", True, WHITE)
            screen.blit(msg, (WIN_W // 2 - msg.get_width() // 2, WIN_H // 2 - msg.get_height() // 2))

        pg.display.flip()
        clock.tick(FPS)
    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
