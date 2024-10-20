import numpy as np
import random
import pickle
from pathlib import Path


# configs
import yaml
configs = yaml.safe_load(open('./configs.yaml', 'r'))
OBSTACLE, FREE_SPACE = configs['grid_map']['OBSTACLE'], configs['grid_map']['FREE_SPACE']
obstacle_density = configs['obstacle_density']


def generate_random_map(map_h, map_w, num_obstacles, form_h, form_w):
    grid_map = np.full((map_h, map_w), FREE_SPACE)
    counter = 0
    while counter < num_obstacles:
        i = random.randint(0, map_h - 1)
        j = random.randint(0, map_w  - 1)
        if (i < form_h and j < form_w) or (i >= map_h - form_h and j >= map_w - form_w):
            continue
        if grid_map[i][j] == FREE_SPACE:
            grid_map[i][j] = OBSTACLE
            counter += 1
    return grid_map


def save_map_file(map_h, map_w, file_name, grid_map):
    with open(file_name, 'a') as f:
        f.write(f"{map_h},{map_w}\n")
        for i in range(map_h):
            for j in range(map_w):
                if grid_map[i][j] == OBSTACLE:
                    f.write('@')
                elif grid_map[i][j] == FREE_SPACE:
                    f.write('.')
            f.write("\n")


def generate_random_form(num_agents, map_h, map_w, form_h, form_w):
    starts, goals = [], []
    formation = np.zeros((form_h, form_w), dtype=bool)
    counter = 0
    while counter < num_agents:
        i = random.randint(0, form_h - 1)
        j = random.randint(0, form_w - 1)
        if formation[i][j]:
            continue
        starts.append((i, j))
        goals.append((i + map_h - form_h, j + map_w - form_w))
        formation[i][j] = True
        counter += 1
    return starts, goals


def save_form_file(file_name, map_h, map_w, form_h, form_w, num_agents, starts, goals):
    with open(file_name, 'a') as f:
        f.write(f"{map_h},{map_w}\n")
        f.write(f"{form_h},{form_w}\n")
        f.write(f"{num_agents}\n")
        for i in range(num_agents):
            f.write(f"{starts[i][0]},{starts[i][1]},{goals[i][0]},{goals[i][1]}\n")


def main():
    num_maps, num_forms = configs['num_maps'], configs['num_forms']
    for map_size, form_size, num_agents in configs['test_settings']:
        maps, forms = [], []
        num_obstacles = int((map_size * map_size - 2 * form_size * form_size) * obstacle_density)
        for i in range(num_maps):
            grid_map = generate_random_map(map_size, map_size, num_obstacles, form_size, form_size)
            maps.append(grid_map)
            file_name = f"./test_set/maps/ms{map_size}_fs{form_size}_na{num_agents}_{i}.map"
            save_map_file(map_size, map_size, file_name, grid_map)
        for i in range(num_forms):
            starts, goals = generate_random_form(num_agents, map_size, map_size, form_size, form_size)     
            forms.append((starts, goals))       
            file_name = f"./test_set/agents/ms{map_size}_fs{form_size}_na{num_agents}_{i}.agent"
            save_form_file(file_name, map_size, map_size, form_size, form_size, num_agents, starts, goals)
        instances = {'maps': maps, 'forms': forms}
        file_name = f"./test_set/ms{map_size}_fs{form_size}_na{num_agents}.pth"
        with open(file_name, 'wb') as f:
            pickle.dump(instances, f)


if __name__ == '__main__':
    Path("./test_set/maps/").mkdir(parents=True, exist_ok=True)
    Path("./test_set/agents/").mkdir(parents=True, exist_ok=True)
    main()