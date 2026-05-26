class Node:
    def __init__(self, state=None, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

def expandAndReturnChildren(state_space, node):
    children = []
    for [m, n, c] in state_space:
        if m == node.state: children.append(Node(n, node, node.path_cost + c))
        elif n == node.state: children.append(Node(m, node, node.path_cost + c))
    return children

def ucs(state_space, initial_state, goal_state):
    frontier = [Node(initial_state, None, 0)]
    explored = []

    while frontier:
        frontier.sort(key=lambda x: x.path_cost)
        current_node = frontier.pop(0)
        
        if current_node.state == goal_state:
            solution = []
            trace_node = current_node
            while trace_node is not None:
                solution.insert(0, trace_node.state)
                trace_node = trace_node.parent
            return solution

        explored.append(current_node)
        
        children = expandAndReturnChildren(state_space, current_node)
        for child in children:
            in_exp = child.state in [e.state for e in explored]
            fr_node = next((f for f in frontier if f.state == child.state), None)
            
            if not in_exp and not fr_node:
                frontier.append(child)
            elif fr_node and child.path_cost < fr_node.path_cost:
                fr_node.parent = child.parent
                fr_node.path_cost = child.path_cost

    return []

if __name__ == '__main__':
    delivery_graph = [
        ['HotBird SS15', 'Jalan Kewajipan', 5],
        ['Jalan Kewajipan', 'USJ 8', 15],

        ['HotBird SS15', 'Jalan SS15/3B', 2],
        ['Jalan SS15/3B', 'Persiaran Tujuan', 3],

        ['Persiaran Tujuan', 'Jalan Kewajipan', 8],
        ['Persiaran Tujuan', 'Persiaran Murni', 4],
        ['Persiaran Tujuan', 'Persiaran Bakti', 2],

        ['Persiaran Murni', 'Persiaran Perpaduan', 2],
        ['Persiaran Perpaduan', 'USJ 8', 3],

        ['Persiaran Bakti', 'USJ 8', 6]
    ]

    start_location = "HotBird SS15"
    end_location = "USJ 8"
    
    route = ucs(delivery_graph, start_location, end_location)
    print(f"Cheapest delivery route from {start_location} to {end_location}:")
    print(" -> ".join(route))