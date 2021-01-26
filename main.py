from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randrange
import math

def generate_random_position(map_size):
    return (randrange(map_size) + 0.5, randrange(map_size) + 0.5, -0.5)

def calculate_points_distance(point_one, point_two):
    xs = (point_one[0] - point_two[0])**2
    ys = (point_one[1] - point_two[1])**2
    zs = (point_one[2] - point_two[2])**2

    # print (point_one)
    # print (point_two)

    return math.sqrt(xs + ys + zs)

def was_disease_caught(disease_poses, snake_pos, lvl_number):
    for i in range(len(disease_poses)):
        if (calculate_points_distance(disease_poses[i].position, snake_pos) <= 3):
            return 0.5
    return 0

class Diseases(Entity):

    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.position = generate_random_position(self.MAP_SIZE)

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
        self.frame_counter = 0
    
    def move_snake(self):
            
        for key, value in held_keys.items():
            if value != 0:
                if key == 'a' or key == 'left arrow':
                    self.direction = Vec3(-1, 0, 0) * time.dt * 10
                elif key == 'd' or key == 'right arrow':
                    self.direction = Vec3(1, 0, 0) * time.dt * 10
                elif key == 'w' or key == 'up arrow': 
                    self.direction = Vec3(0, 1, 0) * time.dt * 10 
                elif key == 's' or key == 'down arrow':
                    self.direction = Vec3(0, -1, 0) * time.dt * 10
                break

        self.snake_elements_positions.append(self.snake_elements_positions[-1] + self.direction)
        self.snake_elements_positions = self.snake_elements_positions[ -self.snake_elements:]

        for snake_el, snake_el_position in zip(self.snake_elements_arr, self.snake_elements_positions):
            snake_el.position = snake_el_position

    def add_new_snake_element(self, position):
        entity = Entity(model='cube', color=color.green, position=position)
        entity.add_script(SmoothFollow(speed=10, target=entity, offset=(0, 0, 0)))
        self.snake_elements_arr.insert(len(self.snake_elements_arr) - 1, entity)

    def improve_snake(self):
        self.snake_elements += 1
        self.position_length += 1
        self.add_new_snake_element(self.snake_elements_positions[len(self.snake_elements_positions) - 1])


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

        self.text3 = Text(origin=(-0.5,11), text=lvl_info_tet, scale=0.05)
    
        scene.clear() # comment to show ursina info and hide game text fields
        
        Entity(model='plane', scale=self.MAP_SIZE, position=(self.MAP_SIZE / 2, self.MAP_SIZE / 2, 0))
        Entity(model=Grid(self.MAP_SIZE, self.MAP_SIZE), scale=self.MAP_SIZE, position=(self.MAP_SIZE / 2, self.MAP_SIZE / 2, -0.001), color=color.black33)

        self.health = HealthIncrement(self.MAP_SIZE, model='cube', color=color.blue)
        self.snake = Snake(self.MAP_SIZE)
        self.diseases = []
        self.initialize_diseases()

        self.health_value = 100
        self.current_lvl = 1
        self.update_info_text()

        camera.position = (self.MAP_SIZE / 2, -35, -20)
        camera.rotation_x = -65

    def initialize_diseases(self):
        add_3_with_each_lvl = 3
        for n in range(add_3_with_each_lvl):
            self.diseases.append(Diseases(self.MAP_SIZE, model='cube', color=color.red, rotation=Vec3(45,45,45)))
       
    def update_info_text(self):

        if self.text1:
            destroy(self.text1)

        health_info_text = f"Health: {self.health_value}"
        self.text1 = Text(origin=(-0.5,9), text=health_info_text, scale=0.05)

        if self.text2:
            destroy(self.text2)

        lvl_info_text = f"Current level: {self.current_lvl}"
        self.text2 = Text(origin=(-0.5,11), text=lvl_info_text, scale=0.05)

    def show_finish_game_info(self):

        if self.text3:
            destroy(self.text3)
        end_info_text = f"End game points: {self.current_lvl * self.health_value}"
        self.text3 = Text(origin=(-0.5,15), text=end_info_text, scale=0.05)

    def is_game_over(self):
        snake = self.snake.snake_elements_positions
        if 0 < snake[0][0] and snake[0][0] < self.MAP_SIZE and 0 < snake[0][1] and snake[0][1] < self.MAP_SIZE:
            return False
        else:
            return True

        return False
    
    def update(self):

        # detecting and handling disease
        for snake_el_position in self.snake.snake_elements_positions:
            snake_sickness_points = was_disease_caught(self.diseases, snake_el_position, self.current_lvl)
            if snake_sickness_points != 0:
                self.health_value -= snake_sickness_points      
                self.update_info_text()   
                break
            
        # gathering health
        was_health_found = calculate_points_distance(self.snake.snake_elements_positions[-1], self.health.position)
        if was_health_found <= 1:
            self.current_lvl += 1
            self.health_value = self.health_value + 5* self.current_lvl
            self.snake.improve_snake()
            self.health.new_position()
            self.initialize_diseases()
            self.update_info_text()
            calculate_points_distance(self.snake.direction, self.health.position)
        
        # if game is over
        if self.is_game_over() or self.health_value <= 0:
            print("game over")
            self.show_finish_game_info()
            application.pause()

        for key, value in held_keys.items():
            print(key)
            if value != 0:
                if key == 'escape' and application.paused:
                    exit()

        #moving snake
        self.snake.move_snake()

if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()