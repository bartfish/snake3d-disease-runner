from ursina import *
from random import randrange
import math

def generate_random_position(map_size):
    return (randrange(map_size) + 0.5, randrange(map_size) + 0.5, -0.5)

class Diseases(Entity):

    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.position = generate_random_position(self.MAP_SIZE)

    def calculate_points_distance(self, point_one, point_two):
        return math.sqrt(((point_one[0] - point_two[0] )**2) + ((point_one[1]-point_two[1])**2) )

    def was_disease_caught(self, disease_poses, health_upgrade, lvl_number):
        for i in range(len(disease_poses)):
            if (disease_poses[i] == health_upgrade):
                return 5

            if (calculate_points_distance(disease_poses[i], health_upgrade) <= 20*lvl_number*0.25):
                return 1
        return 0

class HealthIncrement(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = generate_random_position(self.MAP_SIZE)

class Snake:
    def __init__(self, MAP_SIZE):
        self.MAP_SIZE = MAP_SIZE
        self.snake_elements = 1

        self.position_length = 2
        self.snake_elements_positions = [Vec3(generate_random_position(self.MAP_SIZE))]
        self.snake_elements_arr = []
        self.add_new_snake_element(self.snake_elements_positions[0])
        
        self.direction = Vec3(0, 0, 0)
        self.speed = 4
        self.frame_counter = 0

    def add_new_snake_element(self, position):
        entity = Entity(model='cube', color=color.green, position=position)
        entity.add_script(SmoothFollow(speed=10, target=entity, offset=(0, 0, 0)))
        self.snake_elements_arr.insert(len(self.snake_elements_arr) - 1, entity)

    def improve_snake(self):
        self.snake_elements += 1
        self.position_length += 1
        self.add_new_snake_element(self.snake_elements_positions[len(self.snake_elements_positions) - 1])

    def move_snake(self):
        self.frame_counter = self.frame_counter + 1.5
        if not self.frame_counter % self.speed:
            
            for key in 'awsd':
                if held_keys[key]:

                    if key == 'a':
                        self.direction = Vec3(-1, 0, 0)
                    elif key == 'd':
                        self.direction = Vec3(1, 0, 0)
                    elif key == 'w':
                        self.direction = Vec3(0, 1, 0)
                    elif key == 's':
                        self.direction = Vec3(0, -1, 0)

                    break

            self.snake_elements_positions.append(self.snake_elements_positions[-1] + self.direction)
            self.snake_elements_positions = self.snake_elements_positions[ - self.snake_elements:]

            for snake_el, snake_el_position in zip(self.snake_elements_arr, self.snake_elements_positions):
                snake_el.position = snake_el_position

class Game(Ursina):

    def __init__(self):
        super().__init__()

        self.current_lvl = 1
        self.health_value = 1
        window.color = color.light_gray
        self.MAP_SIZE = 30

        health_info_text = f"Health: {self.health_value}"
        self.text1 = Text(origin=(-0.5,9), text=health_info_text, scale=0.05)

        lvl_info_tet = f"Current level: {self.current_lvl}"
        self.text2 = Text(origin=(-0.5,11), text=lvl_info_tet, scale=0.05)
    
        scene.clear()
        
        Entity(model='plane', scale=self.MAP_SIZE, position=(self.MAP_SIZE / 2, self.MAP_SIZE / 2, 0))
        Entity(model=Grid(self.MAP_SIZE, self.MAP_SIZE), scale=self.MAP_SIZE, position=(self.MAP_SIZE / 2, self.MAP_SIZE / 2, -0.001), color=color.black33)

        self.health = HealthIncrement(self.MAP_SIZE, model='cube', color=color.blue)
        self.snake = Snake(self.MAP_SIZE)
        self.initialize_diseases()

        self.health_value = 100
        self.current_lvl = 1
        self.update_info_text()

        camera.position = (self.MAP_SIZE / 2, -35, -20)
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

    def is_game_over(self):
        snake = self.snake.snake_elements_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE:
            return
        exit()

    def update(self):
        if self.snake.snake_elements_positions[-1] == self.health.position:
            self.current_lvl += 1
            self.health_value = self.health_value + randrange(self.current_lvl, 3 * self.current_lvl)
            self.snake.improve_snake()
            self.health.new_position()
            self.initialize_diseases()
            self.update_info_text()
        
        self.is_game_over()
        self.snake.move_snake()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()