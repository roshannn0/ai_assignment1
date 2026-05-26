# Standardized locations
LOCATIONS = ["Sun U.", "Amirah", "Ariffin", "Timothy", "Ernest", "Roshan"]

# Distance Matrix (KM) from the image
DISTANCE_MATRIX = {
    "Sun U.":   {"Sun U.": 0.0,  "Amirah": 0.26, "Ariffin": 21.5, "Timothy": 12.3, "Ernest": 1.6,  "Roshan": 4.2},
    "Amirah":   {"Sun U.": 0.26, "Amirah": 0.0,  "Ariffin": 24.7, "Timothy": 12.5, "Ernest": 1.8,  "Roshan": 4.3},
    "Ariffin":  {"Sun U.": 22.4, "Amirah": 22.3, "Ariffin": 0.0,  "Timothy": 25.7, "Ernest": 20.2, "Roshan": 24.3},
    "Timothy":  {"Sun U.": 14.0, "Amirah": 15.2, "Ariffin": 37.3, "Timothy": 0.0,  "Ernest": 14.6, "Roshan": 9.1},
    "Ernest":   {"Sun U.": 2.5,  "Amirah": 2.4,  "Ariffin": 20.9, "Timothy": 12.9, "Ernest": 0.0,  "Roshan": 5.0},
    "Roshan":   {"Sun U.": 5.9,  "Amirah": 5.9,  "Ariffin": 24.5, "Timothy": 8.3,  "Ernest": 6.7,  "Roshan": 0.0}
}

# Est. Time Travel Matrix (Minutes) from the image
TIME_MATRIX = {
    "Sun U.":   {"Sun U.": 0, "Amirah": 3,  "Ariffin": 28, "Timothy": 16, "Ernest": 5,  "Roshan": 9},
    "Amirah":   {"Sun U.": 3, "Amirah": 0,  "Ariffin": 28, "Timothy": 18, "Ernest": 6,  "Roshan": 11},
    "Ariffin":  {"Sun U.": 26,"Amirah": 26, "Ariffin": 0,  "Timothy": 35, "Ernest": 22, "Roshan": 26},
    "Timothy":  {"Sun U.": 20,"Amirah": 22, "Ariffin": 45, "Timothy": 0,  "Ernest": 18, "Roshan": 14},
    "Ernest":   {"Sun U.": 7, "Amirah": 7,  "Ariffin": 26, "Timothy": 18, "Ernest": 0,  "Roshan": 9},
    "Roshan":   {"Sun U.": 12,"Amirah": 12, "Ariffin": 30, "Timothy": 12, "Ernest": 12, "Roshan": 0}
}

# Find maximum values to normalize and combine them fairly (0.0 to 1.0 scale)
MAX_DISTANCE = max(max(row.values()) for row in DISTANCE_MATRIX.values())  # 37.3 KM
MAX_TIME = max(max(row.values()) for row in TIME_MATRIX.values())          # 45.0 Mins

def compute_combined_score(from_node, to_node, weight_distance=0.5):
    """
    Combines Distance and Time into a single unified cost score using normalization.
    Weight parameter:
      - 0.5: Perfect 50/50 balance of distance and time importance.
    """
    if from_node == to_node:
        return 0.0
        
    dist = DISTANCE_MATRIX[from_node][to_node]
    time = TIME_MATRIX[from_node][to_node]
    
    # Normalize values to 0.0 - 1.0 scale
    norm_dist = dist / MAX_DISTANCE
    norm_time = time / MAX_TIME
    
    # Combined score (weighted average)
    combined_score = (weight_distance * norm_dist) + ((1.0 - weight_distance) * norm_time)
    return combined_score

def greedy_best_first_search_combined(start_node, weight_distance=0.5):
    """
    Greedy Best-First Search using the unified Combined Score of Distance and Time.
    """
    current = start_node
    visited = [start_node]
    total_dist = 0.0
    total_time = 0.0
    calculation_steps = []

    while len(visited) < len(LOCATIONS):
        unvisited = [loc for loc in LOCATIONS if loc not in visited]
        
        next_node = None
        min_score = float('inf')
        
        # We will calculate unified options for printing
        step_options = {}
        
        for neighbor in unvisited:
            score = compute_combined_score(current, neighbor, weight_distance)
            step_options[neighbor] = {
                "distance": DISTANCE_MATRIX[current][neighbor],
                "time": TIME_MATRIX[current][neighbor],
                "score": score
            }
            if score < min_score:
                min_score = score
                next_node = neighbor
        
        chosen_dist = DISTANCE_MATRIX[current][next_node]
        chosen_time = TIME_MATRIX[current][next_node]
        
        calculation_steps.append({
            "from": current,
            "to": next_node,
            "options": step_options,
            "chosen_score": min_score,
            "chosen_dist": chosen_dist,
            "chosen_time": chosen_time
        })
        
        total_dist += chosen_dist
        total_time += chosen_time
        visited.append(next_node)
        current = next_node

    return visited, total_dist, total_time, calculation_steps


if __name__ == '__main__':
    print("=" * 80)
    print("      GREEDY BEST-FIRST SEARCH: UNIFIED DISTANCE & TIME OPTIMIZATION")
    print("=" * 80 + "\n")
    
    # Perfect 50/50 balance between Distance and Time
    weight = 0.5
    path, dist, time, steps = greedy_best_first_search_combined("Sun U.", weight)
    
    print(f"Unified Best Travel Path:  {' ➔ '.join(path)}")
    print(f"Total Distance:          {dist:.2f} KM")
    print(f"Total Travel Time:       {time:.0f} Minutes")
    print("\n" + "-" * 80)
    print("   HOW THE UNIFIED PATH WAS CALCULATED (Step-by-Step with 50/50 Weights)")
    print("-" * 80)
    
    for idx, step in enumerate(steps):
        print(f"\nStep {idx+1}: From '{step['from']}'")
        print(f"  Available Options:")
        for loc, data in step["options"].items():
            # Show math: (0.5 * Normalized Distance) + (0.5 * Normalized Time)
            norm_d = data['distance'] / MAX_DISTANCE
            norm_t = data['time'] / MAX_TIME
            score_math = f"(0.5 * {data['distance']:.2f}/{MAX_DISTANCE}) + (0.5 * {data['time']}/{MAX_TIME})"
            print(f"    - To {loc:<8} : Dist: {data['distance']:>5.2f} KM | Time: {data['time']:>2} mins | Unified Score: {data['score']:.4f}")
            print(f"                   Math: {score_math}")
            
        print(f"  Chosen: '{step['to']}' because it has the lowest Unified Score ({step['chosen_score']:.4f})")
    print("\n" + "=" * 80)
