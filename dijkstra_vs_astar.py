"""Dijkstra's algorithm vs. A* on a 60x60 grid with a barrier.

Course project for CS 301 (Binghamton University).
Every move costs 1 and moves are 4-directional. A* uses Manhattan distance
(the walking distance on the grid) as its heuristic.

Run:  python dijkstra_vs_astar.py
Needs: matplotlib  (pip install matplotlib)
Saves: figure3.png
"""
import heapq

SIZE = 60
START = (30, 8)    # (row, col)
GOAL = (30, 54)

# A vertical "river" in column 34, rows 8-51. The only crossings are the open
# cells above row 8 and below row 51.
BARRIER = {(r, 34) for r in range(8, 52)}


def in_bounds(cell):
    r, c = cell
    return 0 <= r < SIZE and 0 <= c < SIZE


def get_neighbors(cell):
    r, c = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        n = (r + dr, c + dc)
        if in_bounds(n) and n not in BARRIER:
            yield n


def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def search(use_astar=False):
    frontier = [(0, 0, START)]
    distances = {START: 0}
    parents = {START: None}
    visited = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)

        if current == GOAL:
            break

        for neighbor in get_neighbors(current):
            new_cost = distances[current] + 1

            if new_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_cost
                parents[neighbor] = current

                h = heuristic(neighbor, GOAL) if use_astar else 0
                priority = new_cost + h

                # Ties in priority go to the cell closer to the goal (smaller h),
                # then to the cell coordinates. For Dijkstra h is 0, so this is
                # the same as ordering by (priority, neighbor).
                heapq.heappush(frontier, (priority, h, neighbor))

    path, node = [], GOAL
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return visited, path, distances[GOAL]


def draw(ax, visited, path, title):
    import numpy as np

    img = np.ones((SIZE, SIZE, 3))
    for r, c in visited:
        img[r, c] = (0.75, 0.75, 0.75)          # expanded = gray
    ax.imshow(img, interpolation="nearest")

    br = [r for r, _ in BARRIER]
    ax.plot([34, 34], [min(br) - 0.5, max(br) + 0.5], color="black", lw=4,
            solid_capstyle="butt")
    ax.plot([c for _, c in path], [r for r, _ in path], color="#222222", lw=3)
    ax.plot(START[1], START[0], "o", mfc="white", mec="black", ms=7, mew=1.5)
    ax.plot(GOAL[1], GOAL[0], "*", mfc="white", mec="black", ms=12, mew=1.2)
    ax.set_title(title, fontsize=11)
    ax.set_xticks([])
    ax.set_yticks([])


def main():
    d_visited, d_path, d_cost = search(use_astar=False)
    a_visited, a_path, a_cost = search(use_astar=True)

    saved = 1 - len(a_visited) / len(d_visited)
    print(f"Dijkstra: {len(d_visited):,} nodes expanded, route cost {d_cost}")
    print(f"A*:       {len(a_visited):,} nodes expanded, route cost {a_cost}")
    print(f"A* expanded {saved:.0%} fewer nodes on this grid.")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping figure.")
        return

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 5.4))
    draw(axes[0], d_visited, d_path,
         f"Dijkstra's Algorithm\n{len(d_visited):,} nodes expanded, route cost {d_cost}")
    draw(axes[1], a_visited, a_path,
         f"A* Search\n{len(a_visited):,} nodes expanded, route cost {a_cost}")
    fig.tight_layout(pad=1.0, w_pad=2.0)
    fig.savefig("figure3.png", dpi=200, bbox_inches="tight", pad_inches=0.15)
    print("Saved figure3.png")


if __name__ == "__main__":
    main()
