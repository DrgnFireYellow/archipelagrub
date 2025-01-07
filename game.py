import pygame
import os
import numpy as np
import random
import math
from pathlib import Path

TILE_WIDTH = 16
TILE_HEIGHT = 32


pygame.init()

screen = pygame.display.set_mode((1000, 750), pygame.SCALED, vsync=1)

pygame.display.set_caption("Archipelagrub")

clock = pygame.time.Clock()

pos = [0, 0]


def generate_terrain(map_size):
    map = np.full((map_size, map_size), "0")

    # Use the Voronoi Algorithm to generate islands

    number_of_seeds = map_size * 3
    seeds = []
    seed_types = ["0", "1"]
    seed_weights = [1, 2]

    for seed in range(number_of_seeds):
        seeds.append(
            {
                "type": random.choices(seed_types, seed_weights)[0],
                "position": (
                    random.randint(0, map_size - 1),
                    random.randint(0, map_size - 1),
                ),
            }
        )

    seeds.append({"type": "1", "position": (map_size / 2, map_size / 2)})

    for row in range(len(map)):
        for column in range(len(map)):
            seed_distances = {}
            for seed in seeds:
                seed_distances[
                    math.hypot(column - seed["position"][0], row - seed["position"][1])
                ] = seed["type"]
            map[row][column] = seed_distances[min(seed_distances)]

    # Generate Trees
    objects = np.full((map_size, map_size), None)

    
    for tree in range(int(map_size * 3)):
        treex = random.randint(0, map_size - 1)
        treey = random.randint(0, map_size - 1)

        while (
            treey + 1 >= map_size
            or map[treey + 1][treex] == "1"
            or (treex > 0 and objects[treey][treex - 1] == "2")
            or (treex < map_size - 1 and objects[treey][treex + 1] == "2")
        ):
            treex = random.randint(0, map_size - 1)
            treey = random.randint(0, map_size - 1)

        objects[treey][treex] = "2"

    return [map.tolist(), objects]


layers = generate_terrain(75)

tiles = {}

for tile in os.listdir("assets/tiles"):
    tileid = Path(tile).stem
    tiles[tileid] = pygame.image.load(
        os.path.join("assets", "tiles", tile)
    ).convert_alpha()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_LEFT]:
        pos[0] -= 1

    if pressed_keys[pygame.K_RIGHT]:
        pos[0] += 1

    if pressed_keys[pygame.K_UP]:
        pos[1] -= 1

    if pressed_keys[pygame.K_DOWN]:
        pos[1] += 1

    screen.fill((0, 0, 0))

    tile_scale = pygame.display.get_window_size()[1] / 15 / TILE_WIDTH

    for map in layers:
        for row in range(len(map)):
            for column in range(len(map[row])):
                if map[row][column] != None:
                    screen.blit(
                        pygame.transform.scale_by(tiles[map[row][column]], tile_scale),
                        (
                            int(column) * TILE_WIDTH * tile_scale
                            - (pos[0] * TILE_WIDTH * tile_scale),
                            int(row) * TILE_WIDTH * tile_scale
                            - (pos[1] * TILE_WIDTH * tile_scale),
                        ),
                    )

    pygame.display.update()
