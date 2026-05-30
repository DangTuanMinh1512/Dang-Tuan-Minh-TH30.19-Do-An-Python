import pygame
import random
import sys
import os

# Khởi tạo Pygame
pygame.init()

# --- CẤU HÌNH ĐỒ HỌA & CỬA SỔ ---
WIDTH, HEIGHT = 800, 700
GRID_SIZE = 25
GAME_TOP = 100
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - GAME_TOP) // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake Cyberpunk Pro")
clock = pygame.time.Clock()

# --- BẢNG MÀU NEON ---
BG_COLOR = (15, 15, 27)
PANEL_COLOR = (22, 22, 39)
GRID_LINE = (25, 25, 45)
SNAKE_HEAD = (0, 242, 254)
SNAKE_BODY = (79, 172, 254)
FOOD_COLOR = (255, 0, 127)
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY = (140, 140, 160)
SCORE_COLOR = (0, 255, 135)
EXIT_COLOR = (255, 50, 50)  # Màu đỏ Neon cho nút thoát

# --- HỆ THỐNG PHÔNG CHỮ ---
try:
    font_large = pygame.font.SysFont("Segoe UI", 60, bold=True)
    font_medium = pygame.font.SysFont("Segoe UI", 34, bold=True)
    font_small = pygame.font.SysFont("Segoe UI", 20, bold=False)
except:
    font_large = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 24)

# --- KHỞI TẠO ĐIỂM KỶ LỤC ---
HIGH_SCORE_FILE = "highscore.txt"
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
else:
    high_score = 0


# --- CÁC HÀM TRỢ GIÚP ĐỒ HỌA ---
def draw_text(text, font, color, surface, x, y, center=True):
    shadow = font.render(text, True, (0, 0, 0))
    shadow_rect = shadow.get_rect()
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()

    if center:
        shadow_rect.center = (x + 2, y + 2)
        text_rect.center = (x, y)
    else:
        shadow_rect.topleft = (x + 1, y + 1)
        text_rect.topleft = (x, y)

    surface.blit(shadow, shadow_rect)
    surface.blit(text_obj, text_rect)


def draw_neon_rect(surface, color, rect, width=0, border_radius=5):
    pygame.draw.rect(surface, color, rect, width, border_radius=border_radius)
    if width == 0:
        glow_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))
        pygame.draw.rect(surface, glow_color, rect.inflate(4, 4), 1, border_radius=border_radius + 2)


