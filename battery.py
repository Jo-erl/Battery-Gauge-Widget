import tkinter as tk
import psutil

class BatteryGauge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        
        # Set initial size and position
        window_width = 90
        window_height = 35
        
        # Calculate position to place it a bit above the Taskbar at the bottom right
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x_position = screen_width - window_width - 10  # 10 pixels offset from right edge
        y_position = screen_height - window_height - 80  # 80 pixels above the bottom edge
        
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height, bg='black', highlightthickness=0)
        self.canvas.pack()

        self.battery_outline = self.canvas.create_rectangle(5, 5, 85, 30, outline='white', width=2)
        self.battery_fill = self.canvas.create_rectangle(7, 7, 7, 28, fill='green', outline='')
        self.percentage_text = self.canvas.create_text(45, 17, text='', fill='white', font=('Arial', 12, 'bold'))

        self.update_battery()

        self.offset_x = 0
        self.offset_y = 0

        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_button_press(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_mouse_drag(self, event):
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry(f"+{x}+{y}")

    def update_battery(self):
        battery = psutil.sensors_battery()
        if battery is None:
            percent = 0
            is_charging = False
        else:
            percent = battery.percent
            is_charging = battery.power_plugged
        
        if is_charging:
            fill_color = 'green'
        elif percent >= 70:
            fill_color = 'green'
        elif 40 <= percent < 70:
            fill_color = '#FF7900'
        else:
            fill_color = 'red'

        fill_width = int(78 * (percent / 100))
        self.canvas.coords(self.battery_fill, 7, 7, 7 + fill_width, 28)
        self.canvas.itemconfig(self.battery_fill, fill=fill_color)
        self.canvas.itemconfig(self.percentage_text, text=f'{percent}%')

        self.after(5000, self.update_battery)

    def on_closing(self):
        self.iconify()

if __name__ == "__main__":
    app = BatteryGauge()
    app.mainloop()
