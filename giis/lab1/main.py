import tkinter as tk


class GraphicsEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Graphics Editor")

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.grid_visible = True

        self.toggle_grid_button = tk.Button(self, text="Toggle Grid", command=self.toggle_grid)
        self.toggle_grid_button.pack()

        self.canvas.bind("<Button-1>", self.draw_point)

        self.points = []
        self.lines = []

        self.method = tk.StringVar()
        self.method.set("DDA")

        self.radio_frame = tk.Frame(self)
        self.radio_frame.pack()
        self.dda_button = tk.Radiobutton(self.radio_frame, text="DDA", variable=self.method, value="DDA",
                                         command=self.change_button_color)
        self.dda_button.pack(side=tk.LEFT)
        self.bresenham_button = tk.Radiobutton(self.radio_frame, text="Bresenham", variable=self.method,
                                               value="Bresenham", command=self.change_button_color)
        self.bresenham_button.pack(side=tk.LEFT)
        self.wu_button = tk.Radiobutton(self.radio_frame, text="Wu", variable=self.method, value="Wu",
                                        command=self.change_button_color)
        self.wu_button.pack(side=tk.LEFT)

        self.build_button = tk.Button(self, text="Build Line", command=self.build_line)
        self.build_button.pack()

        self.draw_grid()

    def draw_point(self, event):
        x, y = event.x, event.y
        nearest_x = ((x + 10) // 20) * 20
        nearest_y = ((y + 10) // 20) * 20
        self.points.append((nearest_x, nearest_y))
        self.canvas.create_oval(nearest_x - 2, nearest_y - 2, nearest_x + 2, nearest_y + 2, fill="black")

    def build_line(self):
        if len(self.points) >= 2:
            method = self.method.get()
            if method == "DDA":
                self.build_by_dda(self.points[-2], self.points[-1])
            elif method == "Bresenham":
                self.build_bresenham_line(self.points[-2], self.points[-1])
            elif method == "Wu":
                self.build_wu_line(self.points[-2], self.points[-1])

    def build_by_dda(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        dx = x2 - x1
        dy = y2 - y1
        length = max(abs(dx), abs(dy))
        dx /= length
        dy /= length
        x = x1 + 0.5 * dx
        y = y1 + 0.5 * dy
        line = []
        for _ in range(int(length)):
            line.append(self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="blue", outline="blue"))
            x += dx
            y += dy
        self.lines.append(line)

    def build_bresenham_line(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        line = []
        while True:
            line.append(self.canvas.create_rectangle(x1, y1, x1 + 1, y1 + 1, fill="red", outline="red"))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        self.lines.append(line)

    def build_wu_line(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            gradient = dy / dx
            y = y1 + gradient
            for x in range(x1 + 1, x2):
                self.canvas.create_rectangle(x, int(y), x + 1, int(y) + 1, fill="green", outline="green")
                self.canvas.create_rectangle(x, int(y) + 1, x + 1, int(y) + 2, fill="green", outline="green")
                y += gradient
        else:
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            gradient = dx / dy
            x = x1 + gradient
            for y in range(y1 + 1, y2):
                self.canvas.create_rectangle(int(x), y, int(x) + 1, y + 1, fill="green", outline="green")
                self.canvas.create_rectangle(int(x) + 1, y, int(x) + 2, y + 1, fill="green", outline="green")
                x += gradient

    def toggle_grid(self):
        if self.grid_visible:
            self.canvas.delete("grid")
            self.grid_visible = False
        else:
            self.draw_grid()
            self.grid_visible = True

    def draw_grid(self):
        for i in range(0, 401, 20):
            self.canvas.create_line(0, i, 400, i, fill="lightgray", tags="grid")
        for i in range(0, 401, 20):
            self.canvas.create_line(i, 0, i, 400, fill="lightgray", tags="grid")

    def change_button_color(self):
        method = self.method.get()
        if method == "DDA":
            self.dda_button.config(fg="blue")
            self.bresenham_button.config(fg="black")
            self.wu_button.config(fg="black")
        elif method == "Bresenham":
            self.dda_button.config(fg="black")
            self.bresenham_button.config(fg="red")
            self.wu_button.config(fg="black")
        elif method == "Wu":
            self.dda_button.config(fg="black")
            self.bresenham_button.config(fg="black")
            self.wu_button.config(fg="green")


if __name__ == "__main__":
    app = GraphicsEditor()
    app.mainloop()
