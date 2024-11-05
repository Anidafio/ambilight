import tkinter as tk
import serial.tools.list_ports

class GUI(tk.Frame):
    def __init__(self, master, start_callback, stop_callback, show_overlay_callback, hide_overlay_callback, update_overlay_callback):
        super().__init__(master)
        self.master = master
        self.master.title("Ambient Light Configuration")
        
        # Initialize callback functions
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.show_overlay_callback = show_overlay_callback
        self.hide_overlay_callback = hide_overlay_callback
        self.update_overlay_callback = update_overlay_callback

        # Number of LEDs on each side
        tk.Label(self, text="Horizontal LEDs:").grid(row=0, column=0, padx=5, pady=5)
        self.horizontal_leds = tk.IntVar(value=18)
        tk.Entry(self, textvariable=self.horizontal_leds, width=10).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Vertical LEDs:").grid(row=1, column=0, padx=5, pady=5)
        self.vertical_leds = tk.IntVar(value=10)
        tk.Entry(self, textvariable=self.vertical_leds, width=10).grid(row=1, column=1, padx=5, pady=5)

        # Edge step from screen (in pixels)
        tk.Label(self, text="Edge Step (px):").grid(row=2, column=0, padx=5, pady=5)
        self.edge_step = tk.IntVar(value=50)
        edge_step_entry = tk.Entry(self, textvariable=self.edge_step, width=10)
        edge_step_entry.grid(row=2, column=1, padx=5, pady=5)
        edge_step_entry.bind("<Return>", lambda event: self.update_overlay_callback())
        
        # Zone depth slider
        tk.Label(self, text="Zone Depth:").grid(row=3, column=0, padx=5, pady=5)
        self.zone_depth = tk.IntVar(value=50)
        zone_depth_slider = tk.Scale(self, from_=10, to=200, orient="horizontal", variable=self.zone_depth)
        zone_depth_slider.grid(row=3, column=1, padx=5, pady=5)
        zone_depth_slider.bind("<B1-Motion>", lambda event: self.update_overlay_callback())

        # Preview Zones checkbox and Refresh Preview button
        self.preview_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Preview Zones", variable=self.preview_enabled, command=self.toggle_preview).grid(row=4, column=0, padx=5, pady=5)

        # Serial port selection
        tk.Label(self, text="Arduino Port:").grid(row=5, column=0, padx=5, pady=5)
        self.port_var = tk.StringVar()
        self.port_dropdown = tk.OptionMenu(self, self.port_var, *self.get_serial_ports())
        self.port_dropdown.grid(row=5, column=1, padx=5, pady=5)

        # Refresh Ports Button
        self.refresh_button = tk.Button(self, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # Start/Stop Buttons
        self.start_button = tk.Button(self, text="Start", command=self.start_callback)
        self.start_button.grid(row=6, column=0, padx=5, pady=10)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_callback, state=tk.DISABLED)
        self.stop_button.grid(row=6, column=1, padx=5, pady=10)
    
    def refresh_ports(self):
        """Refresh the list of serial ports."""
        self.port_var.set("")  # Clear the current selection
        menu = self.port_dropdown["menu"]
        menu.delete(0, "end")  # Clear the current menu options
        new_ports = self.get_serial_ports()
        for port in new_ports:
            menu.add_command(label=port, command=lambda value=port: self.port_var.set(value))
            
    def toggle_preview(self):
        if self.preview_enabled.get():
            self.show_overlay_callback()
        else:
            self.hide_overlay_callback()

    def get_serial_ports(self):
        """List all available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]