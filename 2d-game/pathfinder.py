# -*- coding: utf-8 -*-
import heapq

class PriorityQueue(object):
   def __init__(self):
      self.elements = []
   
   def empty(self):
      return len(self.elements) == 0
   
   def put(self, item, priority):
      heapq.heappush(self.elements, (priority, item))
   
   def get(self):
      return heapq.heappop(self.elements)[1]

class PathFinder(object):
    def __init__(self, map):
        self.nodes = map

    def neighbours(self, node):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for dir in dirs:
            neighbour = (node[0] + dir[0], node[1] + dir[1])
            for possible_neighbour in self.nodes:
                if possible_neighbour[0] == neighbour[0] and possible_neighbour[1] == neighbour[1]:
                    result.append((neighbour[0], neighbour[1]))
        return result

    def search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            for next in self.neighbours(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        return path

    def heuristic(self, a, b):
       (x1, y1) = a
       (x2, y2) = b
       return abs(x1 - x2) + abs(y1 - y2)

    def find(self, start, goal):
        cf, csf = self.search(start, goal)
        return self.reconstruct_path(cf, start, goal)

    def draw(self, start, goal):
        cf, csf = self.search(start, goal)
        path = self.reconstruct_path(cf, start, goal)
        line = ""
        for i, node in enumerate(self.nodes, start=1):
            if node in path:
                line += " . "
            else:
                line += " # "
            if i % self.width == 0:
                print line
                line = ""