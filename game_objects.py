from ursina import *
from random import randrange
import math

class Diseases(Entity):

    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.position = (randrange(self.MAP_SIZE) + 0.5, randrange(self.MAP_SIZE) + 0.5, -0.5)

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
        self.position = (randrange(self.MAP_SIZE) + 0.5, randrange(self.MAP_SIZE) + 0.5, -0.5)

class Snake:
    def __init__(self, MAP_SIZE):
        self.MAP_SIZE = MAP_SIZE
        self.snake_elements = 1
        self.position_length = self.snake_elements + 1
        self.snake_elements_positions = [Vec3(randrange(MAP_SIZE) + 0.5, randrange(MAP_SIZE) + 0.5, -0.5)]
        self.segment_entities = []
        self.create_segment(self.snake_elements_positions[0])
        self.directions = {'a': Vec3(-1, 0, 0), 'd': Vec3(1, 0, 0), 'w': Vec3(0, 1, 0), 's': Vec3(0, -1, 0)}
        self.direction = Vec3(0, 0, 0)
        self.permissions = {'a': 1, 'd': 1, 'w': 1, 's': 1}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

    def improve_snake(self):
        self.snake_elements += 1
        self.position_length += 1
        self.score += 1
        self.create_segment(self.snake_elements_positions[0])

    def create_segment(self, position):
        entity = Entity(position=position)
        Entity(model='cube', color=color.green, position=position).add_script(
            SmoothFollow(speed=25, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    def run(self):
        self.frame_counter += 2
        if not self.frame_counter % self.speed:
            self.control()
            self.snake_elements_positions.append(self.snake_elements_positions[-1] + self.direction)
            self.snake_elements_positions = self.snake_elements_positions[-self.snake_elements:]
            for segment, segment_position in zip(self.segment_entities, self.snake_elements_positions):
                segment.position = segment_position

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permissions[key]:
                self.direction = self.directions[key]
                self.permissions = dict.fromkeys(self.permissions, 1)
                break