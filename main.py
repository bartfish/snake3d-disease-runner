from ursina import *
from game_objects import *

class Game(Ursina):

    def __init__(self):
        super().__init__()
        window.color = color.light_gray

        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        
        self.MAP_SIZE = 30
        self.current_lvl = 1
        self.health_value = 1

        health_info_text = f"Health: {self.health_value}"
        self.text1 = Text(origin=(-0.5,9), text=health_info_text, scale=0.05)

        lvl_info_tet = f"Current level: {self.current_lvl}"
        self.text2 = Text(origin=(-0.5,11), text=lvl_info_tet, scale=0.05)
    
        scene.clear()
        
        Entity(model='plane', scale=self.MAP_SIZE, position=(self.MAP_SIZE // 2, self.MAP_SIZE // 2, 0))
        Entity(model=Grid(self.MAP_SIZE, self.MAP_SIZE), scale=self.MAP_SIZE,
               position=(self.MAP_SIZE // 2, self.MAP_SIZE // 2, -0.01), color=color.white)

        self.health = HealthIncrement(self.MAP_SIZE, model='cube', color=color.blue)
        self.snake = Snake(self.MAP_SIZE)
        self.initialize_diseases()

        self.health_value = 100
        self.current_lvl = 1
        self.update_info_text()

        camera.position = (self.MAP_SIZE // 2, -35, -20)
        camera.rotation_x = -65

    def initialize_diseases(self):
        self.diseases = []
        add_3_with_each_lvl = 3
        for n in range(add_3_with_each_lvl):
            self.diseases.append(Diseases(self.MAP_SIZE, model='cube', color=color.red))
       
    def update_info_text(self):

        if self.text1:
            destroy(self.text1)

        health_info_text = f"Health: {self.health_value}"
        self.text1 = Text(origin=(-0.5,9), text=health_info_text, scale=0.05)

        if self.text2:
            destroy(self.text2)

        lvl_info_tet = f"Current level: {self.current_lvl}"
        self.text2 = Text(origin=(-0.5,11), text=lvl_info_tet, scale=0.05)

    def verify_health_found(self):
        if self.snake.snake_elements_positions[-1] == self.health.position:
            self.current_lvl += 1
            self.health_value = self.health_value + randrange(self.current_lvl, 3 * self.current_lvl)
            self.snake.improve_snake()
            self.health.new_position()
            self.initialize_diseases()
            self.update_info_text()

    def is_game_over(self):
        snake = self.snake.snake_elements_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE:
            return
        exit()

    def update(self):
        self.verify_health_found()
        self.is_game_over()
        self.snake.run()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()