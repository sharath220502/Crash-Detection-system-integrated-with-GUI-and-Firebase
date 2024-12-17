import tkinter as tk

class CarGUI:
    def _init_(self, root):
        self.root = root
        self.canvas_width = 1500
        self.canvas_height = 700
        self.car_width = 80
        self.car_height = 40
        self.car_x = 0
        self.car_speed = 5
        self.is_stopped = False

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.road_image = tk.PhotoImage(file="./road_image.png")
        self.road = self.canvas.create_image(
            self.canvas_width / 2, self.canvas_height / 2,
            image=self.road_image
        )

        self.car_image = tk.PhotoImage(file="./car_image.png")
        self.car = self.canvas.create_image(
            self.car_x, self.canvas_height / 2 + 20,
            image=self.car_image
        )

        self.distance_label = tk.Label(root, text="", font=("Arial", 16))
        self.distance_label.pack()

    def move_car(self):
        if not self.is_stopped:
            self.canvas.move(self.car, self.car_speed, 0)
            self.car_x += self.car_speed
            if self.car_x > self.canvas_width:
                self.car_x = -self.car_width
                self.canvas.move(self.car, -self.canvas_width - self.car_width, 0)
        self.root.after(50, self.move_car)

    def stop_car(self):
        self.is_stopped = True

    def start_car(self):
        self.is_stopped = False

    def update_distance_label(self, distance):
        self.distance_label.config(text=f"Distance: {distance}")

def check_distance(car_gui, distances, index):
    if index >= len(distances):
        car_gui.stop_car()
        return

    current_distance = distances[index]

    if current_distance < 10:
        car_gui.stop_car()
    elif current_distance >= 10:
        if car_gui.is_stopped:
            car_gui.start_car()

    car_gui.update_distance_label(current_distance)
    car_gui.root.after(3000, check_distance, car_gui, distances, index + 1)

def main():
    root = tk.Tk()
    root.title("Moving Car GUI")
    car_gui = CarGUI(root)
    car_gui.move_car()

    # Read distances from a text file
    try:
        with open("./distances.txt", "r") as file:
            lines = file.readlines()
            distances = [float(line.strip()) for line in lines if line.strip()]
            check_distance(car_gui, distances, 0)
    except FileNotFoundError:
        print("Distances file not found.")

    root.mainloop()

if __name__ == "_main_":
    main()
