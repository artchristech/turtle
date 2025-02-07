
import turtle
import colorsys
import math
import cv2
import numpy as np
from PIL import ImageGrab
import os

def setup():
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.bgcolor('black')
    screen.title('Rose Curves')
    
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    screen.tracer(0)
    return screen, t

def draw_rose(t, n, d, size, time):
    t.clear()
    k = n / d
    
    # Reduce number of points for better performance
    steps = 360 * d
    angles = np.linspace(0, 4 * np.pi * d, steps, dtype=np.float32)
    
    for offset in range(3):
        scale = size - offset * 20
        # Combine calculations to reduce memory usage
        r = scale * np.cos(k * angles)
        points = np.column_stack((
            r * np.cos(angles + time),
            r * np.sin(angles + time)
        ))
        
        t.penup()
        t.pensize(2)
        hue = (time / 4 + offset / 5) % 1.0
        t.pencolor(*colorsys.hsv_to_rgb(hue, 0.8, 1.0))
        
        # Batch drawing points
        t.goto(points[0][0], points[0][1])
        t.pendown()
        for point in points[1:]:
            t.goto(point[0], point[1])

def capture_frame(screen):
    # Get canvas bounds once
    canvas = screen.getcanvas()
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    # Capture frame directly as numpy array
    frame = np.array(ImageGrab.grab(bbox=(x, y, x + width, y + height)))
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def main():
    screen, t = setup()
    frame_count = 120  # Reduced frame count
    time_values = np.linspace(0, 10, frame_count, dtype=np.float32)
    
    # Setup video writer first
    dummy_frame = capture_frame(screen)
    height, width = dummy_frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('rose_curves.mp4', fourcc, 30, (width, height))
    
    print("Recording animation...")
    for time in time_values:
        n = 4 + np.sin(time / 2)
        draw_rose(t, n, 5, 300, time)
        screen.update()
        # Write frames directly without storing
        out.write(capture_frame(screen))
    
    out.release()
    print("Video saved as 'rose_curves.mp4'")
    screen.bye()

if __name__ == "__main__":
    main()