# --- LỚP ĐỐI TƯỢNG GAME ---
class SnakeGame:
    def __init__(self):
        self.state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER
        self.reset_game()

    def reset_game(self):
        self.snake = [
            {"x": GRID_WIDTH // 2, "y": GRID_HEIGHT // 2},
            {"x": GRID_WIDTH // 2 - 1, "y": GRID_HEIGHT // 2},
            {"x": GRID_WIDTH // 2 - 2, "y": GRID_HEIGHT // 2}
        ]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.score = 0
        self.food = None
        self.spawn_food()

    def spawn_food(self):
        while True:
            self.food = {
                "x": random.randint(0, GRID_WIDTH - 1),
                "y": random.randint(0, GRID_HEIGHT - 1)
            }
            if self.food not in self.snake:
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # XỬ LÝ CHO MÀN HÌNH CHÍNH (MENU)
                if self.state == "MENU":
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.reset_game()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_q:  # Bấm Q để thoát hẳn game
                        pygame.quit()
                        sys.exit()

                # XỬ LÝ KHI ĐANG CHƠI (PLAYING)
                elif self.state == "PLAYING":
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != "DOWN":
                        self.next_direction = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != "UP":
                        self.next_direction = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != "RIGHT":
                        self.next_direction = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != "LEFT":
                        self.next_direction = "RIGHT"
                    elif event.key == pygame.K_SPACE:
                        self.state = "PAUSED"
                    elif event.key == pygame.K_ESCAPE:  # Bấm ESC để quay lại Menu chính
                        self.state = "MENU"

                # XỬ LÝ KHI TẠM DỪNG (PAUSED)
                elif self.state == "PAUSED":
                    if event.key == pygame.K_SPACE:
                        self.state = "PLAYING"
                    elif event.key == pygame.K_q:  # Thoát về Menu từ trạng thái Pause
                        self.state = "MENU"

                # XỬ LÝ KHI GAME OVER
                elif self.state == "GAME_OVER":
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.reset_game()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_q:  # Bấm Q để quay lại Menu chính
                        self.state = "MENU"

    def update(self):
        if self.state != "PLAYING":
            return

        self.direction = self.next_direction
        head = self.snake[0].copy()

        if self.direction == "UP":
            head["y"] -= 1
        elif self.direction == "DOWN":
            head["y"] += 1
        elif self.direction == "LEFT":
            head["x"] -= 1
        elif self.direction == "RIGHT":
            head["x"] += 1

        # Kiểm tra va chạm
        if (head["x"] < 0 or head["x"] >= GRID_WIDTH or
                head["y"] < 0 or head["y"] >= GRID_HEIGHT or
                head in self.snake):
            self.state = "GAME_OVER"
            global high_score
            if self.score > high_score:
                high_score = self.score
                with open(HIGH_SCORE_FILE, "w") as f:
                    f.write(str(high_score))
            return

        self.snake.insert(0, head)

        if head["x"] == self.food["x"] and head["y"] == self.food["y"]:
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        screen.fill(BG_COLOR)

        # 1. Vẽ lưới đồ họa mờ
        for i in range(GRID_WIDTH):
            pygame.draw.line(screen, GRID_LINE, (i * GRID_SIZE, GAME_TOP), (i * GRID_SIZE, HEIGHT))
        for j in range(GRID_HEIGHT):
            pygame.draw.line(screen, GRID_LINE, (0, GAME_TOP + j * GRID_SIZE), (WIDTH, GAME_TOP + j * GRID_SIZE))

        # 2. Vẽ thanh thông tin phía trên
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, GAME_TOP))
        pygame.draw.line(screen, SNAKE_HEAD, (0, GAME_TOP), (WIDTH, GAME_TOP), 2)

        draw_text(f"SCORE: {self.score}", font_medium, SCORE_COLOR, screen, 40, GAME_TOP // 2, center=False)
        draw_text(f"HI-SCORE: {high_score}", font_medium, FOOD_COLOR, screen, WIDTH - 260, GAME_TOP // 2, center=False)

        # 3. Vẽ mồi Neon
        food_rect = pygame.Rect(self.food["x"] * GRID_SIZE + 2, GAME_TOP + self.food["y"] * GRID_SIZE + 2,
                                GRID_SIZE - 4, GRID_SIZE - 4)
        draw_neon_rect(screen, FOOD_COLOR, food_rect, border_radius=GRID_SIZE // 2)

        # 4. Vẽ rắn Neon bo góc
        for idx, part in enumerate(self.snake):
            part_rect = pygame.Rect(part["x"] * GRID_SIZE + 1, GAME_TOP + part["y"] * GRID_SIZE + 1, GRID_SIZE - 2,
                                    GRID_SIZE - 2)
            if idx == 0:
                draw_neon_rect(screen, SNAKE_HEAD, part_rect, border_radius=7)
            else:
                draw_neon_rect(screen, SNAKE_BODY, part_rect, border_radius=4)

        # 5. XỬ LÝ HIỂN THỊ MENU & CÁC NÚT ĐIỀU KHIỂN
        if self.state == "MENU":
            self.draw_overlay()
            draw_text("NEON SNAKE", font_large, SNAKE_HEAD, screen, WIDTH // 2, HEIGHT // 2 - 100)

            # Gợi ý nút Chơi và nút Thoát
            draw_text("Bấm [ SPACE / ENTER ] để Bắt Đầu", font_medium, TEXT_WHITE, screen, WIDTH // 2, HEIGHT // 2 - 10)
            draw_text("Bấm [ Q ] để Thoát Trò Chơi", font_medium, EXIT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 50)

            draw_text("Di chuyển: Phím Mũ Tên hoặc W-A-S-D. Tạm dừng: SPACE", font_small, TEXT_GRAY, screen, WIDTH // 2,
                      HEIGHT // 2 + 130)

        elif self.state == "PAUSED":
            self.draw_overlay()
            draw_text("ĐÃ TẠM DỪNG", font_large, SNAKE_HEAD, screen, WIDTH // 2, HEIGHT // 2 - 60)
            draw_text("Bấm [ SPACE ] để Tiếp tục chơi", font_medium, TEXT_WHITE, screen, WIDTH // 2, HEIGHT // 2 + 10)
            draw_text("Bấm [ Q ] để Quay lại Menu chính", font_medium, EXIT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 60)

        elif self.state == "GAME_OVER":
            self.draw_overlay()
            draw_text("GAME OVER", font_large, FOOD_COLOR, screen, WIDTH // 2, HEIGHT // 2 - 100)
            draw_text(f"Điểm số của bạn: {self.score}", font_medium, SCORE_COLOR, screen, WIDTH // 2, HEIGHT // 2 - 30)

            draw_text("Bấm [ SPACE ] để Chơi lại", font_medium, TEXT_WHITE, screen, WIDTH // 2, HEIGHT // 2 + 30)
            draw_text("Bấm [ Q ] để Quay về Menu chính", font_medium, EXIT_COLOR, screen, WIDTH // 2, HEIGHT // 2 + 80)

        pygame.display.flip()

    def draw_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT - GAME_TOP), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 225))
        screen.blit(overlay, (0, GAME_TOP))


# --- VÒNG LẶP CHÍNH ---
def main():
    game = SnakeGame()
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(11)  # Tốc độ di chuyển của rắn


if __name__ == "__main__":
    main()