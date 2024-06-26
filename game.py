import pygame
import random

# Initialize pygame
pygame.init()

# Set the dimensions of the window
window_x = 720
window_y = 480

# Set colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialize game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# Frames per second controller
fps = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_dir_to(self, dir):
        if dir == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if dir == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if dir == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if dir == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        if self.direction == 'UP':
            self.snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_position[0] += 10

        self.snake_body.insert(0, list(self.snake_position))
        self.snake_body.pop()

    def grow(self):
        self.snake_body.append([0, 0])

    def check_collision(self):
        if self.snake_position[0] < 0 or self.snake_position[0] > window_x-10:
            return True
        if self.snake_position[1] < 0 or self.snake_position[1] > window_y-10:
            return True

        for block in self.snake_body[1:]:
            if self.snake_position == block:
                return True

        return False

    def get_head_position(self):
        return self.snake_position

    def get_body(self):
        return self.snake_body

# Food class
class Food:
    def __init__(self):
        self.food_position = [random.randrange(1, (window_x//10)) * 10,
                              random.randrange(1, (window_y//10)) * 10]
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.food_position = [random.randrange(1, (window_x//10)) * 10,
                                  random.randrange(1, (window_y//10)) * 10]
            self.is_food_on_screen = True
        return self.food_position

    def set_food_on_screen(self, b):
        self.is_food_on_screen = b

# Game class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_dir_to('UP')
                if event.key == pygame.K_DOWN:
                    self.snake.change_dir_to('DOWN')
                if event.key == pygame.K_LEFT:
                    self.snake.change_dir_to('LEFT')
                if event.key == pygame.K_RIGHT:
                    self.snake.change_dir_to('RIGHT')

        self.snake.move()
        snake_head = self.snake.get_head_position()
        if snake_head == self.food.spawn_food():
            self.score += 10
            self.food.set_food_on_screen(False)
            self.snake.grow()

        game_window.fill(black)

        for pos in self.snake.get_body():
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(
            self.food.spawn_food()[0], self.food.spawn_food()[1], 10, 10))

        if self.snake.check_collision():
            return False

        pygame.display.update()
        fps.tick(25)
        return True

    def get_score(self):
        return self.score

    def game_over(self):
        font = pygame.font.SysFont('times new roman', 50)
        GO_surf = font.render('Game Over', True, red)
        GO_rect = GO_surf.get_rect()
        GO_rect.midtop = (window_x/2, window_y/4)
        game_window.fill(black)
        game_window.blit(GO_surf, GO_rect)
        self.show_score(0, red, 'times', 20)
        pygame.display.flip()
        pygame.time.sleep(2)
        return False

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surf = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surf.get_rect()
        if choice == 1:
            score_rect.midtop = (window_x/10, 15)
        else:
            score_rect.midtop = (window_x/2, window_y/1.25)
        game_window.blit(score_surf, score_rect)

# Main function
def main():
    game = Game()

    while True:
        if not game.play_step():
            game.game_over()
            break

    print(f'Your Score: {game.get_score()}')
    pygame.quit()

if __name__ == '__main__':
    main()
