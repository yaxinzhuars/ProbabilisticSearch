import random
from Cell import *


class Landscape(object):
    def __init__(self):
        self.dim = 50
        self.env = self.gen_landscape(0.2, 0.3, 0.3, 0.2)
        target_x = random.randint(0, self.dim - 1)
        target_y = random.randint(0, self.dim - 1)
        self.target_index = (target_x, target_y)
        self.env[target_x][target_y].set_target()
        terrain_list = ['flat', 'hilly', 'forest', 'cave']
        terrain_list.remove(self.env[target_x][target_y].type)
        self.tracker = random.choice(terrain_list)
        self.tracker_history = ''
        
    def gen_landscape(self, p_flat, p_hilly, p_forest, p_cave):
        landscape = [['0' for col in range(self.dim)] for row in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                p = random.random()
                if p < p_flat:
                    landscape[i][j] = Cell('flat')
                elif p < p_flat + p_hilly:
                    landscape[i][j] = Cell('hilly')
                elif p < p_flat + p_hilly + p_forest:
                    landscape[i][j] = Cell('forest')
                elif p < p_flat + p_hilly + p_forest + p_cave:
                    landscape[i][j] = Cell('cave')
        return landscape

    def get_cell_with_highest_belief(self):
        current_belief = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_belief.append(self.env[i][j].belief[-1])
        index = current_belief.index(max(current_belief))
        return (index // self.dim, index % self.dim)

    def get_cell_with_highest_p_of_finding(self):
        current_pfind = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_pfind.append(self.env[i][j].belief[-1]*(1-self.env[i][j].fn))
        index = current_pfind.index(max(current_pfind))
        return (index // self.dim, index % self.dim)

    def get_cell_with_highest_belief_rand(self):
        current_belief = {}
        for i in range(self.dim):
            for j in range(self.dim):
                current_belief[(i, j)] = self.env[i][j].belief[-1]
        indices = [i for i, m in current_belief.items() if m == max(current_belief.values())]
        index = random.sample(indices, 1)[0]
        return index

    def get_cell_with_highest_p_of_finding_rand(self):
        current_pfind = {}
        for i in range(self.dim):
            for j in range(self.dim):
                current_pfind[(i, j)] = self.env[i][j].belief[-1]*(1-self.env[i][j].fn)
        indices = [i for i, m in current_pfind.items() if m == max(current_pfind.values())]
        index = random.sample(indices, 1)[0]
        return index

    def get_cell_with_highest_belief_dist_factor(self, cell):
        (x, y) = cell
        if x == -1 and y == -1:
            while True:
                x = random.randint(0, self.dim-1)
                y = random.randint(0, self.dim-1)
                if self.env[x][y].type == 'flat':
                    break
            return (x, y)
        (max_x, max_y) = (-1, -1)
        max_belief = 0
        max_dist = 0
        dist_belief_matrix = []
        for i in range(self.dim):
            dist_belief_list = []
            for j in range(self.dim):
                dist = abs(x-i) + abs(y-j)
                curr_belief = self.env[i][j].belief[-1] * (1 - pow(dist,2) * 0.01)
                if curr_belief > max_belief:
                    max_belief = curr_belief
                    (max_x, max_y) = (i, j)
                    max_dist = dist
                elif curr_belief == max_belief:
                    if dist < max_dist:
                        (max_x, max_y) = (i, j)
                        max_dist = dist
                dist_belief_list.append(curr_belief)
            dist_belief_matrix.append(dist_belief_list)
        neighbor_d = max_dist
        neighbor_belif = 0
        (next_x, next_y) = (x, y)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i <= self.dim - 1 and 0 <= y + j <= self.dim - 1 and (i==0 or j==0):
                    d = abs(x + i - max_x) + abs(y + j - max_y)
                    if neighbor_d > d:
                        neighbor_d = d
                        neighbor_belif = dist_belief_matrix[x+i][y+j]
                        (next_x, next_y) = (x+i, y+j)
                    elif neighbor_d == d:
                        if neighbor_belif < dist_belief_matrix[x+i][y+j]:
                            neighbor_belif = dist_belief_matrix[x+i][y+j]
                            (next_x, next_y) = (x+i, y+j)
        return (next_x, next_y)

    def get_cell_with_highest_p_of_finding_dist_factor(self, cell):
        (x, y) = cell
        if x == -1 and y == -1:
            while True:
                x = random.randint(0, self.dim-1)
                y = random.randint(0, self.dim-1)
                if self.env[x][y].type == 'flat':
                    break
            return (x, y)
        (max_x, max_y) = (-1, -1)
        max_belief = 0
        max_dist = 0
        dist_belief_matrix = []
        for i in range(self.dim):
            dist_belief_list = []
            for j in range(self.dim):
                dist = abs(x-i) + abs(y-j)
                curr_belief = self.env[i][j].belief[-1] * (1-self.env[i][j].fn) * (1 - pow(dist,2) * 0.01)
                if curr_belief > max_belief:
                    max_belief = curr_belief
                    (max_x, max_y) = (i, j)
                    max_dist = dist
                elif curr_belief == max_belief:
                    if dist < max_dist:
                        (max_x, max_y) = (i, j)
                        max_dist = dist
                dist_belief_list.append(curr_belief)
            dist_belief_matrix.append(dist_belief_list)
        neighbor_d = max_dist
        neighbor_belif = 0
        (next_x, next_y) = (x, y)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i <= self.dim - 1 and 0 <= y + j <= self.dim - 1 and (i==0 or j==0):
                    d = abs(x + i - max_x) + abs(y + j - max_y)
                    if neighbor_d > d:
                        neighbor_d = d
                        neighbor_belif = dist_belief_matrix[x+i][y+j]
                        (next_x, next_y) = (x+i, y+j)
                    elif neighbor_d == d:
                        if neighbor_belif < dist_belief_matrix[x+i][y+j]:
                            neighbor_belif = dist_belief_matrix[x+i][y+j]
                            (next_x, next_y) = (x+i, y+j)
        return (next_x, next_y)

    def target_move(self):
        self.tracker_history = self.tracker
        (target_x, target_y) = self.target_index
        next_location = []
        if target_x - 1 >= 0:
            next_location.append((target_x - 1, target_y))
        if target_x + 1 <= self.dim - 1:
            next_location.append((target_x + 1, target_y))
        if target_y - 1 >= 0:
            next_location.append((target_x, target_y - 1))
        if target_y + 1 <= self.dim - 1:
            next_location.append((target_x, target_y + 1))
        (n_target_x, n_target_y) = random.choice(next_location)
        self.env[target_x][target_y].remove_target()
        self.env[n_target_x][n_target_y].set_target()
        self.target_index = (n_target_x, n_target_y)
        terrain_list = ['flat', 'hilly', 'forest', 'cave']
        terrain_list.remove(self.env[n_target_x][n_target_y].type)
        self.tracker = random.choice(terrain_list)

    def get_cell_with_highest_belief_moving_target(self):
        local_belief = [[self.env[i][j].belief[-1] for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                if self.env[i][j].type == self.tracker_history:
                    valid_neighbor = []
                    if i - 1 >= 0:
                        valid_neighbor.append((i - 1, j))
                    if i + 1 <= self.dim - 1:
                        valid_neighbor.append((i + 1, j))
                    if j - 1 >= 0:
                        valid_neighbor.append((i, j - 1))
                    if j + 1 <= self.dim - 1:
                        valid_neighbor.append((i, j + 1))
                    for k in range(len(valid_neighbor)):
                        (valid_i, valid_j) = valid_neighbor[k]
                        if local_belief[valid_i][valid_j] - local_belief[i][j] / len(valid_neighbor) > 0:
                            local_belief[valid_i][valid_j] -= local_belief[i][j] / len(valid_neighbor)
        for i in range(self.dim):
            for j in range(self.dim):
                if self.env[i][j].type == self.tracker:
                    local_belief[i][j] = 0

        current_belief = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_belief.append(local_belief[i][j])
        index = current_belief.index(max(current_belief))
        return (index // self.dim, index % self.dim)

    def get_cell_with_highest_p_of_finding_moving_target(self):
        local_belief = [[self.env[i][j].belief[-1] for j in range(self.dim)] for i in range(self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                if self.env[i][j].type == self.tracker_history:
                    valid_neighbor = []
                    if i - 1 >= 0:
                        valid_neighbor.append((i - 1, j))
                    if i + 1 <= self.dim - 1:
                        valid_neighbor.append((i + 1, j))
                    if j - 1 >= 0:
                        valid_neighbor.append((i, j - 1))
                    if j + 1 <= self.dim - 1:
                        valid_neighbor.append((i, j + 1))
                    for k in range(len(valid_neighbor)):
                        (valid_i, valid_j) = valid_neighbor[k]
                        if local_belief[valid_i][valid_j] - local_belief[i][j] / len(valid_neighbor) > 0:
                            local_belief[valid_i][valid_j] -= local_belief[i][j] / len(valid_neighbor)
        for i in range(self.dim):
            for j in range(self.dim):
                if self.env[i][j].type == self.tracker:
                    local_belief[i][j] = 0

        current_p_find = []
        for i in range(self.dim):
            for j in range(self.dim):
                current_p_find.append(local_belief[i][j] * (1 - self.env[i][j].fn))
        index = current_p_find.index(max(current_p_find))
        return (index // self.dim, index % self.dim)
