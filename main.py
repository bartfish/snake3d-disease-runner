from ursina import *
from game_objects import *

class Game(Ursina):

    def __init__(self):
        super().__init__()
        window.color = color.black
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        
        self.MAP_SIZE = 30
        self.new_game()

        camera.position = (self.MAP_SIZE // 2, -35, -20)
        camera.rotation_x = -65

    def create_map(self, MAP_SIZE):
        Entity(model='plane', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.white)

    def initialize_diseases(self):
        self.diseases = []
        add_3_with_each_lvl = 3
        for n in range(add_3_with_each_lvl):
            self.diseases.append(Diseases(self.MAP_SIZE, model='cube', color=color.red))

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.health = HealthIncrement(self.MAP_SIZE, model='cube', color=color.blue)
        self.snake = Snake(self.MAP_SIZE)
        self.initialize_diseases()

        descr = 'Health: '
        Text.default_resolution = 800 * Text.size
        test = Text(origin=(.5,.5), text=descr)

        text = Text(text=descr, wordwrap=10, origin=(-.5,.5), y=.25, background=True)
        Entity(model='circle', scale=.0005, color=color.white, y=text.y, z=-1)
        
    def check_apple_eaten(self):
        if self.snake.snake_elements_positions[-1] == self.health.position:
            self.snake.improve_snake()
            self.health.new_position()
            self.initialize_diseases()

    def check_game_over(self):
        snake = self.snake.snake_elements_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)):
                return

        print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)

        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        self.check_apple_eaten()
        self.check_game_over()
        self.snake.run()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()