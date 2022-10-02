# Imports
from tkinter import Tk, Canvas
from os import system

# App
class App(Tk):
    def __init__(self, width, height):
        # Initialization
        Tk.__init__(self)
        self.title("TkSize")
        self.resizable(False, False)
        self.width = width
        self.height = height
        self.geometry(f"{self.width}x{self.height}")
        self.has_first_point = False
        self.has_second_point = False

        # Making Canvas
        self.canvas = Canvas()
        self.canvas.config(bg="blue")
        self.canvas.pack(expand=1, fill="both")

        # Starting lines
        self.x_line = self.canvas.create_line(0, self.height / 2, self.width, self.height / 2)
        self.y_line = self.canvas.create_line(self.width / 2, 0, self.width / 2, self.height)

        # Info labels
        self.mouse_label = self.canvas.create_text(self.width - 70, self.height - 42, text="(N/A, N/A)", font="Verdana 15")
        self.resolution_label = self.canvas.create_text(self.width - 70, self.height - 18, text="N/A", font="Verdana 15", fill="yellow")

        # Bindings
        self.bind("<Motion>", self.handle_motion)
        self.bind("<Button-1>", self.handle_lclick)

    def handle_motion(self, event):
        # Removing past lines
        self.canvas.delete(self.x_line)
        self.canvas.delete(self.y_line)

        # Making new lines
        self.x_line = self.canvas.create_line(0, event.y, self.width, event.y)
        self.y_line = self.canvas.create_line(event.x, 0, event.x, self.height)

        # Editing text
        self.canvas.itemconfig(self.mouse_label, text=f"({event.x}, {event.y})")

    def handle_lclick(self, event):
        if self.has_first_point and (not self.has_second_point):
            # Drawing second point
            self.second_point = self.canvas.create_rectangle(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill="yellow")
            self.has_second_point = True

            # Drawing huge border and getting its coordinates (latter first)
            first_point_coordinates = self.canvas.bbox(self.first_point)
            first_point_x = (first_point_coordinates[2] + first_point_coordinates[0]) / 2
            first_point_y = (first_point_coordinates[3] + first_point_coordinates[1]) / 2

            second_point_coordinates = self.canvas.bbox(self.second_point)
            second_point_x = (second_point_coordinates[2] + second_point_coordinates[0]) / 2
            second_point_y = (second_point_coordinates[3] + second_point_coordinates[1]) / 2

            self.resolution_rectangle = self.canvas.create_rectangle(first_point_x, first_point_y, second_point_x, second_point_y, outline="yellow", width=2)

            # Updating text
            self.canvas.itemconfig(self.resolution_label, text=f"{round(abs(second_point_x - first_point_x))}x{round(abs(second_point_y - first_point_y))}")

        elif (not self.has_first_point) and (not self.has_second_point):
            # Making first point
            self.has_first_point = True
            self.first_point = self.canvas.create_rectangle(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill="yellow")

        else:
            # Reset (if the rectangle has already been made with 2 points)
            self.canvas.delete(self.first_point)
            self.canvas.delete(self.second_point)
            self.canvas.delete(self.resolution_rectangle)
            self.has_first_point, self.has_second_point = False, False
            self.canvas.itemconfig(self.resolution_label, text="N/A")

# Getting resolutions in a foolproof way
system("title TkSize Initialization") # Setting system title
try:
    width = int(input("Enter width (default is 1200): ").strip())
    if width < 100 or width > 1800:
        raise ValueError

except ValueError:
    width = 1200
print("Width set to", width)

try:
    height = int(input("Enter width (default is 600): ").strip())
    if height < 100 or height > 1800:
        raise ValueError
except ValueError:
    height = 600
print("Height set to", height)

# Setting app
app = App(width, height)
app.mainloop()
