import turtle
import math
import random

def setup_turtle():
    """Initialize the turtle with proper settings"""
    screen = turtle.Screen()
    screen.title("Neural Network Art - Interactive Configurator")
    screen.setup(1000, 700)  # Increased size for control panel
    screen.bgcolor("black")

    # Create main drawing turtle
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    # Create text display turtle
    text = turtle.Turtle()
    text.speed(0)
    text.hideturtle()
    text.color("white")

    screen.tracer(0)  # Turn off animation for faster drawing
    return t, text, screen

def draw_neuron(t, x, y, size, activation):
    """Draw a neuron with activation color"""
    color = f"#{int(255 * activation):02x}00{int(255 * (1-activation)):02x}"

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(size)
    t.end_fill()

def draw_synapse(t, x1, y1, x2, y2, weight):
    """Draw a connection between neurons with weight-based thickness"""
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.pensize(weight * 2)
    t.pencolor(f"#{int(255 * weight):02x}ff{int(255 * weight):02x}")
    t.goto(x2, y2)

def sigmoid(x):
    """Sigmoid activation function"""
    return 1 / (1 + math.exp(-x))

def draw_network(t, layers):
    """Draw the complete neural network"""
    t.clear()
    positions = []
    layer_spacing = 150

    # Calculate maximum neurons in any layer for scaling
    max_neurons = max(layers)
    neuron_spacing = min(40, 300 / max_neurons)

    # Draw layers
    for l, layer_size in enumerate(layers):
        layer_positions = []
        layer_x = -300 + l * layer_spacing

        for n in range(layer_size):
            y_offset = (layer_size - 1) * neuron_spacing / 2
            y = -y_offset + n * neuron_spacing

            activation = sigmoid(random.uniform(-2, 2))
            draw_neuron(t, layer_x, y, 10, activation)
            layer_positions.append((layer_x, y))

        positions.append(layer_positions)

    # Draw synapses between layers
    for l in range(len(layers) - 1):
        for pos1 in positions[l]:
            for pos2 in positions[l + 1]:
                weight = random.uniform(0.1, 1.0)
                draw_synapse(t, pos1[0], pos1[1], pos2[0], pos2[1], weight)

def update_instructions(text, layers, selected_layer):
    """Update the instruction panel"""
    text.clear()
    text.penup()
    text.goto(200, 250)

    instructions = [
        "Neural Network Layer Configurator",
        "",
        "Controls:",
        "← → : Select Layer",
        "↑ ↓ : Adjust Neurons",
        "R : Reset Network",
        "Q : Quit",
        "",
        "Current Configuration:"
    ]

    for i, line in enumerate(instructions):
        text.goto(200, 250 - i * 30)
        text.write(line, align="left", font=("Arial", 12, "normal"))

    # Display layer information
    for i, size in enumerate(layers):
        text.goto(200, 250 - (len(instructions) + i) * 30)
        if i == selected_layer:
            text.write(f"Layer {i+1}: {size} neurons  <<<", align="left", font=("Arial", 12, "bold"))
        else:
            text.write(f"Layer {i+1}: {size} neurons", align="left", font=("Arial", 12, "normal"))

def create_interactive_neural_art():
    """Main function to create and control the neural network visualization"""
    t, text, screen = setup_turtle()

    # Initial network configuration
    layers = [4, 6, 6, 4]
    selected_layer = 0

    def update_visualization():
        draw_network(t, layers)
        update_instructions(text, layers, selected_layer)
        screen.update()

    # Key bindings
    def select_prev_layer():
        nonlocal selected_layer
        selected_layer = (selected_layer - 1) % len(layers)
        update_visualization()

    def select_next_layer():
        nonlocal selected_layer
        selected_layer = (selected_layer + 1) % len(layers)
        update_visualization()

    def increase_neurons():
        nonlocal layers
        if layers[selected_layer] < 10:  # Maximum 10 neurons per layer
            layers[selected_layer] += 1
            update_visualization()

    def decrease_neurons():
        nonlocal layers
        if layers[selected_layer] > 1:  # Minimum 1 neuron per layer
            layers[selected_layer] -= 1
            update_visualization()

    def reset_network():
        nonlocal layers
        layers = [4, 6, 6, 4]
        update_visualization()

    # Register key bindings
    screen.onkey(select_prev_layer, "Left")
    screen.onkey(select_next_layer, "Right")
    screen.onkey(increase_neurons, "Up")
    screen.onkey(decrease_neurons, "Down")
    screen.onkey(reset_network, "r")
    screen.onkey(screen.bye, "q")

    screen.listen()
    update_visualization()
    screen.mainloop()

if __name__ == "__main__":
    create_interactive_neural_art()
