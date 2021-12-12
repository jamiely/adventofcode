import re
lines = open('day12.input', 'r').readlines()
print(lines)
adjlist = {}
for line in lines:
    s, e = line.strip().split('-')
    if s not in adjlist:
        adjlist[s] = set()
    adjlist[s].add(e)
    if e not in adjlist:
        adjlist[e] = set()
    adjlist[e].add(s)
print(adjlist)

routes = []

def is_small_cave(neighbor):
    return re.match(r'^[a-z]', neighbor)

def explore(node_name, route, visited):
    route.append(node_name)
    if node_name == 'end':
        routes.append(route.copy())
        return

    if node_name not in visited:
        visited[node_name] = 0
    visited[node_name] += 1

    if visited[node_name] > 1 and is_small_cave(node_name):
        visited['already_visited_cave_twice'] = True

    for neighbor in adjlist[node_name]:
        if neighbor == 'start':
            continue
        if visited['already_visited_cave_twice'] and neighbor in visited and is_small_cave(neighbor):
            continue
        explore(neighbor, route.copy(), visited.copy())


explore('start', [], {'already_visited_cave_twice': False})
for route in routes:
    print(', '.join(route))
#     start
#     /   \
# c--A-----b--d
#     \   /
#      end
print(f"{len(routes)} routes")

