import matplotlib.pyplot as plt

def visualize_layout(room_width, room_height, furniture_width, furniture_height, x, y):
    fig, ax = plt.subplots()
    room = plt.Rectangle((0, 0), room_width, room_height, fill=None, edgecolor="black", linewidth=2)
    furniture = plt.Rectangle((x, y), furniture_width, furniture_height, fill=True, color="blue")

    ax.add_patch(room)
    ax.add_patch(furniture)
    plt.xlim(0, room_width)
    plt.ylim(0, room_height)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.title("Optimized Furniture Placement")
    plt.show()

# Example visualization
visualize_layout(15, 15, 3, 3, 5, 5)
