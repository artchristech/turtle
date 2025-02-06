import turtle
import colorsys
import math
import random

def setup_screen(width, height):
    screen = turtle.Screen()
    screen.setup(width, height)
    screen.bgcolor("#000")
    screen.title("Trippy Mountain Contours")
    return screen

def create_turtle():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    return t

def draw_mountain_contour(t, time, y_offset, amplitude):
    points = []
    for x in range(-400, 401, 5):
        y = math.sin(x/100 + time) * amplitude
        y += math.sin(x/50 + time * 2) * (amplitude/2)
        y += math.sin(x/25 + time * 3) * (amplitude/4)
        y += y_offset
        points.append((x, y))

    hue = (time/5 + y_offset/200) % 1.0
    color = colorsys.hsv_to_rgb(hue, 0.8, 1)
    t.pencolor(color)

    for i, (x, y) in enumerate(points):
        t.penup() if i == 0 else t.pendown()
        t.goto(x, y)

def sacred_grid(h, w):
    screen = setup_screen(w, h)
    t = create_turtle()
    screen.tracer(0)
    t.pensize(2)
    time = 0

    while True:
        t.clear()

        # Draw multiple mountain contours
        for i in range(-5, 6):
            y_offset = i * 60
            amplitude = 100 - abs(i) * 8
            draw_mountain_contour(t, time + i/5, y_offset, amplitude)

        screen.update()
        time += 0.03

sacred_grid(600, 800)
turtle.done()
